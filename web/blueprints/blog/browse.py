from flask import redirect, session, url_for, request
from werkzeug import Response
from db import Query
from web.overloads import render_template
from web.forms import blank_form
import profile


def _browse(user_id: int) -> Response | str:
    post_delete_form = blank_form()

    if ("user_id") in session:
        if post_delete_form.validate_on_submit():
            blog_id: str | None = request.form.get("delete")
            
            if blog_id:
                try:
                    int(blog_id)
                except ValueError:
                    return redirect(url_for("user.blog.browse", user_id=user_id))
                
                query = Query()
                blogs: list[dict] = query.select_blogs(blog_id=int(blog_id))
                if blogs:
                    if (int(session["user_id"] == user_id)) or (int(session["user_id"]) == blogs[0]["author_id"]):
                        query.delete_blog(blog_id=int(blog_id))
            
            return redirect(url_for("user.blog.browse", user_id=user_id))

    return render_template(
        "blog/browse.html",
        properties = profile.get_profile_properties(user_id),
        blogposts = profile.get_all_user_blogposts(user_id),
        friends = profile.get_user_friends(user_id),
        is_friends = profile.is_friends(user_id),
        forms = {
            "friend": blank_form(),
            "delete_post": post_delete_form
        }
    )
