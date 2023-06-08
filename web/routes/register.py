from flask import redirect, request, session, url_for
from cdn import copy_default_avatar
from web.misc import render_template
import web.forms as forms
import auth


def register(captcha):
    if ("user_id") in session:
        return redirect(url_for("user_profile", user_id=session["user_id"]))

    register_form = forms.register_form()
    captcha_obj = captcha.create()

    if register_form.validate_on_submit():
        captcha_hash = request.form.get("captcha-hash")
        captcha_text = request.form.get("captcha-text")

        if captcha.verify(captcha_text, captcha_hash):
            # registration successful
            user_id = auth.register_user(register_form.username.data, register_form.password.data)

            copy_default_avatar.delay(user_id)

            return forms.register_commit(register_form.username.data, user_id)

    return render_template(
        "register.html",
        form=register_form,
        captcha=captcha_obj
    )