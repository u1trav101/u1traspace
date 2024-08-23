from werkzeug import Response
from flask import redirect, session, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, EmailField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo


class login_form(FlaskForm):
    email: EmailField = EmailField("email", validators=[DataRequired(), Length(2, 100)])
    password: PasswordField = PasswordField("password", validators=[DataRequired(), Length(2, 30)])
    submit: SubmitField = SubmitField("login", validators=[DataRequired()])


class register_form(FlaskForm):
    email: EmailField = EmailField("email", validators=[DataRequired(), Length(2, 100)])
    username: StringField = StringField("username", validators=[DataRequired(), Length(2, 30)])
    password: PasswordField = PasswordField("password", validators=[DataRequired(), Length(2, 64)])
    confirm: PasswordField = PasswordField("confirm", validators=[DataRequired(), Length(2, 64), EqualTo("password")])
    submit: SubmitField = SubmitField("register", validators=[DataRequired()])


def register_commit(user_id: int) -> Response:
    session["user_id"] = user_id

    return redirect(url_for("user.page", user_id=user_id))


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
    privacy = BooleanField("private")
    submit = SubmitField("save", validators=[DataRequired()])


class new_blog_form(FlaskForm):
    title = StringField("title", validators=[DataRequired(), Length(1, 60)])
    corpus = TextAreaField("corpus", validators=[DataRequired(), Length(1, 4000)])
    submit = SubmitField("submit", validators=[DataRequired()])


class notification_action_form(FlaskForm):
    action = SubmitField("action", validators=[DataRequired()])


class friend_form(FlaskForm):
    friend = SubmitField("friend", validators=[DataRequired()])
