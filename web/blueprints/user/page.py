from flask import session, redirect, url_for, request
from werkzeug import Response
from flask_wtf import FlaskForm
from db import Query
from web.overloads import render_template
import web.forms as forms
import profile
import messaging


def _page(user_id: int) -> Response | str | tuple:
    comment_form: FlaskForm = forms.comment_form()
    delete_form: FlaskForm = forms.comment_delete_form()
    friend_form: FlaskForm = forms.friend_form()
    query = Query()

    if ("user_id") in session:
        if comment_form.validate_on_submit():
            messaging.send_profile_comment(
                int(session["user_id"]),
                user_id,
                comment_form.corpus.data
            )

        elif delete_form.validate_on_submit():
            res: str | None = request.form.get("delete")
            if not res:
                return "Invalid value for field 'delete'", 400

            comment_id: int = int(res)
            comment: dict = query.select_page_comments(comment_id=int(res))[0]

            if (int(session["user_id"]) == user_id) or (int(session["user_id"]) == comment["author_id"]):
                query.delete_page_comment(comment_id=comment_id, limit=1)

                return redirect(url_for("user.page", user_id=user_id))

        if request.method == "POST":
            return redirect(url_for("user.page", user_id=user_id))


    query.increase_page_views(user_id)

    properties: dict = profile.get_profile_properties(user_id)
    template: str = "user/page.html"
    match properties["layout"]:
        case "twitter":
            template = "twitter/user/page.html"
        case "myspace":
            template = "myspace93/user/page.html"

    return render_template(
        template,
        properties=properties,
        comments=profile.get_profile_comments(user_id),
        blogposts=profile.get_all_user_blogposts(user_id),
        friends=profile.get_user_friends(user_id),
        is_friends=profile.is_friends(user_id),
        comment_form=comment_form,
        delete_form=delete_form,
        friend_form=friend_form
    )
