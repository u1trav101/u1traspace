from urllib import request
from urllib.error import HTTPError


def get_image_size(url: str) -> int:
    try:
        req: request.Request = request.Request(url, method="HEAD")
        file = request.urlopen(req)
        size = file.headers["content-length"]
        return int(size)
    except HTTPError:
        return 0
