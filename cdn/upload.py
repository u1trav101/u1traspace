from boto3 import Session, session
from config import CONFIG


sess: Session = session.Session()
client = sess.client(
    "s3",
    region_name=CONFIG.S3_REGION_NAME,
    endpoint_url=CONFIG.S3_ENDPOINT_NAME,
    aws_access_key_id=CONFIG.S3_ACCESS_ID,
    aws_secret_access_key=CONFIG.S3_SECRET_KEY
)


def upload_image(file_path: str, destination: str) -> None:
    client.upload_file(
        file_path,
        CONFIG.S3_BUCKET_NAME,
        destination
    )


def upload_audio(file_path: str, destination: str) -> None:
    client.upload_file(
        file_path,
        CONFIG.S3_BUCKET_NAME,
        destination
    )


def upload_css(file_path: str, destination: str) -> None:
    client.upload_file(
        file_path,
        CONFIG.S3_BUCKET_NAME,
        destination
    )
