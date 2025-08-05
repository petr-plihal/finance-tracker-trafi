import pandas as pd

from csv_loader import csv_loader

def main():
    loader = csv_loader("Vypis_354650030277_20240401_20250401.csv")
    data = loader.get_dataframe()

if __name__ == "__main__":
    main()