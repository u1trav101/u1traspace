from flask import session, redirect, url_for
from web.misc import render_template

def message_list():
    if ("user_id") not in session:
        return redirect(url_for("login"))

    return render_template("messagelist.html")