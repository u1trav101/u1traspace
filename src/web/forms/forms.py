from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    TextAreaField,
    SelectField,
    EmailField,
    BooleanField,
)
from wtforms.validators import EqualTo
from web.overloads import DataRequired, Length, Email
from web.forms.validators import email_not_taken
from config import CONFIG


class login_form(FlaskForm):
    email: EmailField = EmailField(
        "email", validators=[DataRequired("email"), Length("email", 2, 100), Email()]
    )
    password: PasswordField = PasswordField(
        "password", validators=[DataRequired("password"), Length("password", 2, 30)]
    )
    submit: SubmitField = SubmitField("submit")


class register_form(FlaskForm):
    email: EmailField = EmailField(
        "email",
        validators=[
            DataRequired("email"),
            Length("length", 2, 100),
            Email(),
            email_not_taken,
        ],
    )
    username: StringField = StringField(
        "username", validators=[DataRequired("username"), Length("username", 2, 30)]
    )
    password: PasswordField = PasswordField(
        "password", validators=[DataRequired("password"), Length("password", 2, 64)]
    )
    confirm: PasswordField = PasswordField(
        "confirm",
        validators=[
            DataRequired("password confirmation"),
            Length("password confirmation", 2, 64),
            EqualTo(
                "password",
                message=CONFIG.STRINGS["errors"]["validation"]["password_mismatch"],
            ),
        ],
    )
    submit: SubmitField = SubmitField("submit")


class preferences_form(FlaskForm):
    avatar = FileField("avatar")
    audio = FileField("audio")
    css = TextAreaField("css")
    bio = TextAreaField("bio")
    interface = SelectField(
        "interface", choices=[(0, "default"), (1, "twitter"), (2, "myspace")]
    )
    privacy = BooleanField("private")
    submit = SubmitField("save")


class new_blog_form(FlaskForm):
    title = StringField(
        "title", validators=[DataRequired("title"), Length("title", 1, 60)]
    )
    corpus = TextAreaField(
        "corpus", validators=[DataRequired("corpus"), Length("corpus", 1, 4000)]
    )
    submit = SubmitField("submit")


def input_form(textarea: bool = False) -> FlaskForm:
    if textarea:
        return _textarea_input_form()
    return _string_input_form()


class _string_input_form(FlaskForm):
    corpus = StringField(
        "corpus", validators=[DataRequired("corpus"), Length("corpus", 1, 1024)]
    )
    submit = SubmitField("submit")


class _textarea_input_form(FlaskForm):
    corpus = TextAreaField(
        "corpus", validators=[DataRequired("corpus"), Length("corpus", 1, 1024)]
    )
    submit = SubmitField("submit")


class blank_form(FlaskForm):
    value = SubmitField("value")
