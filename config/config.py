from bitwarden_sdk import BitwardenClient, DeviceType, client_settings_from_dict
from yaml import safe_load
from pathlib import Path
import os


client: BitwardenClient = BitwardenClient(
    client_settings_from_dict(
        {
            "apiUrl": os.getenv("API-URL", "https://api.bitwarden.com"),
            "deviceType": DeviceType.SDK,
            "identityURL": os.getenv("IDENTITY-URL", "https://identity.bitwarden.com/connect/token"),
            "userAgent": "Python"
        }
    )
)

client.access_token_login(open(".bitwarden-access-token", "r").readline().strip())


class CONFIG:
    VERSION: str = "1.0.4"

    DEBUG: bool = True
    PORT: int = 5000
    NUM_OF_PROXIES: int = 1

    MARIADB_HOST: str = "127.0.0.1"
    MARIADB_PORT: int = 3306
    MARIADB_USER: str = "u1traspace"
    MARIADB_PASSWORD: str = client.secrets().get("bf0630d0-d130-479c-b8c4-b173001c9148").data.value
    MARIADB_ROOT_PASSWORD: str = client.secrets().get("e653a440-6388-4406-bd72-b17101589fe1").data.value
    MARIADB_DATABASE: str = "u1traspace"
    SELECT_LIMIT: int = 999

    REDIS_BROKER_URL: str = "redis://127.0.0.1:6379/0"
    REDIS_RESULT_URL: str = "redis://127.0.0.1:6379/1" 

    CDN_URI: str = "https://cdn.u1trav101.net/u1traspace"
    INSECURE_CDN_URI: str = "http://cdn.u1trav101.net/ultraspace"

    MAX_CONTENT_LENGTH: int = 8 * 1000 * 1000 #  bytes

    SECRET_KEY: str = client.secrets().get("04d85160-cad6-42e6-9e4f-b17501735703").data.value
    CAPTCHA_CONFIG: dict[str, str] = {"SECRET_CSRF_KEY": SECRET_KEY}

    SOCK_SERVER_OPTIONS: dict[str, int] = {
        "max_message_size":  512000, # bytes
        "ping_interval": 25 # seconds (s)
    }

    CACHE_TYPE: str = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT: int = 300 # seconds

    S3_ACCESS_ID: str = client.secrets().get("fa54bc8d-5d1f-43dc-9139-b17f002037ad").data.value
    S3_SECRET_KEY: str = client.secrets().get("e447c57f-6f12-4be6-bf02-b17501870a12").data.value
    S3_REGION_NAME: str = "eu-west-2"
    S3_ENDPOINT_NAME: str | None = None
    S3_BUCKET_NAME: str = "u1trav101"

    CELERY: dict[str, str | bool] = dict(
        broker_url=REDIS_BROKER_URL,
        result_backend=REDIS_RESULT_URL,
        task_ignore_result=True,
    )

    USERS_PER_PAGE = 20
    
    STRINGS: dict = safe_load(Path("config/strings.yml").read_text())
    BLACKLISTED_SEARCHES: list[str] = safe_load(Path("config/search-blacklist.yml").read_text())
    ALLOWED_IMAGE_UPLOAD_EXTENSIONS: list[str] = safe_load(Path("config/img-ext-whitelist.yml").read_text())
    ALLOWED_IMAGE_MIME_TYPES: list[str] = safe_load(Path("config/img-mime-whitelist.yml").read_text())
    ALLOWED_AUDIO_UPLOAD_EXTENSIONS: list[str] = safe_load(Path("config/audio-ext-whitelist.yml").read_text())
    ALLOWED_AUDIO_MIME_TYPES: list[str] = safe_load(Path("config/audio-mime-whitelist.yml").read_text())
