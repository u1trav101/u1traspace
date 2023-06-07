from flask import request, escape
from db.search import search as search_db
from web.misc import render_template
from web.forms import search_form
from config import CONFIG
import re


RE_COMBINE_WHITESPACE = re.compile(r"\s+")


def search():
    form = search_form()

    if request.method == "GET":
        return render_template(
            "search.html",
            form=form,
            results=None,
            search_term=None,
            search_terms=None
        )

    results = None
    corpus = request.form.get("corpus")
    if request.form.get("corpus").replace(" ", "") not in CONFIG.BLACKLISTED_SEARCHES:
        results = search_db(corpus)

    search_term = escape(corpus)

    search_terms = RE_COMBINE_WHITESPACE.sub(" ", corpus).strip().split(" ")
    for i in range(len(search_terms)):
        search_terms[i] = escape(search_terms[i])

    return render_template(
        "search.html",
        form=form,
        results=results,
        search_term=search_term,
        search_terms=search_terms
    )
