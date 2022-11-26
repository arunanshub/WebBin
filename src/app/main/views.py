from __future__ import annotations

import secrets
from datetime import datetime
from typing import Any

from flask import abort, current_app, flash, redirect, render_template, url_for

from .. import db
from ..crypto import EncryptedPaste, RawPaste, decrypt_paste, encrypt_paste
from ..models import Paste
from . import main
from .forms import AcceptPasteForm, AskPasswordForm, RevealPasteForm


@main.route("/", methods=["GET", "POST"])
def index() -> Any:
    form = AcceptPasteForm()
    if form.validate_on_submit():
        # get the paste-id/slug
        paste_id = form.paste_id.data
        # encrypt the user's secret data
        secret_data = encrypt_paste(
            RawPaste(form.paste_title.data, form.text.data),
            form.password.data,
        )
        # get expires at value
        assert form.expires_after.data is not None
        expires_after = form.EXPIRES_AFTER[form.expires_after.data]
        # add the data to the database
        db.session.add(
            Paste(
                id=paste_id,
                title=secret_data.title,
                data=secret_data.secret_data,
                nonce=secret_data.nonce,
                token=secret_data.token,
                salt=secret_data.salt,
                expires_after=expires_after,
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
    db_secret: Paste = Paste.query.filter_by(id=paste_id).first_or_404()

    # check whether the requested paste has already expired
    if db_secret.expires_after and (
        datetime.utcnow() > db_secret.created_at + db_secret.expires_after
    ):
        db.session.delete(db_secret)
        db.session.commit()
        abort(404)

    # first ask for password
    ask_password_form = AskPasswordForm()
    if ask_password_form.validate_on_submit():
        # build payload and try to decrypt the data
        payload = EncryptedPaste(
            db_secret.title,
            db_secret.data,
            db_secret.nonce,
            db_secret.salt,
            db_secret.token,
        )
        try:
            decrypted_paste = decrypt_paste(
                payload,
                ask_password_form.password.data,
            )
        except ValueError:
            flash("Decryption failed! Incorrect password.", category="error")
            return redirect(url_for(".ask_password", paste_id=paste_id))

        # a burn after read paste: delete immediately
        if not db_secret.expires_after:
            db.session.delete(db_secret)
            db.session.commit()

        # build the reveal form and display the decrypted data
        reveal_form = RevealPasteForm()
        reveal_form.text.label.text = decrypted_paste.title
        reveal_form.text.data = decrypted_paste.paste
        return render_template("reveal-secret.html", form=reveal_form)

    return render_template(
        "ask-password.html",
        form=ask_password_form,
        paste_id=paste_id,
    )
