import boto3
from botocore.exceptions import NoCredentialsError


def upload_to_s3(bucket, key, data):
    """Upload data to S3"""
    s3 = boto3.client('s3')

    try:
        s3.put_object(Bucket=bucket, Key=key, Body=data)
        print(f"Data uploaded to S3: {bucket}/{key}")
    except NoCredentialsError:
        print("AWS credentials not found.")
