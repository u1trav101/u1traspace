from flask import session, request

# Get timezone from the browser and store it in the session object.
def set_timezone():
    timezone = request.data.decode("utf-8")
    session["timezone"] = timezone
    return ""