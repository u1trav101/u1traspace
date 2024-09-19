from config import CONFIG
import magic
import log

mime = magic.Magic(mime=True)


def upload(client, file_path: str, destination: str) -> None:
    log.write(__name__, f"{file_path} uploading to cdn at {destination}...")

    mime_type = mime.from_file(file_path)
    if mime_type == "text/plain":
        mime_type = "text/css"

    client.upload_file(
        file_path,
        CONFIG.S3_BUCKET_NAME,
        destination,
        ExtraArgs={"ACL": "public-read", "ContentType": mime_type},
    )

    log.write(__name__, f"{file_path} uploading to cdn at {destination}... DONE")
