from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import (
    Field,
    PasswordField,
    StringField,
    SubmitField,
    TextAreaField,
    ValidationError,
)
from wtforms.validators import DataRequired, Length, Regexp

from app.models import Secret


class DataForm(FlaskForm):
    text = TextAreaField(
        "Data To Hide",
        validators=[DataRequired()],
        render_kw={"rows": 11},
        description="What secrets do you want to hide?",
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=3)],
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

    def validate_paste_id(self, field: Field) -> None:
        if Secret.query.filter_by(paste_id=field.data).first():
            raise ValidationError("The Paste ID is already in use.")


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
