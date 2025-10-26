import os
from datetime import date

import requests
import validators
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from flask import (
    Flask,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for,
)

from .database import DataBase
from .parser import parser
from .url_normalyzer import normalize_url

load_dotenv()

app = Flask(__name__)
app.logger.setLevel("INFO")
app.secret_key = os.getenv("SECRET_KEY")
db = DataBase(os.getenv("DATABASE_URL"))


@app.route("/")
def index():
    messages = get_flashed_messages()
    return render_template(
        "index.html",
        messages=messages
    )


@app.route("/urls", methods=["GET", "POST"])
def show_urls():
    messages = get_flashed_messages()
    if request.method == "GET":
        urls = db.get_all_urls()
        app.logger.info(urls)
        return render_template(
            "urls/urls.html",
            urls=urls,
            messages=messages
        )
    
    if request.method == "POST":
        url = request.form.get("url")
        if not url:
            return render_template(
                "index.html",
                error="URL не может быть пустым"
            ), 422

        if not validators.url(url):
            return render_template(
                "index.html",
                error="Некорректный URL"
            ), 422
        
        if db.url_exists(normalize_url(url)):
            existing_id = db.get_url_id_by_name(normalize_url(url))
            flash("Страница уже существует")
            return redirect(
                url_for("show_url",
                        url_id=existing_id
                )
            )
                
        url_id = db.add_new_url(normalize_url(url), date.today())
        flash("Страница успешно добавлена")
        return redirect(
            url_for(
                "show_url",
                url_id=url_id
            )
        )


@app.route("/urls/<int:url_id>")
def show_url(url_id):
    messages = get_flashed_messages()
    url = db.get_url_by_id(url_id)
    if not url:
        return render_template("urls/errors.html")
    
    checks = db.get_checks_by_url_id(url_id)
    return render_template(
        "urls/show.html",
        url=url,
        url_checks=checks,
        messages=messages
    )


@app.route("/urls/<int:url_id>/checks", methods=["POST"])
def new_verification_url(url_id):
    url = db.get_url_by_id(url_id)
    if not url:
        flash("URL не найден")
        return redirect(url_for("show_urls"))

    try:
        status_code, h1, title, description = parser(url)
    except Exception as e:
        app.logger.error(f"Ошибка проверки URL {url['name']}: {e}")
        return render_template("urls/show.html", url=url, 
                                   error="Произошла ошибка при проверке"), 422
    db.add_check(url_id, status_code, h1, title, description, date.today())
    flash("Страница успешно проверена")
    return redirect(url_for("show_url", url_id=url_id))


if __name__ == "__main__":
    app.run(debug=True)
