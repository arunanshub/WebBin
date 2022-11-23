from __future__ import annotations

import secrets
from typing import Any

from flask import (
    current_app,
    flash,
    redirect,
    render_template,
    session,
    url_for,
)

from .. import db
from ..crypto import SecretData, decrypt_data, encrypt_data
from ..models import Secret
from . import main
from .forms import AskPasswordForm, DataForm, RevealForm


@main.route("/", methods=["GET", "POST"])
def index() -> Any:
    form = DataForm()
    if form.validate_on_submit():
        # get the paste-id/slug or generate one if not provided
        paste_id = form.paste_id.data
        # encrypt the user's secret data
        secret_data = encrypt_data(form.text.data, form.password.data)
        # add the data to the database
        secret = Secret(
            paste_id=paste_id,
            secret_data=secret_data.secret_data,
            nonce=secret_data.nonce,
            token=secret_data.token,
            salt=secret_data.salt,
        )
        db.session.add(secret)
        db.session.commit()
        flash("Your secret has been stored!")

        return redirect(url_for(".ask_password", paste_id=paste_id))

    # use a generated slug by default
    form.paste_id.data = secrets.token_urlsafe(
        current_app.config["DEFAULT_PASTE_ID_NUM_BYTES"]
    )
    return render_template("index.html", form=form)


@main.route("/<string:paste_id>/reveal")
def reveal_secret(paste_id: str) -> Any:
    form = RevealForm()
    try:
        secret_key = session["key"]
    except KeyError:
        return redirect(url_for(".ask_password", paste_id=paste_id))

    # get the encrypted data from the database
    db_secret: Secret = Secret.query.filter_by(
        paste_id=paste_id
    ).first_or_404()
    # build the encrypted data payload
    encrypted_data = SecretData(
        secret_data=db_secret.secret_data,
        nonce=db_secret.nonce,
        token=db_secret.token,
        salt=db_secret.salt,
    )

    # decrypt the data using the secret key from the query param
    try:
        decrypted_data = decrypt_data(encrypted_data, secret_key)
    except ValueError:
        # decryption failed
        flash("Decryption failed! Incorrect password.", category="error")
        return redirect(url_for(".ask_password", paste_id=paste_id))

    # put decrypted data in the form
    form.text.data = decrypted_data
    # delete the data from the database
    db.session.delete(db_secret)
    db.session.commit()
    return render_template("reveal-secret.html", form=form)


@main.route("/<string:paste_id>", methods=["GET", "POST"])
def ask_password(paste_id: str) -> Any:
    Secret.query.filter_by(paste_id=paste_id).first_or_404()
    form = AskPasswordForm()
    if form.validate_on_submit():
        session["key"] = form.password.data
        return redirect(
            url_for(
                ".reveal_secret",
                paste_id=paste_id,
            )
        )
    return render_template("ask-password.html", form=form)
