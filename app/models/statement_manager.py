import pandas as pd

class StatementManager:
    """
    Manages the bank statement DataFrame, handling the initial loading, cleaning, and persistent storage of the main dataset.

    Attributes:
        file_path (str): The path to the CSV file used for loading the data.
        dataframe (pd.DataFrame): Main DataFrame of bank transactions.
    """
    file_path: str
    dataframe: pd.DataFrame

    def __init__(self, csv_path: str):
        """
        Initializes StatementManager by loading and cleaning the bank statement data from the specified CSV file.

        **Only handles KB bank file format.**
        Args:
            csv_path (str): The full path to the bank statement CSV file.
        """

        # Load data with minimal column set
        df = pd.read_csv(
            csv_path,
            encoding="cp1250", # TODO: 
            sep=';', 
            header=16,
            usecols=[
                "Datum provedeni",
                "Nazev protiuctu",
                "Castka",
                "Identifikace transakce" # TODO: Is this really unique?
            ]
        )

        # Normalize the KB bank column names into internal column names
        norm_cols = {
            "Datum provedeni": "date",
            "Nazev protiuctu": "contra_account_name",
            "Castka": "amount",
            "Identifikace transakce": "transaction_id"
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

    def get_dataframe(self) -> pd.DataFrame:
        """
        Returns main DataFrame itself.

        **Original Dataframe returned - not a copy!**
        Returns:
            pd.DataFrame: Stored transaction DataFrame.
        """
        return self.dataframe