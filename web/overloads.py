from flask import request, render_template as real_render_template
from wtforms.validators import (
    DataRequired as _DataRequired,
    Length as _Length,
    Email as _Email,
)
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


def DataRequired(name: str, *args, **kwargs) -> _DataRequired:
    return _DataRequired(
        message=CONFIG.STRINGS["errors"]["validation"]["missing_input"].format(name),
        *args,
        **kwargs,
    )


def Length(name: str, *args, **kwargs) -> _Length:
    return _Length(
        message=CONFIG.STRINGS["errors"]["validation"]["bad_length"].format(
            name, args[0], args[1]
        ),
        min=args[0],
        max=args[1],
        **kwargs,
    )


def Email(*args, **kwargs) -> _Email:
    return _Email(
        message=CONFIG.STRINGS["errors"]["validation"]["invalid_email"], *args, **kwargs
    )
