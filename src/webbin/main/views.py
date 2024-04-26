from __future__ import annotations

import secrets
from datetime import datetime
from typing import Any

from flask import abort, current_app, flash, redirect, render_template, url_for

from webbin import db
from webbin.crypto import EncryptedPaste, RawPaste
from webbin.models import Paste

from . import main
from .forms import AcceptPasteForm, AskPasswordForm, RevealPasteForm


def _encrypt_data_from_form(form: AcceptPasteForm) -> EncryptedPaste:
    return RawPaste(form.paste_title.data, form.text.data).encrypt(
        form.password.data,
        current_app.config.get("COMPRESSION_THRESHOLD_SIZE"),
    )


@main.route("/", methods=["GET", "POST"])
def index() -> Any:
    form = AcceptPasteForm()
    if form.validate_on_submit():
        # get the paste-id/slug
        paste_id = form.paste_id.data
        # encrypt the data recieved from form
        secret_data = _encrypt_data_from_form(form)
        # get expires at value
        assert form.expires_after.data is not None
        expires_after = form.EXPIRES_AFTER[form.expires_after.data]
        # add the data to the database
        db.session.add(
            Paste(
                id=paste_id,
                title=secret_data.title,
                data=secret_data.data,
                is_compressed=secret_data.is_compressed,
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
    db_secret: Paste = db.get_or_404(Paste, paste_id)

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
            db_secret.is_compressed,
        )
        try:
            decrypted_paste = payload.decrypt(
                ask_password_form.password.data,
            )
        except ValueError:
            flash("Decryption failed! Incorrect password.", category="error")
            return redirect(url_for(".ask_password", paste_id=paste_id))

        # increase the view count
        db_secret.views = db_secret.views + 1

        # a burn after read paste: delete immediately
        if not db_secret.expires_after:
            flash(
                "Paste was created for your eyes only. When this paste is "
                "closed there will be no way to recover or view it again!",
                category="warning",
            )

            db.session.delete(db_secret)
        else:
            # update count if it is not a burn after read paste
            db.session.add(db_secret)

        db.session.commit()

        # build the reveal form and display the decrypted data
        reveal_form = RevealPasteForm()
        reveal_form.text.data = decrypted_paste.data
        return render_template(
            "reveal-secret.html",
            form=reveal_form,
            paste_title=decrypted_paste.title or "Untitled",
            paste_created_at=db_secret.created_at.isoformat(),
            views=db_secret.views,
        )

    return render_template(
        "ask-password.html",
        form=ask_password_form,
        paste_id=paste_id,
    )
