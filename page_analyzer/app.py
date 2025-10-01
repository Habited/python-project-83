import os
import validators
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, flash, url_for
from validators.domain import domain
from .tools import DataBase


load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")
db = DataBase(os.getenv("DATABASE_URL"))

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/urls", methods=["GET"])
def show_urls():
    urls = db.get_all_urls()
    return render_template("urls.html", urls=urls)


@app.route("/urls", methods=["POST"])
def new_url():
    url = request.form.get("url")
    valid_url = validators.url(url)
    if not valid_url:
        flash("Некорректный URL")
        return redirect("/", code=302)
    elif url in db.get_url(db.get_url_id()):
        flash("Такой URL уже есть")
        return redirect("/", code=302)        
    db.add_new_url(url)
    flash("Корректный URL")
    return redirect(url_for("show_url", url_id=db.get_url_id()))


@app.route("/urls/<int:url_id>")
def show_url(url_id):
    urls = db.get_url(url_id)
    print(urls)
    return render_template("urls/new.html", urls=urls)


if __name__ == "__main__":
    app.run(debug=True)
