from config import CONFIG


def ls(client, prefix: str, delimiter: str = "/") -> list:
    res = client.list_objects(
        Bucket=CONFIG.S3_BUCKET_NAME, Prefix=prefix, Delimiter=delimiter
    )

    return res
