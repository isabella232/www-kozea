import datetime

from flask import Flask, render_template
from sassutils.wsgi import SassMiddleware

MENU_LIST = {
    "solutions": "Solutions",
    "ressources": "Ressources",
    "à-propos": "À propos",
    "contact": "Contact",
}

PAGE_LIST = [
    "à-propos",
    "backoffice",
    "community",
    "contact",
    "groupement",
    "kozea-media",
    "legal",
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


def create_app():
    app = Flask(__name__)

    app.wsgi_app = SassMiddleware(
        app.wsgi_app,
        {"www_kozea": ("static/sass", "static/css", "/static/css", False)},
    )

    page_data = {
        "home": {
            "cards": [
                {
                    "icon": "images/service-pharminfo.svg",
                    "title": "Votre pharmacie disponible 24h/24",
                    "body": "Site internet avec réservation d'ordonnance, "
                    "Click & Collect, vente en ligne.",
                    "page": "pharminfo",
                },
                {
                    "icon": "images/service-kozea-media.svg",
                    "title": "Votre communication maîtrisée et externalisée",
                    "body": "Réseaux sociaux, rédaction d'articles, "
                    "création visuelle, régie média.",
                    "page": "kozea-media",
                },
                {
                    "icon": "images/service-backoffice.svg",
                    "title": "Votre tiers-payant géré de A à Z",
                    "body": "Délégation, formation, gestion en interne.",
                    "page": "backoffice",
                },
                {
                    "icon": "images/service-promomaker.svg",
                    "title": "Vos campagnes promotionnelles en 1 clic",
                    "body": "Outil simple et accessible pour votre PLV.",
                    "page": "promomaker",
                },
            ]
        },
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
                    "page": "pharminfo",
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
                    "page": "kozea-media",
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
                    "page": "backoffice",
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
                    "page": "promomaker",
                },
                {
                    "cover": "images/kozea-community-mini-solutions.png",
                    "headline": "Kozea community",
                    "title": "Développement de projets innovants",
                    "body": "Bénéficiez des logiciels libres développés par "
                    "les membres de l'équipe Kozea group et de leur expertise "
                    "pour la création de nouveaux projets.",
                    "features": [],
                    "page": "community",
                },
            ],
            "cards_alt": [
                {
                    "title": "Mise à jour de votre site internet",
                    "body": "Augmentez votre référencement sur internet pour "
                    "plus de trafic en officine.",
                    "page": "kozea-media",
                },
                {
                    "title": "Animation des réseaux sociaux",
                    "body": "Soyez au plus proche de vos patients et "
                    "optimisez votre présence en ligne.",
                    "page": "kozea-media",
                },
                {
                    "title": "Création de vos contenus rédactionnels et "
                    "graphiques",
                    "body": "Valorisez votre communication et l'image de "
                    "votre pharmacie.",
                    "page": "kozea-media",
                },
                {
                    "title": "Gestion de votre tiers-payant",
                    "body": "Déléguez les tâches administratives pour vous "
                    "recentrer sur votre cœur de métier.",
                    "page": "backoffice",
                },
            ],
        },
    }

    for page in PAGE_LIST:
        create_endpoint(app, page, page_data)

    @app.route("/")
    def home():
        return render_template(
            "home.html",
            page="home",
            data=page_data.get("home"),
            menu_list=MENU_LIST,
        )

    app.add_template_global(datetime)

    return app


def create_endpoint(app, page, page_data):
    @app.route(f"/{page}/", endpoint=page)
    def view_func():
        return render_template(
            f"{page}.html",
            data=page_data.get(page),
            page=page,
            menu_list=MENU_LIST,
        )

    return view_func
