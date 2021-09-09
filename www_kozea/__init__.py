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
                    "page": "pharminfo",
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
        "pharminfo": {
            "cards": [
                {
                    "icon": "images/pharminfo-ordonnance.svg",
                    "title": "Envoi d'ordonnance",
                },
                {
                    "icon": "images/pharminfo-click-collect.svg",
                    "title": "Click and Collect",
                },
                {
                    "icon": "images/pharminfo-vente.svg",
                    "title": "Vente en ligne",
                },
                {
                    "icon": "images/pharminfo-rendez-vous.svg",
                    "title": "Prise de rendez-vous en ligne",
                },
            ],
            "cards_alt": [
                {
                    "title": "Ecoweb",
                    "body": "Site internet vitrine",
                },
                {
                    "title": "Flexiweb+",
                    "body": "Envoi d'ordonnance et prise de rendez-vous "
                    "en ligne",
                },
                {
                    "title": "Click and Collect",
                    "body": "Commande en ligne avec retrait et paiement "
                    "en pharmacie",
                },
                {
                    "title": "Optiweb",
                    "body": "Vente en ligne avec une base de plus de "
                    "8000 produits "
                    "et la synchronisation possible avec votre LGO",
                },
            ],
        },
        "kozea-media": {
            "cards": [
                {
                    "icon": "images/kozea-media-gestion.svg",
                    "title": "Gestion des réseaux sociaux",
                    "body": "Facebook & Instagram",
                },
                {
                    "icon": "images/kozea-media-creation.svg",
                    "title": "Création graphique",
                    "body": "Logo, affiche, charte graphique, thème "
                    "personnalisé pour votre site internet",
                },
                {
                    "icon": "images/kozea-media-redaction.svg",
                    "title": "Contenu rédactionnel",
                    "body": "Article de blog, newsletter",
                },
                {
                    "icon": "images/kozea-media-conseil.svg",
                    "title": "Conseil stratégie digitale",
                    "body": "Plan d'actions, accompagnement",
                },
                {
                    "icon": "images/kozea-media-regie.svg",
                    "title": "Régie média",
                    "body": "Gestion d'espaces publicitaires, plan média",
                },
            ]
        },
        "backoffice": {
            "cards": [
                {
                    "icon": "images/backoffice-gestion.svg",
                    "title": "Pour gérer votre tiers-payant en interne",
                    "body": "Nous mettons à votre disposition un outil web "
                    "facile d'utilisation avec un contrôle simple et rapide "
                    "de vos rejets",
                },
                {
                    "icon": "images/backoffice-externalisation.svg",
                    "title": "Un service d'externalisation pour plus de "
                    "liberté",
                    "body": "Déléguez l'ensemble de la gestion de votre "
                    "tiers-payant à nos experts !",
                },
                {
                    "icon": "images/backoffice-formation.svg",
                    "title": "Pour comprendre et approfondir la gestion du "
                    "tiers-payant",
                    "body": "Nous proposons plusieurs offres de formations "
                    "pour les débutants comme pour les plus experts !",
                },
            ]
        },
        "groupement": {
            "cards": [
                {
                    "icon": "images/service-pharminfo.svg",
                    "title": "Site internet pour mettre en avant votre "
                    "groupement et vos adhérents",
                    "body": "Vitrine pour votre groupement et des services "
                    "adaptés comme la réservation d'ordonnances, le Click & "
                    "Collect, la vente en ligne ou la prise de rendez-vous "
                    "en ligne",
                    "page": "pharminfo",
                },
                {
                    "icon": "images/service-kozea-media.svg",
                    "title": "Votre communication maîtrisée et externalisée",
                    "body": "Réseaux sociaux, rédaction d'articles, "
                    "création visuelle, régie média : pour vous et vos "
                    "adhérents.",
                    "page": "kozea-media",
                },
                {
                    "icon": "images/service-backoffice.svg",
                    "title": "Le tiers-payant de vos adhérents géré de A à Z",
                    "body": "Délégation, formation, gestion en interne : "
                    "recentrez le pharmacien sur son cœur de métier.",
                    "page": "backoffice",
                },
                {
                    "icon": "images/service-promomaker.svg",
                    "title": "Vos campagnes promotionnelles en 1 clic",
                    "body": "Outil simple et accessible pour uniformiser "
                    "vos PLV (Publicités sur Lieu de Vente).",
                    "page": "promomaker",
                },
            ]
        },
        "à-propos": {
            "cards": [
                {
                    "icon": "images/service-pharminfo.svg",
                    "title": "Création de sites internet",
                    "page": "pharminfo",
                },
                {
                    "icon": "images/service-kozea-media.svg",
                    "title": "Gestion de la communication digitale",
                    "page": "kozea-media",
                },
                {
                    "icon": "images/service-backoffice.svg",
                    "title": "Gestion du tiers-payant",
                    "page": "backoffice",
                },
                {
                    "icon": "images/service-promomaker.svg",
                    "title": "Créations d'affiches promotionnelles",
                    "page": "promomaker",
                },
            ],
            "cards_alt": [
                {
                    "title": "J'aide ma pharmacie",
                    "body": "Augmentez votre référencement sur internet pour "
                    "plus de trafic en officine.",
                    "url": "https://www.jaidemapharmacie.fr/",
                },
                {
                    "title": "Engagé pour la e-santé",
                    "body": "Nous sommes fiers de faire partie des "
                    "signataires de la charte «Engagé pour la e-santé» aux "
                    "côtés du Ministère des Solidarités et de la Santé",
                    "url": "https://esante.gouv.fr/sites/default/files/"
                    "media_entity/documents/charte-engage-pour-la-e-sante"
                    "-06-06-21.pdf",
                },
                {
                    "title": "Femmes de santé",
                    "body": "Nous soutenons également le collectif «Femmes "
                    "de santé» en signant leur charte et en nous engageant "
                    "vers une meilleure visibilité des femmes expertes dans "
                    "le secteur de la santé.",
                    "url": "https://www.femmesdesante.fr/",
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
