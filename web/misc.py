from flask import session, request
from flask import render_template as real_render_template
from datetime import datetime
from zoneinfo import ZoneInfo
from time import time

from config import CONFIG
from db import Query
import re


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


# this function is executed on every request
# updates the 'lastseen' field in db for the user if they are logged in
def before_request() -> None:
    if ("user_id") in session:
        if "poll" not in request.path:
            query = Query()
            query.update_last_seen(session["user_id"])


# converts unix time to human readable time format
def epoch_to_readable(time: datetime, short=False) -> str:
    strf: str = "%H:%M:%S" if short else "%d/%m/%Y %H:%M:%S"

    readable_time: str = datetime(
        time.year,
        time.month,
        time.day,
        time.hour,
        time.minute,
        time.second,
        time.microsecond,
        tzinfo=ZoneInfo(session["timezone"] if ("timezone") in session else "Etc/UTC")
    ).strftime(strf)

    return readable_time


def regex_replace(text: str, find: str, replace: str) -> str:
    regex: re.Pattern[str] = re.compile(re.escape(find), re.IGNORECASE)

    return regex.sub(repl=replace, string=text)
