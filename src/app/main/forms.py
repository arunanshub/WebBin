from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Regexp


class DataForm(FlaskForm):
    text = TextAreaField(
        "Data To Hide",
        validators=[DataRequired()],
        render_kw={"rows": 11},
        description="What secrets do you want to hide?",
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()],
        description="Password to protect your retarded secrets.",
    )
    paste_id = StringField(
        "Slug/Paste ID",
        validators=[
            Length(min=1, max=32),
            DataRequired(),
            Regexp(
                r"^\S+$",
                message="No whitespace allowed in slug!",
            ),
        ],
        description="Slug or ID for the data. Edit me if you want a "
        "custom slug.",
    )
    submit = SubmitField("Hide!")


class RevealForm(FlaskForm):
    text = TextAreaField(
        "Secret message",
        render_kw={"readonly": True, "rows": 11},
    )


class AskPasswordForm(FlaskForm):
    password = PasswordField(
        "Password",
        description="This password decrypts the secret message",
        validators=[DataRequired()],
    )
    submit = SubmitField("Unlock the secret!")
