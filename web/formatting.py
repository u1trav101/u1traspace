from flask import session
from datetime import datetime
from zoneinfo import ZoneInfo
import re


# converts unix time to human readable time format
def epoch_to_readable(time: datetime, short=False, obj=False) -> str:
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
    )

    if obj:
        return readable_time
    return readable_time.strftime(strf)

# escapes characters with potential for XSS (e.g. 'javascript:')
def regex_replace(text: str, find: str, replace: str) -> str:
    regex: re.Pattern[str] = re.compile(re.escape(find), re.IGNORECASE)

    return regex.sub(repl=replace, string=text)
