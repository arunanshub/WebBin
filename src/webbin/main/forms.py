from __future__ import annotations

from collections import OrderedDict
from datetime import timedelta

from flask_wtf import FlaskForm  # type: ignore[import-untyped]
from wtforms import (
    Field,
    Form,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
    ValidationError,
)
from wtforms.validators import (
    DataRequired,
    Length,
    Regexp,
)

from webbin import db
from webbin.models import Paste


class UniquePasteID:
    def __init__(self, message: str | None = None) -> None:
        self._message = message or "The Paste ID '{id}' is already in use."

    def __call__(self, _: Form, field: Field) -> None:
        if db.session.get(Paste, field.data):
            raise ValidationError(self._message.format(id=field.data))


class AcceptPasteForm(FlaskForm):
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
            DataRequired(),
            Length(min=1, max=32),
            Regexp(
                r"^[a-zA-Z0-9-_]+$",
                message="No whitespace or special characters allowed in paste"
                " ID!",
            ),
            UniquePasteID(),
        ],
        description="Slug or ID for the data. Edit me if you want a "
        "custom slug.",
    )

    EXPIRES_AFTER = OrderedDict(
        {
            "Burn After Read": timedelta(),
            "10 minutes": timedelta(minutes=10),
            "1 hour": timedelta(hours=1),
            "1 day": timedelta(days=1),
            "1 week": timedelta(weeks=1),
            "2 weeks": timedelta(weeks=2),
            "1 month": timedelta(days=30),
            "6 months": timedelta(days=30 * 6),
            "1 year": timedelta(days=365),
        }
    )
    expires_after = SelectField(
        "Expire the paste after",
        choices=list(EXPIRES_AFTER),
        description="When should I remove the paste from the database?",
    )

    paste_title = StringField(
        "Paste Title",
        validators=[Length(max=100)],
        description="The paste title that will be displayed over the data.",
    )

    submit = SubmitField("Hide!")


class RevealPasteForm(FlaskForm):
    text = TextAreaField("", render_kw={"readonly": True, "rows": 11})


class AskPasswordForm(FlaskForm):
    password = PasswordField(
        "Password",
        description="This password decrypts the secret message",
        validators=[DataRequired(), Length(min=3)],
    )
    submit = SubmitField("Unlock the secret!")
