import datetime

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

    page_data = {
        "solutions": {
            "cards": [
                {
                    "cover": "images/pharminfo-mini-solutions.png",
                    "headline": "Pharminfo.fr",
                    "title": "Votre pharmacie disponible 24h/24 et 7j/7",
                    "body": "Des services adaptés pour vous et vos patients :",
                    "features": [
                        "Envoi d'ordonnance",
                        "Click and Collect",
                        "Vente en ligne",
                        "Prise de rendez-vous",
                    ],
                },
                {
                    "cover": "images/kozea-media-mini-solutions.png",
                    "headline": "Kozea media",
                    "title": "Votre communication maîtrisée et externalisée",
                    "body": "Kozea media conseille depuis 10 ans les acteurs "
                    "de santé dans leur transformation digitale.",
                    "features": [
                        "Gestion des réseaux sociaux",
                        "Régie média (publicité)",
                        "Création graphique et contenu rédactionnel",
                    ],
                },
                {
                    "cover": "images/backoffice-mini-solutions.png",
                    "headline": "Backoffice",
                    "title": "Votre tiers-payant géré de A à Z",
                    "body": "Redonnez de la valeur à votre métier de "
                    "pharmacien et gagnez du temps sur vos tâches "
                    "administratives !",
                    "features": [
                        "Externalisation du tiers-payant",
                        "Formations adaptées à l'équipe officinale",
                        "Suivi et contrôle en toute autonomie",
                    ],
                },
                {
                    "cover": "images/promomaker-mini-solutions.png",
                    "headline": "Promomaker",
                    "title": "Vos campagnes promotionnelles en 1 clic",
                    "body": "Créez et diffusez très simplement des campagnes "
                    "de communication et de promotion pour votre pharmacie.",
                    "features": [
                        "Création automatique",
                        "Accessible pour tous et pour votre groupement",
                        "Choix du format d'impression",
                    ],
                },
                {
                    "cover": "images/kozea-community-mini-solutions.png",
                    "headline": "Kozea community",
                    "title": "Développement de projets innovants",
                    "body": "Bénéficiez des logiciels libres développés par "
                    "les membres de l'équipe Kozea group et de leur expertise "
                    "pour la création de nouveaux projets.",
                    "features": [],
                },
            ]
        }
    }

    for page in page_list:
        create_endpoint(app, page, page_data)

    @app.route("/")
    def home():
        return render_template("home.html", page="home")

    app.add_template_global(datetime)

    return app


def create_endpoint(app, page, page_data):
    @app.route(f"/{page}/", endpoint=page)
    def view_func():
        return render_template(
            f"{page}.html", data=page_data.get(page), page=page
        )

    return view_func
