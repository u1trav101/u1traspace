from flask_wtf import FlaskForm
from wtforms import Field, ValidationError
from db import Query
from config import CONFIG


def email_not_taken(form: FlaskForm, field: Field) -> bool:
    query = Query()
    user: list = query.select_users(email=field.data, limit=1)

    if user:
        raise ValidationError(CONFIG.STRINGS["errors"]["validation"]["email_taken"])
    return True
