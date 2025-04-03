import boto3
from datetime import datetime, timedelta
from config.settings import S3_BUCKET


def list_old_files(bucket, prefix, older_than_days=180):
    """List S3 files older than N days"""

    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)

    if 'Contents' not in response:
        return []

    old_files = []
    cutoff_date = datetime.now() - timedelta(days=older_than_days)

    for obj in response['Contents']:
        last_modified = obj['LastModified'].replace(tzinfo=None)
        if last_modified < cutoff_date:
            old_files.append(obj['Key'])

    return old_files


def cleanup_old_data():
    """Delete old files from S3 bucket"""

    prefix = "reports/"
    old_files = list_old_files(S3_BUCKET, prefix)

    s3 = boto3.client('s3')

    for file_key in old_files:
        s3.delete_object(Bucket=S3_BUCKET, Key=file_key)
        print(f"🗑️ Deleted: {file_key}")

    print("Cleanup completed successfully!")


if __name__ == "__main__":
    cleanup_old_data()
