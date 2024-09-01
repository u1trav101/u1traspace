from flask import redirect, url_for
from flask_wtf import FlaskForm
from werkzeug import Response
from db import Query
from profile import get_profile_properties
from web.overloads import render_template
import web.forms as forms


def _new(user_id: int) -> Response | str:
    new_blog_form: FlaskForm = forms.new_blog_form()
    if new_blog_form.validate_on_submit():
        query = Query()
        query.insert_blog(user_id, new_blog_form.title.data, new_blog_form.corpus.data)
        blog_id: int = query.select_blogs(limit=1, author_id=user_id)[0]["blog_id"]

        return redirect(url_for("user.blog.post", user_id=user_id, post_id=blog_id))

    return render_template(
        "blog/new.html",
        new_blog_form = new_blog_form,
        properties = get_profile_properties(user_id),
        forms = {
            "new_blog": new_blog_form
        }
    )
