import pandas as pd

class DataValidator:
    """
    A class to perform data validation checks on broker recommendation data.
    """

    @staticmethod
    def validate_columns(df: pd.DataFrame, required_columns: list) -> bool:
        """
        Validates that all required columns are present in the DataFrame.

        Args:
            df (pd.DataFrame): DataFrame containing broker recommendations.
            required_columns (list): List of required column names.

        Returns:
            bool: True if all columns are present, False otherwise.
        """
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            print(f" [ERROR] Missing columns: {missing_columns}")
            return False
        return True

    @staticmethod
    def validate_non_empty(df: pd.DataFrame) -> bool:
        """
        Validates that the DataFrame is not empty.

        Args:
            df (pd.DataFrame): DataFrame to validate.

        Returns:
            bool: True if the DataFrame contains data, False otherwise.
        """
        if df.empty:
            print(" [ERROR] DataFrame is empty.")
            return False
        return True

    @staticmethod
    def validate_numeric_columns(df: pd.DataFrame, numeric_cols: list) -> bool:
        """
        Validates that specified columns contain only numeric values.

        Args:
            df (pd.DataFrame): DataFrame containing broker recommendations.
            numeric_cols (list): List of numeric column names to validate.

        Returns:
            bool: True if all columns contain numeric values, False otherwise.
        """
        for col in numeric_cols:
            if not pd.api.types.is_numeric_dtype(df[col]):
                print(f" [ERROR] Column '{col}' contains non-numeric values.")
                return False
        return True
