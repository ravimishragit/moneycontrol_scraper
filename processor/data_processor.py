import pandas as pd
from datetime import datetime, timedelta


class DataProcessor:
    """
    Handles data processing tasks: filtering, grouping, and finding top recommendations.
    """

    def __init__(self, data: pd.DataFrame):
        self.data = data

    def filter_data(self):
        """ Filters the data for the last 3 months and only 'Buy' and 'Sell' recommendations """
        self.data['Reporting_Date'] = pd.to_datetime(self.data['Reporting_Date'])

        # Filter last 3 months
        three_months_ago = datetime.today() - timedelta(days=90)
        self.data = self.data[(self.data['Reporting_Date'] >= three_months_ago) &
                              (self.data['Recommendation'].isin(['Buy', 'Sell']))]

    def group_by_broker(self):
        """ Group data by Broker and find the top recommendation based on Profit Potential """
        top_recommendations = (
            self.data.sort_values(['Broker', 'Profit_Potential'], ascending=[True, False])
            .groupby('Broker')
            .first()
            .reset_index()
        )
        return top_recommendations

    def find_top_3(self, grouped_df: pd.DataFrame):
        """ Finds the Top 3 Companies and Brokers based on Profit Potential """
        top_companies = (
            self.data.sort_values('Profit_Potential', ascending=False)
            .head(3)[['Company', 'Profit_Potential']]
        )

        top_brokers = (
            grouped_df.sort_values('Profit_Potential', ascending=False)
            .head(3)[['Broker', 'Profit_Potential']]
        )

        return top_companies, top_brokers
