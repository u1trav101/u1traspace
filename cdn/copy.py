from boto3 import Session, session
from celery import shared_task
from config import CONFIG


sess: Session = session.Session()
client = sess.client(
    "s3",
    region_name=CONFIG.S3_REGION_NAME,
    endpoint_url=CONFIG.S3_ENDPOINT_NAME,
    aws_access_key_id=CONFIG.S3_ACCESS_ID,
    aws_secret_access_key=CONFIG.S3_SECRET_KEY
)

@shared_task
def copy_default_avatar(user_id: int) -> None:
    client.copy_object(
        CopySource=f"{CONFIG.S3_BUCKET_NAME}/u1traspace/usercontent/img/raw/default.webp",
        Bucket=CONFIG.S3_BUCKET_NAME,
        Key=f"u1traspace/usercontent/img/raw/{user_id}.webp",
        ACL="public-read",
        ContentType="image/gif"
    )
    for size in ["32px", "100px", "200px"]:
        client.copy_object(
            CopySource=f"{CONFIG.S3_BUCKET_NAME}/u1traspace/usercontent/img/rsz/{size}/default.webp",
            Bucket=CONFIG.S3_BUCKET_NAME,
            Key=f"u1traspace/usercontent/img/rsz/{size}/{user_id}.webp",
            ACL="public-read",
            ContentType="image/gif"
        )
