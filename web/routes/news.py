from flask import request, session, redirect, url_for
from werkzeug import Response
from web.overloads import render_template
from db import Query


def news() -> Response | str:
    query = Query()
    blogs: list[dict] | None = None

    if request.args.get("show") == "friends":
        if ("user_id") not in session:
            return redirect(url_for("news"))
        
        blogs = query.get_all_friend_blogposts(session["user_id"], 20)
    else:
        blogs = query.get_all_blogposts(20)
    
    return render_template(
        "news.html",
        new_posts=blogs
    )