from flask import redirect, request, url_for
from markupsafe import escape
from werkzeug import Response
from flask_wtf import FlaskForm
from db.search import search as search_db
from web.overloads import render_template
from web.forms import input_form
from config import CONFIG
import re


RE_COMBINE_WHITESPACE = re.compile(r"\s+")


def search() -> Response | str | tuple:
    search_form: FlaskForm = input_form()

    if request.method == "GET":
        return render_template(
            "search.html",
            results=None,
            search_term=None,
            search_terms=None,
            forms={"search": search_form},
        )

    corpus: str | None = search_form.corpus.data
    if not corpus:
        return redirect(url_for("search"))

    results: dict[str, list] | None = None
    if corpus.replace(" ", "") not in CONFIG.BLACKLISTED_SEARCHES:
        results = search_db(corpus)

    search_term = escape(corpus)
    search_terms = RE_COMBINE_WHITESPACE.sub(" ", corpus).strip().split(" ")
    for i in range(len(search_terms)):
        search_terms[i] = escape(search_terms[i])

    return render_template(
        "search.html",
        results=results,
        search_term=search_term,
        search_terms=search_terms,
        forms={"search": search_form},
    )
