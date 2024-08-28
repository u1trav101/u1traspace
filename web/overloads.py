from flask import request, render_template as real_render_template
from time import time
from config import CONFIG
from web.formatting import epoch_to_readable


# template render function to pass an argument to all routes
def render_template(*args, **kwargs) -> str:
    CDN_URI: str = CONFIG.CDN_URI
    if request.headers.get("X-HTTP-Legacy") == "true":
        CDN_URI: str = CONFIG.INSECURE_CDN_URI

    return real_render_template(
        *args,
        **kwargs,
        cdn_uri=CDN_URI,
        current_time=round(time()),
        time=epoch_to_readable,
    )