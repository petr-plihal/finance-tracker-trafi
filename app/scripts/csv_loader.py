import pandas as pd

class csv_loader:

    file_path: str
    dataframe: pd.DataFrame

    def __init__(self, csv_path: str):

        # Load data with minimal column set
        self.dataframe = pd.read_csv(
            csv_path,
            sep=';', 
            header=16,
            usecols=[
                "Datum provedeni",
                "Nazev protiuctu",
                "Castka",
                "Identifikace transakce" # TODO: Is this really unique?
            ]
        )

        # Convert columns to appropriate types

        self.dataframe["Datum provedeni"] = pd.to_datetime(
            self.dataframe["Datum provedeni"],
            format="%d.%m.%Y",
            )
        
        self.dataframe["Castka"] = self.dataframe["Castka"].replace(",", ".", regex=True)

        self.dataframe["Castka"] = pd.to_numeric(
            self.dataframe["Castka"],
        )

    def get_dataframe(self) -> pd.DataFrame:
        return self.dataframe