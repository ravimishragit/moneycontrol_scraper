import json
import pytest
import boto3
from unittest.mock import patch, MagicMock
from apis.lambda_handler import lambda_handler
from config import AWS_BUCKET_NAME

@pytest.fixture
def mock_event():
    """Mock API Gateway Event"""
    return {
        "httpMethod": "GET",
        "path": "/broker-recommendation",
        "queryStringParameters": {}
    }

@pytest.fixture
def mock_context():
    """Mock Lambda Context"""
    class MockContext:
        function_name = "broker-recommendation-lambda"
        memory_limit_in_mb = 512
        invoked_function_arn = f"arn:aws:lambda:ap-south-1:123456789012:function:broker-recommendation-lambda"
        aws_request_id = "test-request-id"
    return MockContext()

@patch("apis.lambda_handler.ingest_mock_data")
@patch("apis.lambda_handler.DataProcessor")
@patch("apis.lambda_handler.generate_report")
@patch("apis.lambda_handler.s3_client.upload_file")
def test_lambda_handler_success(mock_upload, mock_report, mock_processor, mock_ingest, mock_event, mock_context):
    """
    Test case: Lambda function execution should be successful.
    """

    # Mock Data Processing
    mock_ingest.return_value = MagicMock()  # Simulate DataFrame return
    mock_processor.return_value.filter_last_3_months.return_value = MagicMock()
    mock_processor.return_value.filter_by_recommendation.return_value = MagicMock()
    mock_processor.return_value.get_top_recommendations_by_broker.return_value = {
        "ICICI Securities": {"Company": "TCS", "Profit %": 15.2}
    }
    mock_processor.return_value.find_top_companies_and_brokers.return_value = (
        ["TCS", "Reliance", "Infosys"],
        ["ICICI Securities", "HDFC Securities", "Kotak Securities"]
    )

    # Mock report generation
    mock_report.return_value = None

    # Mock S3 Upload
    mock_upload.return_value = None

    # Execute Lambda
    response = lambda_handler(mock_event, mock_context)

    # Assertions
    assert response["statusCode"] == 200
    response_body = json.loads(response["body"])
    assert "Report generated and saved to S3 successfully!" in response_body["message"]
    assert response_body["top_companies"] == ["TCS", "Reliance", "Infosys"]
    assert response_body["top_brokers"] == ["ICICI Securities", "HDFC Securities", "Kotak Securities"]
    assert f"s3://{AWS_BUCKET_NAME}/broker_reports/" in response_body["s3_report_path"]

@patch("apis.lambda_handler.ingest_mock_data")
def test_lambda_handler_failure(mock_ingest, mock_event, mock_context):
    """
     Test case: Lambda function should return 500 error on failure.
    """

    # Simulate ingestion failure
    mock_ingest.side_effect = Exception("Mock Ingestion Failure")

    # Execute Lambda
    response = lambda_handler(mock_event, mock_context)

    # Assertions
    assert response["statusCode"] == 500
    response_body = json.loads(response["body"])
    assert "error" in response_body
    assert "Mock Ingestion Failure" in response_body["error"]
