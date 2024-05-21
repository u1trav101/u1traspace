from web.misc import render_template
import web.forms as forms
from db import Query


def index():
    query = Query()
    res = query.select_blogs(limit=6)

    search_form = forms.search_form()

    return render_template(
        "index.html",
        new_posts=res,
        form=search_form
    )
