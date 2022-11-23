from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class DataForm(FlaskForm):
    text = TextAreaField("Data To Hide", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    paste_id = StringField(
        "Custom Slug",
        validators=[Length(max=64)],
        description="Custom Slug or ID for the data. Leave it blank if you "
        "want me to provide one for you.",
    )
    submit = SubmitField("Hide!")


class RevealForm(FlaskForm):
    text = TextAreaField("Secret message", render_kw={"readonly": True})


class AskPasswordForm(FlaskForm):
    password = PasswordField(
        "Password",
        description="This password decrypts the secret message",
        validators=[DataRequired()],
    )
    submit = SubmitField()
