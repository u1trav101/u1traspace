from config import CONFIG
import magic


mime = magic.Magic(mime=True)


def upload(client, file_path: str, destination: str) -> None:
    mime_type = mime.from_file(file_path)
    if mime_type == "text/plain":
        mime_type = "text/css"

    client.upload_file(
        file_path,
        CONFIG.S3_BUCKET_NAME,
        destination,
        ExtraArgs={"ACL": "public-read", "ContentType": mime_type},
    )
