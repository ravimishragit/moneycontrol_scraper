import json
import os
import boto3
from datetime import datetime
from scraper.ingestor import ingest_mock_data
from processor.data_processor import DataProcessor
from reports.report_generator import generate_report
from utils.logger import setup_logger
from config import AWS_BUCKET_NAME, AWS_REGION

# Initialize logger
logger = setup_logger()

# AWS S3 client
s3_client = boto3.client('s3', region_name=AWS_REGION)

# File Paths
MOCK_DATA_FILE = "mock_data/mock_broker_data.csv"
REPORT_FILE = "/tmp/output_report.json"

def save_to_s3(file_path, bucket_name, object_name):
    """
    Saves a local file to an S3 bucket.

    Args:
        file_path (str): Local path of the file.
        bucket_name (str): S3 bucket name.
        object_name (str): S3 object key.
    """
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        logger.info(f"[SUCCESS] File saved to S3: {bucket_name}/{object_name}")
    except Exception as e:
        logger.error(f"[ERROR] Failed to upload to S3: {str(e)}")
        raise

def lambda_handler(event, context):
    """
    AWS Lambda entry point.

    Args:
        event: Incoming request event data.
        context: Lambda execution context.

    Returns:
        dict: HTTP response with report summary.
    """
    logger.info("🔥 [INFO] Lambda function invoked...")

    try:
        # Step 1: Load Mock Data
        logger.info("📥 [INFO] Ingesting mock data...")
        df = ingest_mock_data(MOCK_DATA_FILE)

        # Step 2: Data Processing
        processor = DataProcessor(df)

        logger.info("⚙️ [INFO] Filtering last 3 months and recommendations...")
        filtered_df = processor.filter_last_3_months()
        buy_sell_df = processor.filter_by_recommendation(['Buy', 'Sell'])

        top_recommendations = processor.get_top_recommendations_by_broker()
        top_companies, top_brokers = processor.find_top_companies_and_brokers()

        # Step 3: Generate and Save Report Locally
        logger.info("📊 [INFO] Generating report...")
        generate_report(top_recommendations, top_companies, top_brokers, REPORT_FILE)

        # Step 4: Save Report to S3 with timestamp
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        s3_object_key = f"broker_reports/report_{timestamp}.json"

        logger.info("☁️ [INFO] Uploading report to S3...")
        save_to_s3(REPORT_FILE, AWS_BUCKET_NAME, s3_object_key)

        # Prepare response
        response = {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Report generated and saved to S3 successfully!",
                "s3_report_path": f"s3://{AWS_BUCKET_NAME}/{s3_object_key}",
                "top_companies": top_companies,
                "top_brokers": top_brokers
            })
        }

        logger.info("[SUCCESS] Lambda function executed successfully!")
        return response

    except Exception as e:
        logger.error(f" [ERROR] Lambda execution failed: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }
