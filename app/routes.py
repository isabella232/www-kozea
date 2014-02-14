from . import app
from flask import render_template


@app.route("/")
def index():
    return render_template('index.jinja2')


@app.route("/<string:path>")
def catch_all(path):
    return render_template('index.jinja2', path=path)
