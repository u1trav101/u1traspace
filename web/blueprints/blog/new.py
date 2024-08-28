from flask import session, redirect, url_for
from flask_wtf import FlaskForm
from werkzeug import Response
from db import Query
from profile import get_profile_properties
from web.overloads import render_template
from web.forms import new_blog_form


def _new(user_id: int) -> Response | str:
    if int(session["user_id"]) != int(user_id):
        return redirect(url_for("user.page", user_id=user_id))

    form: FlaskForm = new_blog_form()
    if form.validate_on_submit():
        query = Query()
        query.insert_blog(user_id, form.title.data, form.corpus.data)
        blog_id: int = query.select_blogs(limit=1, author_id=user_id)[0]["blog_id"]

        return redirect(url_for("user.blog.post", user_id=user_id, post_id=blog_id))

    return render_template(
        "blog/new.html",
        form=form,
        properties=get_profile_properties(user_id)
    )
