---
author: Laurène Jover
title: "Du push à la prod, l’histoire d’un commit"
date: 2019-02-26
tags: Community
caption: du-push-a-la-prod-lhistoire-dun-commit.webp
---

Spoiler : GitLabCI & bash.

L’objectif est qu’une mise en production soit effectuée lorsqu’un commit a lieu sur une branche de production (master pour nous). Si il s’agit d’une autre branche, on s’arrête au déploiement d’une plateforme de test.

Les projets sont stockés sur GitHub. Pour pouvoir utiliser GitLabCI, ils ont été importés sur GitLab, et un gitlab-runner a été installé (avec comme exécuteur Docker).

Ça y est ça commence, petit commit est pushé. Un hook GitHub alerte le gestionnaire de l’intégration continue (son petit nom c’est Junkrat). L’alerte est reçue, Junkrat met à jour le projet sur GitLab.

GitLab détecte le nouvel arrivant.

Un fichier « .gitlab-ci.yml » est présent dans le dépôt et le gitlab-runner est disponible.

Une pipeline est lancée, le plan prévu pour le valeureux commit est celui-ci :

![ci_flow](/2019-02-26_du-push-a-la-prod-lhistoire-dun-commit/ci_flow.png)

Les premières étapes consistent en la vérification de l’installation, du build et des tests.

C’est validé, petit commit entre en lice pour un déploiement en test (bien sûr on est sur master ou sur une branche avec une pull request ouverte).

Junkrat est appelé depuis la pipeline pour lancer le script bash qui va permettre à petit commit de se transformer en plateforme de test.

Sur un serveur de test, le projet est cloné, et on se place au niveau du commit.

Une fois ici, l’installation et le build sont lancés. Cette fois, pas dans un container Docker, mais bel et bien sur un vrai serveur.

Si le projet utilise une base de données SQLite, une base est simplement récupérée depuis les sauvegardes (les sauvegardes c’est bien) et mise à disposition de la plateforme.

Dans le cas d’une base PostgreSQL, c’est différent. Tous les jours, les bases sont restaurées sur le serveur de test à partir des sauvegardes. Une base d’un projet peut alors être amenée à être utilisée par plusieurs plateformes en même temps. Mais si petit commit veut une base rien qu’à lui, pour par exemple supprimer des tables, il suffit que le nom de sa branche contienne « database », et une base sera à disposition exclusive de la plateforme.

Enfin, les divers fichiers de configuration nécessaires (configuration du projet, nginx et uWSGI) sont récupérés depuis les sauvegardes, et adaptés à l’environnement de test (merci sed).

La plateforme de test est up.

Petit commit est sur la branche master, le déploiement de la plateforme de test est un succès. Mais son aventure ne s’arrête pas là, il doit aller en production.

Une nouvelle fois Junkrat est appelé pour lancer le script bash associé.

Malgré les histoires effrayantes sur les mises en production qu’il a entendues, le commit n’a pas peur, il sait que ça va être similaire au test.

Un dossier de production n’est qu’un simple clone du dépôt git du projet. Le « git pull » est lancé, puis une installation, et un build, ça rappelle des souvenirs.

Ce que le commit ne sait pas, c’est que ça vient de se passer dans une copie du dossier de production, puis un lien symbolique a opéré, évitant alors du downtime sur le service.

Le uWSGI est touché.

Le commit a fini sa mission.

Il pense alors à ses amis les variables GitLab, Docker, gitlab-runner, ssh, bash et MakeCitron sans qui tout ça aurait été beaucoup plus compliqué.

Le commit est en production…
