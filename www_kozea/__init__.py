from flask import Flask, render_template


def create_app():
    # breakpoint()
    app = Flask(__name__)

    @app.route("/solutions/")
    def solutions():
        return render_template("solutions.html")

    @app.route("/lost/")
    def lost():
        return render_template("lost.html")

    @app.route("/")
    def home():
        return render_template("home.html")

    return app
