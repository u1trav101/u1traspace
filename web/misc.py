from flask import session, request
from flask import render_template as real_render_template
from datetime import datetime
from time import time
from config import CONFIG
from db import Query
from profile import get_notification_counters
import web.forms as forms
import re


# template render function to pass an argument to all routes
def render_template(*args, **kwargs):
    login_form = forms.login_form()

    return real_render_template(
        *args,
        **kwargs,
        cdn_uri=CONFIG.CDN_URI,
        login_form=login_form,
        current_time=round(time()),
        notification_counters=get_notification_counters(),
        time=unix_to_readable,
    )


# this function is executed on every request
# updates the 'lastseen' field in db for the user if they are logged in
def before_request():
    if ("user_id") in session:
        if "poll" not in request.path:
            query = Query()
            query.update_last_seen(session["user_id"])


# converts unix time to human readable time format
def unix_to_readable(time, short=False):
    readable_time = datetime.fromtimestamp(int(time)).strftime("%d/%m/%Y %H:%M:%S")

    if short:
        readable_time = datetime.fromtimestamp(int(time)).strftime("%H:%M:%S")

    if int(time) <= 0:
        return "never!"

    return readable_time


def regex_replace(s, find, replace):
    regex = re.compile(re.escape(find), re.IGNORECASE)

    return regex.sub(replace, s)
