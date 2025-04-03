from utils.data_validator import DataValidator
from utils.datetime_helper import DateTimeHelper
from scraper.ingestor import ingest_mock_data
from processor.data_processor import DataProcessor
from reports.report_generator import generate_report
from scraper.scraper import save_mock_data_to_csv

# Constants
MOCK_DATA_FILE = "mock_data/mock_broker_data.csv"


def main():
    print("\n🔥 [INFO] Starting the data pipeline...")

    # Step 1: Generate and Save Mock Data (Optional)
    if not os.path.exists(MOCK_DATA_FILE):
        print("\n🚀 [INFO] Generating mock data...")
        save_mock_data_to_csv(MOCK_DATA_FILE, n=100)

    # Step 2: Ingest Mock Data
    print("\n📥 [INFO] Ingesting mock data...")
    df = ingest_mock_data(MOCK_DATA_FILE)

    # Data Validation
    if not DataValidator.validate_columns(df, ['Company', 'Broker', 'Profit_Potential', 'Recommendation']):
        print("\n [ERROR] Missing columns. Exiting.")
        return

    if not DataValidator.validate_non_empty(df):
        print("\n [ERROR] No data to process. Exiting.")
        return

    # Step 3: Data Processing
    processor = DataProcessor(df)

    filtered_df = processor.filter_last_3_months()
    buy_sell_df = processor.filter_by_recommendation(['Buy', 'Sell'])

    top_recommendations = processor.get_top_recommendations_by_broker()
    top_companies, top_brokers = processor.find_top_companies_and_brokers()

    # Step 4: Generate and Save Report
    generate_report(top_recommendations, top_companies, top_brokers, "mock_data/output_report.json")

    print("\n[SUCCESS] Data pipeline completed successfully!")


if __name__ == "__main__":
    main()
