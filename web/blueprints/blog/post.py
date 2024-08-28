from flask import session, redirect, url_for, request
from werkzeug import Response
from flask_wtf import FlaskForm
from web.overloads import render_template
from db import Query
import web.forms as forms
import profile
import messaging


def _post(user_id: int, post_id: int) -> Response | str | tuple:
    blogpost: dict | None = profile.get_blogpost(user_id, post_id)
    if not blogpost:
        return redirect(url_for("user.blog.browse", user_id=user_id))

    comment_form: FlaskForm = forms.comment_form()
    delete_form: FlaskForm = forms.comment_delete_form()
    friend_form: FlaskForm = forms.friend_form()

    if ("user_id") in session:
        if comment_form.validate_on_submit():
            messaging.send_blog_comment(
                session["user_id"], post_id, comment_form.corpus.data)

        elif delete_form.validate_on_submit():
            delete_value: str | None = request.form.get("delete")
            query = Query()

            if delete_value == "blog":
                query.delete_blogpost(user_id, post_id)

                return redirect(url_for("user.page", user_id=user_id))
            elif delete_value == "blog_comment":
                res: str = str(query.get_blog_comment_author(
                    user_id,
                    post_id,
                    delete_value
                ))

                if (session["user_id"] == user_id) or (session["user_id"] == res):
                    query.delete_blog_comment(post_id, delete_value)

                    return redirect(url_for(
                        "blog.post",
                        user_id=user_id,
                        post_id=post_id
                    ))
            else:
                return "Invalid value for field 'delete'", 400

        if request.method == "POST":
            return redirect(url_for("user.blog.post", user_id=user_id, post_id=post_id))

    properties: dict = profile.get_profile_properties(user_id)
    template: str = "blog/post.html"
    match properties["layout"]:
        case "twitter":
            template = "twitter/blogpost.html"
        case "classic":
            template = "classic/blogpost.html"
        case "myspace":
            template = "myspace/blogpost.html"

    return render_template(
        template,
        properties=properties,
        blogpost=blogpost,
        blogposts=profile.get_all_user_blogposts(user_id),
        comments=profile.get_blogpost_comments(post_id),
        friends=profile.get_user_friends(user_id),
        is_friends=profile.is_friends(user_id),
        comment_form=comment_form,
        delete_form=delete_form,
        friend_form=friend_form
    )
