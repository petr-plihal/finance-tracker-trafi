"""Class for managing loaded bank statements"""
import os
import pandas as pd

from sqlalchemy import select
from pandas import Timestamp
from decimal import Decimal

from app.extensions import db
from app.models.database import Account, Currency, Transaction

from app.exceptions import StatementFileNotFoundError, StatementFileEmptyError

class StatementManager:
    """
    Manages the bank statement DataFrame, handling the initial loading, cleaning, and persistent storage.

    **Only handles KB bank file format for inputs.**
    Attributes:
        file_path (str): The path to the CSV file used for loading the data.
        dataframe (pd.DataFrame): Main DataFrame of bank transactions.
    """
    file_path: str
    dataframe: pd.DataFrame
    dataframe_header: pd.DataFrame

    def __init__(self, csv_path: str):
        """
        Initializes StatementManager by loading and cleaning the bank statement data from the specified CSV file.

        **Only handles KB bank file format.**
        Args:
            csv_path (str): The full path to the bank statement CSV file.
        """
        self.store_statements_first_time(csv_path)

    def _validate_input_file(self, file_path: str):
        """
        Validates existence of input file and checks if it is empty.

        Args:
            file_path (str): Full path to the file.
        """
        if not os.path.isfile(file_path):
            raise StatementFileNotFoundError(f"Statement file not found at path: {file_path}")

        # Input file should not be empty
        if os.stat(file_path).st_size == 0:
            raise StatementFileEmptyError(f"Empty statement file passed at path: {file_path}")

    def store_statements_first_time(self, csv_path: str):
        """
        Loads and cleans first bank statement data from the specified CSV file into pandas dataframe.

        Args:
            csv_path (str): The full path to the bank statement CSV file.
        """

        self._validate_input_file(csv_path)

        # TODO: The size of header should be separated into some sort of config variable.
        # Load data with minimal column set
        df = pd.read_csv(
            csv_path,
            encoding="cp1250",
            sep=';',
            header=16,
            usecols=[
                "Datum zauctovani",
                "Datum provedeni",
                "Protistrana",
                "Nazev protiuctu",
                "Castka",
                "Mena",
                "Originalni castka",
                "Originalni mena",
                "Smenny kurz",
                "VS",
                "KS",
                "SS",
                "Identifikace transakce",
                "Typ transakce",
                "Popis pro me",
                "Zprava pro prijemce",
                "Reference platby",
                "BIC / SWIFT",
                "Poplatek",
            ]
        )

        # Load additional data into separate dataframe
        self.dataframe_header = pd.read_csv(
            csv_path,
            encoding="cp1250",
            sep=';',
            nrows=16,
            header=None
        )

        # Normalize the KB bank column names into internal column names
        # NOTE: Maybe this could be separated into a "interface" to allow Pylint checking.
        norm_cols = {
            "Datum zauctovani": "posting_date",
            "Datum provedeni": "date", # TODO: This should be renamed to be more descriptive/not "collide" with posting_date.
            "Protistrana": "contra_account_number",
            "Nazev protiuctu": "contra_account_name",
            "Castka": "amount",
            "Mena": "currency",
            "Originalni castka": "original_amount",
            "Originalni mena": "original_currency",
            "Smenny kurz": "exchange_rate",
            "VS": "variable_symbol",
            "KS": "constant_symbol",
            "SS": "specific_symbol",
            "Identifikace transakce": "bank_transaction_id",
            "Typ transakce": "transaction_type",
            "Popis pro me": "description_for_me",
            "Zprava pro prijemce": "description_for_recipient",
            "Reference platby": "payment_reference",
            "BIC / SWIFT": "bic_or_swift",
            "Poplatek": "fee",
        }
        df = df.rename(columns=norm_cols)

        # Type cast date column to datetime
        df["date"] = pd.to_datetime(
            df["date"],
            format="%d.%m.%Y",
            )

        # Type cast amount column to numeric (floats)
        df["amount"] = df["amount"].replace(",", ".", regex=True)
        df["amount"] = pd.to_numeric(
            df["amount"],
        )

        # Sort rows by date
        df = df.sort_values(by="date", ascending=False)

        # Save "Base" dataframe for later use
        self.dataframe = df

    def store_statements(self, csv_path: str):
        """
        Loads, cleans and stores bank statement data to database from the specified CSV file.

        Args:
            csv_path (str): The full path to the bank statement CSV file.
        """

        self._validate_input_file(csv_path)
        self.store_statements_first_time(csv_path)

        # TODO: Outside of the need for making this code work with different csv formats, as of now the database does not take into account multiple users. Also, there should be a value validation.
        csv_account_number: str = str(self.dataframe_header.iat[3,1])

        db_account = select(Account).filter_by(account_number = csv_account_number)
        account_exists = db.session.scalar(db_account)

        if not account_exists:
            db_account = Account(
                name = "",
                bank_name = "",
                account_number = csv_account_number,
            )
            db.session.add(db_account)
        else:
            db_account = db.session.execute(db_account).scalar()


        for transaction in self.dataframe.itertuples(name="Transaction"):

            # Needs to be done since dataframe when broken into tuples does not keep track of item types -> this will be of type Timestamp, but there is no way for static analyzer to know that. Also we should exit if that is not the case.
            print(type(transaction.date))
            assert isinstance(transaction.date, Timestamp)

            transaction_date = transaction.date.to_pydatetime()
            transaction_amount = Decimal(pd.to_numeric(transaction.amount))

            currency_code = str(transaction.currency)
            db_currency = select(Currency).filter_by(code = currency_code)
            currency_exists = db.session.scalar(db_currency)

            if not currency_exists:
                db_currency = Currency(
                    name = "",
                    sign = "",
                    code = currency_code,
                )
                db.session.add(db_currency)
            else:
                db_currency = db.session.execute(db_currency).scalar()

            transaction_exists = db.session.scalar(select(Transaction).filter_by(
                amount = transaction.amount,
                date = transaction.date,
                contra_account_number = transaction.contra_account_number,
                contra_account_name = transaction.contra_account_name,

                account = db_account,
                currency = db_currency,
            ))

            if not transaction_exists and db_account and db_currency:
                new_transaction = Transaction(
                    amount = transaction_amount,
                    date = transaction_date,
                    contra_account_number = str(transaction.contra_account_number),
                    contra_account_name = str(transaction.contra_account_name),
                    my_description = str(transaction.description_for_me),
                    message = str(transaction.description_for_recipient),

                    account = db_account,
                    currency = db_currency
                )
                db.session.add(new_transaction)

        db.session.commit()

    def get_dataframe(self) -> pd.DataFrame:
        """
        Returns main DataFrame itself.

        **Original Dataframe returned - not a copy!**
        Returns:
            pd.DataFrame: Stored transaction DataFrame.
        """
        return self.dataframe
