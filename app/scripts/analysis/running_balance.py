# TODO: remove before merging
from app.scripts.analysis.tmp import StatementManager

# NOTE: keep
import pandas as pd
import plotly.express as px
# from app.exceptions import

# TODO: remove before merging
if __name__ == "__main__":
    manager = StatementManager("app/scripts/analysis/Vypis_354650030277_20250101_20251231.csv")
    df = manager.get_dataframe()

    # NOTE: keep
    print("Test")
    fig = px.line(df, x="date", y="amount", title='Title')
    fig.show()
