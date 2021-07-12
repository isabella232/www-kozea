from flask import Flask, render_template
from sassutils.wsgi import SassMiddleware


def create_app():
    app = Flask(__name__)

    app.wsgi_app = SassMiddleware(
        app.wsgi_app,
        {"www_kozea": ("static/sass", "static/css", "/static/css", False)},
    )

    page_list = [
        "à-propos",
        "backoffice",
        "community",
        "contact",
        "groupement",
        "kozea-media",
        "livres-blancs",
        "lost",
        "newsletter",
        "nous-rejoindre",
        "pharminfo",
        "promomaker",
        "ressources",
        "solutions",
        "témoignages",
    ]

    for page in page_list:
        create_endpoint(app, page)

    @app.route("/")
    def home():
        return render_template("home.html")

    return app


def create_endpoint(app, page):
    @app.route(f"/{page}/", endpoint=page)
    def view_func():
        return render_template(f"{page}.html")

    return view_func
