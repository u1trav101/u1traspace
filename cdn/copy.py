from boto3 import session
from celery import shared_task
from config import CONFIG


session = session.Session()
client = session.client(
    "s3",
    region_name=CONFIG.S3_REGION_NAME,
    endpoint_url=CONFIG.S3_ENDPOINT_NAME,
    aws_access_key_id=CONFIG.S3_ACCESS_ID,
    aws_secret_access_key=CONFIG.S3_SECRET_KEY
)

@shared_task
def copy_default_avatar(user_id):
    client.copy_object(
        CopySource=f"{CONFIG.S3_ACCESS_ID}/usercontent/img/raw/default.gif",
        Bucket=CONFIG.S3_ACCESS_ID,
        Key=f"usercontent/img/raw/{user_id}.gif",
        ACL="public-read",
        ContentType="image/gif"
    )
    for size in ["32px", "100px", "200px"]:
        client.copy_object(
            CopySource=f"{CONFIG.S3_ACCESS_ID}/usercontent/img/rsz/{size}/default.gif",
            Bucket=CONFIG.S3_ACCESS_ID,
            Key=f"usercontent/img/rsz/{size}/{user_id}.gif",
            ACL="public-read",
            ContentType="image/gif"
        )
