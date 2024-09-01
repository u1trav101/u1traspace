from flask import session, redirect, url_for, request
from werkzeug import Response
from flask_wtf import FlaskForm
from web.overloads import render_template
from db import Query
import web.forms as forms
import profile
import messaging


def _post(user_id: int, post_id: int) -> Response | str | tuple:
    comment_form: FlaskForm = forms.input_form()
    delete_form: FlaskForm = forms.blank_form()

    if ("user_id") in session:
        if comment_form.validate_on_submit():
            messaging.send_blog_comment(
                session["user_id"], post_id, comment_form.corpus.data)
            
            return redirect(url_for("user.blog.post", user_id=user_id, post_id=post_id))

        elif delete_form.validate_on_submit():
            comment_id: str | None = request.form.get("value")
            
            if comment_id:
                try:
                    int(comment_id)
                except ValueError:
                    return redirect(url_for("user.blog.post", user=user_id, post_id=post_id))

                query = Query()
                comments: list[dict] = query.select_blog_comments(comment_id=int(comment_id), limit=1)
                if comments:
                    if (int(session["user_id"]) == user_id) or (int(session["user_id"]) == comments[0]["author_id"]):
                        query.delete_blog_comment(comment_id=int(comment_id))

            return redirect(url_for("user.blog.post", user_id=user_id, post_id=post_id))

    properties: dict = profile.get_profile_properties(user_id)
    template: str = "blog/post.html"
    match properties["layout"]:
        case "twitter":
            template = "twitter/blog/post.html"
        case "myspace":
            template = "myspace93/blog/post.html"

    return render_template(
        template,
        properties = properties,
        blogpost = profile.get_blogpost(user_id, post_id),
        blogposts = profile.get_all_user_blogposts(user_id),
        comments = profile.get_blogpost_comments(post_id),
        friends = profile.get_user_friends(user_id),
        is_friends = profile.is_friends(user_id),
        forms = {
            "comment": comment_form,
            "delete_post": delete_form,
            "friend": forms.forms.blank_form()
        }
    )
