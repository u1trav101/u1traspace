from flask import redirect, session, url_for
from werkzeug.utils import secure_filename
from random import randint
from db import Query
from web.misc import render_template
from config import CONFIG
import os
import pylibmagic
import magic
import web.forms as forms
import profile
import tasks


dir_name = os.path.dirname(__file__)
temp_dir = os.path.join(dir_name, "../../.tmp/")
usercontent_dir = os.path.join(dir_name, "../../usercontent/")


def user_preferences():
    if ("user_id") not in session:
        return redirect(url_for("login"))

    query = Query()
    res = query.get_interface_and_privacy(session["user_id"])
    selected_interface = res["interface"]
    selected_privacy = int.from_bytes(res["private"], "big")
    interfaces = {
        "default": 0,
        "twitter": 1,
        "myspace": 2,
        "classic": 3
    }
    preferences_form = forms.preferences_form(
        interface=interfaces[selected_interface],
        privacy=selected_privacy
    )

    if preferences_form.validate_on_submit():
        form_handler(query, preferences_form)

        return redirect(f"/id/{session['user_id']}?i={randint(1,1000)}")

    properties = profile.get_profile_properties(session["user_id"])
    properties.update({
        "css": profile.get_profile_css(session["user_id"])
    })

    return render_template(
        "prefs.html",
        properties=properties,
        form=preferences_form
    )


def form_handler(query, preferences_form):
    if len(preferences_form.bio.data) < 4096:
        query.update_user_preferences(
            session["user_id"],
            preferences_form.bio.data,
            [
                "default",
                "twitter",
                "myspace",
                "classic"
            ][int(preferences_form.interface.data)],
            int(preferences_form.privacy.data)
        )

    avatar = preferences_form.avatar.data
    if avatar:
        file_extension = os.path.splitext(secure_filename(avatar.filename))[-1]
        if file_extension in CONFIG.ALLOWED_IMAGE_UPLOAD_EXTENSIONS:

            file_name = f"img/{session['user_id'] + file_extension}"
            file_path = os.path.join(temp_dir, file_name)
            avatar.save(file_path)

            if magic.from_file(file_path, mime=True) in CONFIG.ALLOWED_IMAGE_MIME_TYPES:
                tasks.transcode_and_upload_images.delay(
                    file_path,
                    usercontent_dir,
                    session["user_id"]
                )

    audio = preferences_form.audio.data
    if audio:
        file_extension = os.path.splitext(secure_filename(audio.filename))[-1]
        if file_extension in CONFIG.ALLOWED_AUDIO_UPLOAD_EXTENSIONS:

            file_name = f"audio/{session['user_id'] + file_extension}"
            file_path = os.path.join(temp_dir, file_name)
            audio.save(file_path)

            if magic.from_file(file_path, mime=True) in CONFIG.ALLOWED_AUDIO_MIME_TYPES:
                tasks.transcode_and_upload_audio.delay(
                    file_path,
                    usercontent_dir,
                    session["user_id"]
                )

    css = preferences_form.css.data
    if css:
        tasks.save_css.delay(
            css,
            usercontent_dir,
            session["user_id"]
        )
