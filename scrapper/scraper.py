import pandas as pd
import random
from datetime import datetime, timedelta

BROKERS = ['ICICI Securities', 'HDFC Securities', 'Kotak Securities',
           'Motilal Oswal', 'Axis Securities', 'Reliance Securities']

COMPANIES = ['Tata Motors', 'Reliance Industries', 'HDFC Bank', 'Infosys',
             'Wipro', 'Bajaj Finance', 'Maruti Suzuki', 'Larsen & Toubro',
             'TCS', 'Hindustan Unilever']

RECOMMENDATIONS = ['Buy', 'Sell']


def generate_mock_data(n: int = 50) -> pd.DataFrame:
    """
    Generates mock broker recommendation data.

    Args:
        n (int): Number of records to generate (default 50)

    Returns:
        pd.DataFrame: Mock broker data
    """
    data = []

    for _ in range(n):
        broker = random.choice(BROKERS)
        company = random.choice(COMPANIES)

        # Random reporting date within last 6 months
        reporting_date = datetime.today() - timedelta(days=random.randint(1, 180))

        recommendation = random.choice(RECOMMENDATIONS)
        profit_potential = round(random.uniform(-20, 50), 2)  # % profit potential

        data.append({
            "Broker": broker,
            "Company": company,
            "Reporting_Date": reporting_date.strftime('%Y-%m-%d'),
            "Recommendation": recommendation,
            "Profit_Potential": profit_potential
        })

    df = pd.DataFrame(data)
    return df


def save_mock_data_to_csv(file_path: str, n: int = 50):
    """
    Saves the mock data to a CSV file.

    Args:
        file_path (str): Path to save the CSV file.
        n (int): Number of records to generate.
    """
    df = generate_mock_data(n)
    df.to_csv(file_path, index=False)
    print(f"[INFO] Mock data saved to {file_path}")


if __name__ == "__main__":
    # Generate 100 mock records and save to CSV
    save_mock_data_to_csv("mock_data/mock_broker_data.csv", n=100)
