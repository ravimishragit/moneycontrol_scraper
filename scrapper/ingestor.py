import pandas as pd

def ingest_mock_data(file_path: str) -> pd.DataFrame:
    """
    Ingest mock data from CSV into a DataFrame.
    Args:
        file_path (str): Path to the CSV file.
    Returns:
        pd.DataFrame: DataFrame containing mock data.
    """
    try:
        df = pd.read_csv(file_path)
        print(f"[INFO] Loaded {len(df)} records from mock data.")
        return df
    except Exception as e:
        print(f"[ERROR] Failed to load data: {e}")
        return pd.DataFrame()
