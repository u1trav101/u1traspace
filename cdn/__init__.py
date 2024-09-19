from boto3 import Session, session
from cdn.upload import upload as _upload
from cdn.info import ls as _ls
from config import CONFIG


def _setup():
    sess: Session = session.Session()
    client = sess.client(
        "s3",
        region_name=CONFIG.S3_REGION_NAME,
        endpoint_url=CONFIG.S3_ENDPOINT_NAME,
        aws_access_key_id=CONFIG.S3_ACCESS_ID,
        aws_secret_access_key=CONFIG.S3_SECRET_KEY,
    )

    return client


def upload(*args, **kwargs) -> None:
    _upload(_setup(), *args, **kwargs)


def ls(*args, **kwargs) -> list:
    return _ls(_setup(), *args, **kwargs)
