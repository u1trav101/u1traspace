from flask import session, request, redirect, url_for
from functools import wraps
from typing import Callable
from db import Query


# this function is executed on every request
# updates the 'lastseen' field in db for the user if they are logged in
def before_request() -> None:
    if ("user_id") in session:
        if "poll" not in request.path:
            query = Query()
            query.update_last_seen(session["user_id"])

# ensures that user_id and post_id are always int, and redirects if casting if not possible
def validate_url_vars(func: Callable) -> Callable:
    @wraps(func)
    def decorator(*args, **kwargs):
        if "user_id" in kwargs:
            try:
                kwargs["user_id"] = int(kwargs["user_id"])
            except ValueError:
                return redirect(url_for("user_list"))
        
        if "post_id" in kwargs:
            try:
                kwargs["post_id"] = int(kwargs["post_id"])
            except ValueError:
                return redirect(url_for("user.blog.browse", user_id=kwargs["user_id"]))
        
        return func(*args, **kwargs)
    
    return decorator