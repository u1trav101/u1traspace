from web.overloads import render_template


def rules() -> str:
    return render_template("rules.html")
