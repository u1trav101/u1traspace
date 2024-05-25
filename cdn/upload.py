from boto3 import session
from config import CONFIG


session = session.Session()
client = session.client(
    "s3",
    region_name=CONFIG.S3_REGION_NAME,
    endpoint_url=CONFIG.S3_ENDPOINT_NAME,
    aws_access_key_id=CONFIG.S3_ACCESS_ID,
    aws_secret_access_key=CONFIG.S3_SECRET_KEY
)


def upload_image(file_path, destination):
    client.upload_file(
        file_path,
        CONFIG.S3_ACCESS_ID,
        destination,
        ExtraArgs={
            "ACL": "public-read",
            "ContentType": "image/gif"
        }
    )


def upload_audio(file_path, destination):
    client.upload_file(
        file_path,
        CONFIG.S3_ACCESS_ID,
        destination,
        ExtraArgs={
            "ACL": "public-read",
            "ContentType": "audio/mpeg"
        }
    )


def upload_css(file_path, destination):
    client.upload_file(
        file_path,
        CONFIG.S3_ACCESS_ID,
        destination,
        ExtraArgs={
            "ACL": "public-read",
            "ContentType": "text/css"
        }
    )
