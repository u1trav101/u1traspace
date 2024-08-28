from web.overloads import render_template

def faq() -> str:
    return render_template("faq.html")