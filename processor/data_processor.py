import pandas as pd
from datetime import datetime, timedelta


class DataProcessor:
    """
    Handles data processing tasks: filtering, grouping, and finding top recommendations.
    """

    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()  # Avoid mutating original input

    def filter_last_3_months(self) -> pd.DataFrame:
        """Filter data from the last 3 months based on 'Reporting_Date'"""
        self.data['Reporting_Date'] = pd.to_datetime(self.data['Reporting_Date'])
        three_months_ago = datetime.today() - timedelta(days=90)
        filtered = self.data[self.data['Reporting_Date'] >= three_months_ago]
        return filtered

    def filter_by_recommendation(self, recommendations: list) -> pd.DataFrame:
        """Filter data by given recommendation types (e.g., Buy, Sell)"""
        filtered = self.data[self.data['Recommendation'].isin(recommendations)]
        return filtered

    def get_top_recommendations_by_broker(self) -> pd.DataFrame:
        """
        Group data by Broker and return the top recommendation based on Profit Potential.
        """
        top_recommendations = (
            self.data.sort_values(['Broker', 'Profit_Potential'], ascending=[True, False])
            .groupby('Broker')
            .first()
            .reset_index()
        )
        return top_recommendations

    def find_top_companies_and_brokers(self) -> tuple:
        """
        Finds the Top 3 Companies and Brokers based on Profit Potential.
        Returns:
            top_companies (DataFrame), top_brokers (DataFrame)
        """
        top_companies = (
            self.data.sort_values('Profit_Potential', ascending=False)
            .head(3)[['Company', 'Profit_Potential']]
        )

        broker_grouped = self.get_top_recommendations_by_broker()
        top_brokers = (
            broker_grouped.sort_values('Profit_Potential', ascending=False)
            .head(3)[['Broker', 'Profit_Potential']]
        )

        return top_companies, top_brokers
