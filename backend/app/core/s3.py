import os
import boto3

S3_ENDPOINT = os.environ.get("S3_ENDPOINT", "http://minio:9000")
S3_ACCESS_KEY = os.environ.get("S3_ACCESS_KEY", "minioadmin")
S3_SECRET_KEY = os.environ.get("S3_SECRET_KEY", "minioadmin123")
S3_BUCKET = os.environ.get("S3_BUCKET", "assets")
S3_REGION = os.environ.get("S3_REGION", "us-east-1")

s3_client = boto3.client(
    "s3",
    endpoint_url=S3_ENDPOINT,
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY,
    region_name=S3_REGION,
    config=boto3.session.Config(signature_version="s3v4"),
)


def create_presigned_upload_url(key: str, expires_in: int = 3600) -> str:
    return s3_client.generate_presigned_url(
        "put_object",
        Params={"Bucket": S3_BUCKET, "Key": key},
        ExpiresIn=expires_in,
    )


def create_presigned_download_url(key: str, expires_in: int = 3600) -> str:
    return s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": S3_BUCKET, "Key": key},
        ExpiresIn=expires_in,
    )
