from flask import session, redirect, url_for


def konata():
    if ("konata") in session:
        session.pop("konata")
    else:
        session["konata"] = True

    return redirect(url_for("user_list"))
