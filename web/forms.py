from flask import redirect, session
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, EmailField
from wtforms.validators import DataRequired, Length


class login_form(FlaskForm):
    email = EmailField("email", validators=[DataRequired(), Length(2, 100)])
    password = PasswordField("password", validators=[DataRequired(), Length(2, 30)])
    submit = SubmitField("submit", validators=[DataRequired()])


class register_form(FlaskForm):
    email = EmailField("email", validators=[DataRequired(), Length(2, 100)])
    username = StringField("username", validators=[DataRequired(), Length(2, 30)])
    password = PasswordField("password", validators=[DataRequired(), Length(2, 64)])
    submit = SubmitField("submit", validators=[DataRequired()])


def register_commit(username, user_id):
    print(f"u1traspace: User '{username}' created...")

    session["user_id"] = str(user_id)

    return redirect(f"/id/{user_id}")


class comment_form(FlaskForm):
    corpus = TextAreaField("corpus", validators=[DataRequired(), Length(1, 1024)])
    submit = SubmitField("submit", validators=[DataRequired()])


class comment_delete_form(FlaskForm):
    delete = SubmitField("delete", validators=[DataRequired()])


class message_form(FlaskForm):
    corpus = StringField("corpus", validators=[DataRequired(), Length(1, 1024)])
    submit = SubmitField("submit", validators=[DataRequired()])


class search_form(FlaskForm):
    corpus = StringField("corpus", validators=[DataRequired()])
    submit = SubmitField("search", validators=[DataRequired()])


class preferences_form(FlaskForm):
    avatar = FileField("avatar")
    audio = FileField("audio")
    css = TextAreaField("css")
    bio = TextAreaField("bio")
    interface = SelectField("interface", choices=[(0, "default"), (1, "twitter"), (2, "myspace"), (3, "classic")])
    privacy = SelectField("privacy", choices=[(0, "public"), (1, "private")])
    submit = SubmitField("submit", validators=[DataRequired()])


class new_blog_form(FlaskForm):
    title = StringField("title", validators=[DataRequired(), Length(1, 60)])
    corpus = TextAreaField("corpus", validators=[DataRequired(), Length(1, 4000)])
    submit = SubmitField("submit", validators=[DataRequired()])


class notification_action_form(FlaskForm):
    action = SubmitField("action", validators=[DataRequired()])


class friend_form(FlaskForm):
    friend = SubmitField("friend", validators=[DataRequired()])
