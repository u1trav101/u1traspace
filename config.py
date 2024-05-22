from bitwarden_sdk import BitwardenClient, DeviceType, client_settings_from_dict
import os

client = BitwardenClient(
    client_settings_from_dict(
        {
            "apiUrl": os.getenv("API-URL", "https://api.bitwarden.com"),
            "deviceType": DeviceType.SDK,
            "identityURL": os.getenv("IDENTITY-URL", "https://identity.bitwarden.com/connect/token"),
            "userAgent": "Python"
        }
    )
)

organisation_id = os.getenv("ORGANISATION_ID")
client.access_token_login(open(".bitwarden-access-token", "r").readline())


class CONFIG:
    DEBUG = True
    PORT = 5000

    MARIADB_HOST = "127.0.0.1"
    MARIADB_PORT = 3306
    MARIADB_USER = "backend"
    MARIADB_PASSWORD = client.secrets().get("bf0630d0-d130-479c-b8c4-b173001c9148").data.value
    MARIADB_ROOT_PASSWORD = client.secrets().get("e653a440-6388-4406-bd72-b17101589fe1").data.value
    MARIADB_DATABASE = "u1traspace"
    SELECT_LIMIT = 999

    CDN_URI = "https://cdn.u1trav101.net/u1traspace"
    INSECURE_CDN_URI = "http://cdn.u1trav101.net/ultraspace"

    MAX_CONTENT_LENGTH = 8 * 1000 * 1000

    SECRET_KEY = client.secrets().get("04d85160-cad6-42e6-9e4f-b17501735703").data.value
    CAPTCHA_CONFIG = {"SECRET_CSRF_KEY": SECRET_KEY}

    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 300

    S3_ACCESS_ID = "u1trav101cdn"
    S3_SECRET_KEY = client.secrets().get("e447c57f-6f12-4be6-bf02-b17501870a12").data.value
    S3_REGION_NAME = "eu-north-1"
    S3_ENDPOINT_NAME = "http://127.0.0.1:8080"

    CELERY = dict(
        broker_url="redis://127.0.0.1:6379/0",
        result_backend="redis://127.0.0.1:6379/1",
        task_ignore_result=True,
    )

    BLACKLISTED_SEARCHES = [
        "and"
    ]

    ALLOWED_IMAGE_UPLOAD_EXTENSIONS = [
        ".gif",
        ".png",
        ".jpg",
        ".jpeg",
        ".webp"
    ]
    ALLOWED_IMAGE_MIME_TYPES = [
        "image/gif",
        "image/jpeg",
        "image/png",
        "image/apng",
        "image/webp"
    ]
    ALLOWED_AUDIO_UPLOAD_EXTENSIONS = [
        ".mp3",
        ".ogg",
        ".m4a",
        ".xm"
    ]
    ALLOWED_AUDIO_MIME_TYPES = [
        "audio/mp3",
        "audio/mpeg",
        "audio/ogg",
        "audio/mp4",
        "audio/x-mod"
    ]