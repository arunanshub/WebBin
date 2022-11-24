from __future__ import annotations

import secrets
from typing import Any

from flask import current_app, flash, redirect, render_template, url_for

from .. import db
from ..crypto import SecretData, decrypt_data, encrypt_data
from ..models import Secret
from . import main
from .forms import AskPasswordForm, DataForm, RevealForm


@main.route("/", methods=["GET", "POST"])
def index() -> Any:
    form = DataForm()
    if form.validate_on_submit():
        # get the paste-id/slug
        paste_id = form.paste_id.data
        # encrypt the user's secret data
        secret_data = encrypt_data(form.text.data, form.password.data)
        # add the data to the database
        db.session.add(
            Secret(
                paste_id=paste_id,
                secret_data=secret_data.secret_data,
                nonce=secret_data.nonce,
                token=secret_data.token,
                salt=secret_data.salt,
            )
        )
        db.session.commit()
        flash("Your secret has been stored!")
        return redirect(url_for(".ask_password", paste_id=paste_id))

    # use a generated slug by default
    form.paste_id.data = secrets.token_urlsafe(
        current_app.config["DEFAULT_PASTE_ID_NUM_BYTES"]
    )
    return render_template("index.html", form=form)


@main.route("/<string:paste_id>", methods=["GET", "POST"])
def ask_password(paste_id: str) -> Any:
    """
    This route does two things at once. For "GET" requests, it asks for a
    password using a form. When you submit the form, it decrypts the data and
    displays it using another form.
    """
    # check if the paste exists in our database
    db_secret: Secret = Secret.query.filter_by(
        paste_id=paste_id
    ).first_or_404()

    # first ask for password
    ask_password_form = AskPasswordForm()
    if ask_password_form.validate_on_submit():
        # build payload and try to decrypt the data
        payload = SecretData(
            db_secret.secret_data,
            db_secret.nonce,
            db_secret.salt,
            db_secret.token,
        )
        try:
            decrypted_data = decrypt_data(
                payload,
                ask_password_form.password.data,
            )
        except ValueError:
            flash("Decryption failed! Incorrect password.", category="error")
            return redirect(url_for(".ask_password", paste_id=paste_id))

        # delete the paste since decryption is successful
        db.session.delete(db_secret)
        db.session.commit()

        # build the reveal form and display the decrypted data
        reveal_form = RevealForm()
        reveal_form.text.data = decrypted_data
        return render_template("reveal-secret.html", form=reveal_form)

    return render_template(
        "ask-password.html",
        form=ask_password_form,
        paste_id=paste_id,
    )
