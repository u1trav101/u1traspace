from flask import redirect, session, url_for, request
from werkzeug import Response
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from db import Query
from web.overloads import render_template
from config import CONFIG
import os
import magic
import web.forms as forms
import profile
import tasks


DIR_NAME: str = os.path.dirname(__file__)
TEMP_DIR: str = os.path.join(DIR_NAME, "/tmp/u1traspace")
USERCONTENT_DIR: str = os.path.join(DIR_NAME, "../../usercontent/")


def preferences() -> Response | str:
    query = Query()
    res: dict = query.select_users(user_id=session["user_id"], limit=1)[0]
    selected_interface: str = res["layout"]
    selected_privacy: str = res["private"]
    interfaces = {
        "u1traspace": 0,
        "myspace93": 1,
        "twitter": 2
    }
    preferences_form: FlaskForm = forms.preferences_form(
        interface=interfaces[selected_interface],
        privacy=selected_privacy
    )

    if preferences_form.validate_on_submit():
        form_handler(query, preferences_form)

        return redirect(request.url)

    properties: dict = profile.get_profile_properties(session["user_id"])
    properties.update({
        "css": profile.get_profile_css(session["user_id"])
    })

    avatar_uploading: bool = False
    audio_uploading: bool = False
    scheduled_tasks: list | None = tasks.get_scheduled_tasks()
    running_tasks: list | None = tasks.get_running_tasks()
    if scheduled_tasks:
        for task in scheduled_tasks:
            avatar_uploading = True if check_task(task, "image") is True else avatar_uploading
            audio_uploading = True if check_task(task, "audio") is True else avatar_uploading
    if running_tasks:
        for task in running_tasks:
            avatar_uploading = True if check_task(task, "image") is True else avatar_uploading
            audio_uploading = True if check_task(task, "audio") is True else avatar_uploading

    return render_template(
        "preferences.html",
        properties = properties,
        avatar_uploading = avatar_uploading,
        audio_uploading = audio_uploading,
        forms = {
            "preferences": preferences_form
        }
    )


def check_task(task: dict, type: str) -> bool:
    if task["name"] == "tasks.transcoding._transcode_and_upload_image" and type == "image":
        return True
    elif task["name"] == "tasks.transcoding.transcode_and_upload_audio" and type == "audio":
        return True
    
    return False

def form_handler(query: Query, preferences_form: FlaskForm) -> None:
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
        file_extension: str = os.path.splitext(secure_filename(avatar.filename))[-1]
        if file_extension in CONFIG.ALLOWED_IMAGE_UPLOAD_EXTENSIONS:

            file_name: str = f"{str(session['user_id']) + file_extension}"
            file_path: str = os.path.join(TEMP_DIR, file_name)
            avatar.save(file_path)

            if magic.from_file(file_path, mime=True) in CONFIG.ALLOWED_IMAGE_MIME_TYPES:
                tasks.transcode_and_upload_images.delay(
                    file_path,
                    USERCONTENT_DIR,
                    session["user_id"]
                )

    audio = preferences_form.audio.data
    if audio:
        file_extension: str = os.path.splitext(secure_filename(audio.filename))[-1]
        if file_extension in CONFIG.ALLOWED_AUDIO_UPLOAD_EXTENSIONS:

            file_name: str = f"{str(session['user_id']) + file_extension}"
            file_path: str = os.path.join(TEMP_DIR, file_name)
            audio.save(file_path)

            if magic.from_file(file_path, mime=True) in CONFIG.ALLOWED_AUDIO_MIME_TYPES:
                tasks.transcode_and_upload_audio.delay(
                    file_path,
                    USERCONTENT_DIR,
                    session["user_id"]
                )

    css = preferences_form.css.data
    if css:
        tasks.save_css.delay(
            css,
            USERCONTENT_DIR,
            session["user_id"]
        )
