from __future__ import annotations

from datetime import timedelta

from flask_wtf import FlaskForm
from wtforms import (
    Field,
    PasswordField,
    SelectField,
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
    expires_at = SelectField(
        "Expire the paste after",
        choices=[
            (timedelta(), "Burn After Read"),
            (timedelta(hours=1), "1 hour"),
            (timedelta(hours=2), "2 hours"),
            (timedelta(days=1), "1 day"),
            (timedelta(weeks=1), "1 week"),
        ],
        description="When should I remove the paste from the database?",
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
        validators=[DataRequired(), Length(min=3)],
    )
    submit = SubmitField("Unlock the secret!")
