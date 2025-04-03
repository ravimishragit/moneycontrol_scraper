from datetime import datetime, timedelta

class DateTimeHelper:
    """
    A helper class for date operations.
    """

    @staticmethod
    def get_current_date() -> str:
        """
        Returns the current date in YYYY-MM-DD format.

        Returns:
            str: Current date string.
        """
        return datetime.today().strftime('%Y-%m-%d')

    @staticmethod
    def get_date_n_months_ago(n: int) -> str:
        """
        Returns the date N months ago in YYYY-MM-DD format.

        Args:
            n (int): Number of months to go back.

        Returns:
            str: Date string in YYYY-MM-DD format.
        """
        date_n_months_ago = datetime.today() - timedelta(days=n * 30)
        return date_n_months_ago.strftime('%Y-%m-%d')

    @staticmethod
    def is_within_last_n_months(date_str: str, n: int) -> bool:
        """
        Checks if the given date is within the last N months.

        Args:
            date_str (str): Date in YYYY-MM-DD format.
            n (int): Number of months to check.

        Returns:
            bool: True if the date is within the last N months, False otherwise.
        """
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            date_n_months_ago = datetime.today() - timedelta(days=n * 30)
            return date_obj >= date_n_months_ago
        except ValueError:
            print(f" [ERROR] Invalid date format: {date_str}")
            return False
