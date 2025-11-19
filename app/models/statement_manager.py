import pandas as pd

class StatementManager:

    file_path: str
    dataframe: pd.DataFrame

    def __init__(self, csv_path: str):

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
        return self.dataframe