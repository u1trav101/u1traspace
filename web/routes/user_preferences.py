from flask import redirect, session, url_for, request
from werkzeug.utils import secure_filename
from db import Query
from web.misc import render_template
from config import CONFIG
import os
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
    res = query.select_users(user_id=session["user_id"], limit=1)[0]
    selected_interface = res["layout"]
    selected_privacy = res["private"]
    interfaces = {
        "u1traspace": 0,
        "myspace93": 1,
        "twitter": 2
    }
    preferences_form = forms.preferences_form(
        interface=interfaces[selected_interface],
        privacy=selected_privacy
    )

    if preferences_form.validate_on_submit():
        form_handler(query, preferences_form)

        return redirect(request.url)

    properties = profile.get_profile_properties(session["user_id"])
    properties.update({
        "css": profile.get_profile_css(session["user_id"])
    })

    avatar_uploading = False
    audio_uploading = False
    scheduled_tasks = tasks.get_scheduled_tasks()
    running_tasks = tasks.get_running_tasks()
    if scheduled_tasks:
        for task in scheduled_tasks:
            avatar_uploading = True if check_task(task, "image") is True else avatar_uploading
            audio_uploading = True if check_task(task, "audio") is True else avatar_uploading
    if running_tasks:
        for task in running_tasks:
            avatar_uploading = True if check_task(task, "image") is True else avatar_uploading
            audio_uploading = True if check_task(task, "audio") is True else avatar_uploading

    return render_template(
        "prefs.html",
        properties=properties,
        form=preferences_form,
        avatar_uploading=avatar_uploading,
        audio_uploading=audio_uploading
    )


def check_task(task, type):
    if task["name"] == "tasks.transcoding._transcode_and_upload_image" and type == "image":
        return True
    elif task["name"] == "tasks.transcoding.transcode_and_upload_audio" and type == "audio":
        return True

def form_handler(query, preferences_form):
    if len(preferences_form.bio.data) < 4096:
        # empty input uploads "" but must be None to properly update DB 
        preferences_form.bio.data = None if preferences_form.bio.data == "" else preferences_form.bio.data

        layouts = ["u1traspace", "myspace", "twitter"]
        query.update_user(
            session["user_id"],
            preferences_form.bio.data,
            layouts[int(preferences_form.interface.data)],
            preferences_form.privacy.data
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
