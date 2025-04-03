import pandas as pd

def generate_report(top_companies: pd.DataFrame, top_brokers: pd.DataFrame):
    """
    Generates and prints a report of the top 3 companies and brokers.
    """
    print("\n🔥 Top 3 Companies by Profit Potential 🔥")
    print(top_companies.to_string(index=False))

    print("\n🔥 Top 3 Brokers by Profit Potential 🔥")
    print(top_brokers.to_string(index=False))
