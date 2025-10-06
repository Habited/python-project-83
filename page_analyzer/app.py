import os

import validators
from dotenv import load_dotenv
from flask import Flask, flash, redirect,render_template, request, url_for, get_flashed_messages
from datetime import date
from .tools import DataBase

load_dotenv()

app = Flask(__name__)

app.logger.setLevel("INFO")
app.secret_key = os.getenv("SECRET_KEY")
db = DataBase(os.getenv("DATABASE_URL"))


@app.route("/")
def index():
    messages = get_flashed_messages()
    return render_template("index.html", messages=messages)


@app.route("/urls", methods=["GET"])
def show_urls():
    urls = db.get_table_urls()
    return render_template("urls.html", urls=urls)


@app.route("/urls", methods=["POST"])
def new_url():
    url = request.form.get("url")
    today = date.today()
    valid_url = validators.url(url)
    if not valid_url:
        flash("Некорректный URL")
        return redirect("/", code=302)
    elif url in [url["name"] for url in db.get_all_urls()]:
        flash("Страница уже существует")
        return redirect("/", code=302)        
    db.add_new_url(url, today)
    flash("Корректный URL")
    return redirect(url_for("show_url", 
                            url_id=db.get_url_id()))


@app.route("/urls/<int:url_id>")
def show_url(url_id):
    url = db.get_url(url_id)
    app.logger.info(f"{url}")
    messages = get_flashed_messages()
    return render_template("urls/new.html", url=url, messages=messages)


@app.route("/urls/<int:url_id>/checks")
def show_the_verification_status(url_id):
    id = db.get_url_id()
    url = db.get_url(id)
    messages = get_flashed_messages()
    return render_template("urls/checks.html", url=url, messages=messages)


@app.route("/urls/checks", methods=["POST"])
def new_ferification_url():
    id = db.get_url_id()
    url = db.get_url(id)
    valid_url = True
    if not valid_url:
        flash("Проверка не пройдена")
        return redirect("/status", code=302)    
    flash("Страница успешно проверена")
    return redirect(url_for("show_the_verification_status", url_id=db.get_url_id()))


@app.route("/status")
def show_status():
    render_template()

if __name__ == "__main__":
    app.run(debug=True)
