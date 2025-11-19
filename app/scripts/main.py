import pandas as pd
import matplotlib.pyplot as plt

from app.models.statement_manager import StatementManager

def main():

    # 1. Data Collection (Acquisition) & Data Cleaning (Preprocessing)
    loader = StatementManager("test_data/Vypis_354650030277_20240115_20250710.csv")
    data = loader.get_dataframe()

    # 2. Data Transformation (Structuring)
    # Group data by years and months
    month_groups = data.groupby([
        data["date"].dt.year.rename("year"), 
        data["date"].dt.month.rename("month"),
        ])

    # 3. Categorization (Labeling) & Exploratory Data Analysis (EDA)
    monthly_income = month_groups.apply(lambda x: x[x['amount'] > 0]['amount'].sum())
    monthly_expenses = month_groups.apply(lambda x: x[x['amount'] < 0]['amount'].sum())
    monthly_net = month_groups['amount'].sum()
    
    monthly_analysis_df = pd.DataFrame({
        'income': monthly_income,
        'expenses': monthly_expenses,
        'net': monthly_net,
        'transaction_count': month_groups['amount'].count()
    })

    # 4. Visualization, Reporting
    print("Monthly summary:")
    print(monthly_analysis_df)

    monthly_analysis_df.plot()
    plt.show()

if __name__ == "__main__":
    main()