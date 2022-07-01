---
author: Laurène Jover
title: "Comment générer automatiquement des jolis documents ?"
date: 2018-07-18
tags: Community
caption: comment-generer-automatiquement-des-jolis-documents.webp
---

La génération automatique de documents imprimables est une étape relativement classique de toutes les applications Web. Une partie réduite mais cruciale de l’information doit pouvoir être récupérée dans un format prêt à l’impression, par exemple des factures, des rapports ou des tickets.

Avant d’arriver à une solution convenable, je me suis égaré sur des chemins plus ou moins chaotiques, avec des résultats à chaque fois loin de mes espérances. Puis au fil des années, après avoir discuté avec nombre de développeurs employés par des entreprises de diverses tailles, il fallait bien me résoudre à l’évidence :

- Je n’étais pas le seul.
- Les problèmes étaient très souvent similaires.
- Les mauvaises solutions successives étaient très souvent similaires.

Et voilà comment je me retrouve à partager mes (douloureuses) expériences, afin de faire (peut-être !) gagner un peu de temps aux développeurs aventuriers qui se retrouvent au point où j’en étais il y a plus de 10 ans…

## Au début, ça a l’air facile

Je vais te raconter une histoire.

Tu as développé un petit site de réservation de places pour Jeanine et Marcel qui tiennent le café-théâtre à côté de chez toi. Tout fonctionne à merveille, les commandes en ligne affluent et le café-théâtre est plein tous les soirs. Malheureusement, après avoir payé leurs places en ligne, leurs gentils clients veulent tout de suite avoir une facture et un ticket à imprimer.

Mouais. Ça va qu’ils sont sympas, Jeanine et Marcel, et qu’ils te payent un coup à boire de temps en temps.

### Fausse bonne idée n°1 : mise en page manuelle

Franchement, générer une facture et un ticket, ça ne doit pas être bien sorcier.

Après avoir réfléchi quelques minutes, tu arrives à la conclusion que tu n’auras besoin que d’une bibliothèque capable de générer du PDF (comme
[Cairo](https://www.cairographics.org/)
ou
[jsPDF](https://parall.ax/products/jspdf)
par exemple). Avec ça, tu es capable d’écrire du texte et de dessiner des traits, c’est tout ce qu’il te faut.

Évidemment, quand on écrit un paragraphe, il faut apprendre à couper les lignes automatiquement au bon endroit. On n’a qu’à couper quand on voit des espaces près de la fin de la ligne, rien de trop compliqué.

Rien d’insurmontable non plus pour faire le petit tableau de la facture. Ça se passe bien, jusqu’au jour où le théâtre se décide à jouer la pièce « Mon amant est caché dans la baignoire pendant que mon mari prend sa douche ». C’est sûr, c’est pas Macbeth, ça prend beaucoup trop de place dans le tableau, et évidemment ça dépasse.

(Qui a eu l’idée d’un titre aussi stupide ?)

Va falloir aussi couper les lignes dans les tableaux. Ou alors que les colonnes aient des largeurs qui dépendent du contenu.

Va falloir aussi gérer le cas où des clients fous furieux décident d’acheter 20 places pour tous les spectacles du mois, parce que ton tableau ne tiendra pas sur une seule page.

Et va falloir aussi répondre à Jeanine qui se plaint du fait que la facture n’est « pas super jolie, ils en font des bien chez Desigual, tiens, regarde ». Franchement, avec tes t-shirts noirs pourris t’as vraiment l’air d’un graphiste ?

### Fausse bonne idée n°2 : pagination automatique

Au moment d’écrire ta 10 000e
ligne de code pour ajouter un petit cas particulier quand le tableau en page paire est coupé au milieu d’une ligne qui contient un prix supérieur à 10 €, il est temps de te rendre à l’évidence : soit Marcel va aussi te payer ta bouffe, tes vacances et tes séances chez le psy, soit il se trouvera quelqu’un d’autre pour générer ses factures. « C’est quand même pas bien compliqué ma petite-nièce elle fait des factures super vite sur Word et les mots ils sortent jamais des tableaux. »

Tu t’apprêtes à lui répondre d’un ton légèrement condescendant que les ordinateurs ne savent pas se servir de Word tout seuls, que malgré les apparences sa petite-nièce est un peu plus intelligente qu’un tas de ferraille boosté au
_machine learning_, quand tu es pris d’un doute.

Et si on générait des
[ODT](https://fr.wikipedia.org/wiki/OpenDocument)
et qu’on les envoyait à un LibreOffice qui les transformerait en PDF ? En plus, ça te permettrait de récupérer ce fabuleux modèle de facture Desigual en ODT qui doit bien traîner dans un coin d’Internet.

Ou du
[LaTeX](https://fr.wikipedia.org/wiki/LaTeX), tiens, pourquoi pas ? Mais ouais, plutôt que d’installer et de maintenir un LibreOffice et ses milliards de dépendances sur un serveur (avoue, c’était un peu stupide comme idée), installer LaTeX c’est tranquille. En plus, ça te permettrait de récupérer ce fabuleux modèle de facture Desigual en LaTeX qui doit bien traîner dans un coin d’Internet. Ou pas.

Bon. On va la faire courte.

LaTeX, ça marche bien pour faire des bouquins et des articles scientifiques. Tu pourrais rester des heures en extase devant des documents mis en page à la perfection, franchement, c’est presque la chose la plus belle sur Terre, presque…

Reste un problème : Jeanine. En vrac :

- « C’est quoi ces marges blanches, là, sur les côtés ? Tu trouves pas qu’elles sont mille fois trop grandes ? »
- « T’as vu ? Des fois, les mots, ils sortent du tableau, mais des fois pas. Marcel a une petite-nièce qui… »
- « On peut mettre un fond vert et jaune, un petit espace là, une petite bordure ici, et des points roses là ? »
- « C’est quoi ce
  [Ã©](http://i18nqa.com/debug/utf8-debug.html)
  ? »2018/06/28/newsletter-pour-suivre-toute-notre-actualite-abonnez-vous-a-notre-newsletter/
- « On peut mettre du Comic Sans MS ? »

Et si tu es resté bloqué sur l’idée de générer des fichiers ODT, aucun souci, voilà un lien vers
[la table des matières de la norme OpenDocument](http://docs.oasis-open.org/office/v1.2/os/OpenDocument-v1.2-os.pdf), elle fait 102 pages (la table des matières, hein, pas la norme).

Et dernier petit détail : quand tu embaucheras un graphiste pour rendre jolies tes factures, n’oublie pas de préciser dans ton annonce « 5 ans d’expérience en feuilles de style LaTeX et ODT seraient un plus ». Mouuuhahahaha. Hahahahaha. Hahaha.

## L’aveu d’impuissance, première étape vers la bonne idée

Ce soir, c’est la dernière de « Ma femme mange les brocolis à la vinaigrette que mon amant m’a préparés la semaine dernière ». Salle comble. Tu as décidé de noyer ton chagrin dans ces fameux shooters de téquila dont Marcel à le secret, avec le sel et les cornichons. C’est décidé, tu vas partir dans le Cantal élever des chèvres.

Tu t’es finalement rendu compte que de mettre en page du texte, c’était compliqué. Ce n’est pas que du texte, quand on y réfléchit bien. C’est du texte parfois justifié, des tableaux avec des colonnes aux largeurs automatiquement calculées, des coupures de mots aux bons endroits, des images et des photos et des code barres et des QR codes, des pages qui se sautent mais pas entre un titre et le paragraphe juste en dessous. C’est du contenu sur plusieurs colonnes, des encadrés, des marges, des belles lettrines au début des paragraphes, des coins arrondis, de l’italique, des trucs pas toujours droits…

Et en plus, faut que ça soit joli comme du Desigual.

### L’illumination

Alors que tu somnoles affalé sur la table, les yeux dans le vague, un peu perdu entre la traite des chèvres à 6 heures du matin et les croquettes de Médor-le-berger-allemand-qui-garde-le-troupeau, tu as l’illumination. Enfin !

(C’était quand, la dernière fois ? Et au fait, il faut combien de temps pour que le lait de chèvre devienne un fromage qui se défend ?)

C’était pourtant simple :

1. Il faut un format facile à générer.
2. Il faut un format facile à rendre joli.
3. Il faut un format facile à mettre en page.

Il faut du HTML et du CSS. Voilà. C’était pas plus compliqué.

Des millions de développeurs sont capables de pondre du HTML sur des centaines de frameworks. Des millions de webdesigners avec des Mac™ sont capables de rendre ça joli avec du CSS. Et surtout, on n’a jamais rien fait de plus compliqué que ces millions de sites d’agences de com qui se la pètent à coups de mises en page plus stupides les unes que les autres.

Euh… Juste une question : comment on fait des fichiers PDF avec du HTML et du CSS ?

### Les navigateurs pour l’impression

Bonne nouvelle pour toi : il y a maintes solutions, tu n’as qu’à choisir. Figure-toi que le HTML et le CSS ont été pensés pour faire des documents paginés. Même dans l’antique CSS 2, tu trouveras
[un chapitre entier sur les médias paginés](https://www.w3.org/TR/2011/REC-CSS2-20110607/page.html#the-page).

Alors évidemment, tu as déjà utilisé la fonction « Imprimer » de ton navigateur, et ce que tu as vu en sortie ne t’as pas particulièrement rassuré : des coupures de pages à l’arrache, des lettres qui sont positionnées n’importe comment les unes par rapport aux autres dans un même mot, et une vague impression qu’on a fait une capture d’écran à peine améliorée. Sans compter que tu n’as pas abandonné l’idée d’installer LibreOffice sur tes serveurs pour te retrouver à installer un navigateur à la place.

Je vais t’épargner une recherche sur ton moteur de recherche favori… Voilà les outils que tu cherches :

- [WeasyPrint](https://wkhtmltopdf.org/)
- [Wkhtmltopdf](https://wkhtmltopdf.org/)
- [Prince](http://www.princexml.com/)
- [AntennaHouse Formatter](http://www.antennahouse.com/antenna1/formatter/)

Ils ont tous leurs avantages et leurs inconvénients. Les deux derniers sont très performants, mais ils sont propriétaires et assez chers (je te laisse découvrir la licence par processeur proposée par Formatter, une merveille). Wkhtmltopdf est plutôt sympa, mais son principal avantage est également son principal inconvénient : il est basé sur WebKit, qui comme nous l’avons vu juste au-dessus n’est pas le meilleur outil de rendu pour la pagination.

Évidemment, je ne pourrais que trop te conseiller de jeter un œil sur WeasyPrint, d’abord parce que c’est un très bon outil, et accessoirement parce que c’est nous qu’on l’a fait. C’est libre, c’est du Python, sa communauté est super réactive (petit clin d’œil), ça ne coûte pas grand chose de l’essayer. Au pire, tu auras perdu une petite heure de ta vie, et au mieux tu auras gagné un paquet de temps, de clients et d’argent (en tout cas bien assez pour m’inviter au café-théâtre).

## Conclusion

Encore long est ton chemin, jeune Padawan. Tu te rendras bientôt compte que la pagination n’est pas la priorité du W3C et que nombre de ses normes ne sont encore que des brouillons pas toujours implémentés. Tu te rendras également compte de tous les petits cas particuliers que tu devras gérer : je ne veux jamais changer de page au milieu d’un tableau (sauf des fois), au milieu d’une liste (sauf des fois), après un titre (sauf des fois)… Et bien sûr, tu devrais très gentiment rapporter quelques tout petits bugs lorsque tu tenteras d’afficher des tableaux dans des pages multi-colonnes avec un peu de flex et une image flottante.

Mais en tout cas, c’est un sacré problème que tu viens de résoudre là. Finies les soirées à picoler la mauvaise vodka de Jeanine, finies les vielles remarques désobligeantes de Marcel sur ton goût douteux : tu demanderas à un·e webdesigner de te filer un coup de main, les gens qui ont du goût ont de bien meilleures compétences en CSS qu’en LaTeX (va savoir pourquoi).

Et t’as de la chance : quand je me suis posé la question il y a 10 ans, j’avais une petite étape de plus à régler : écrire WeasyPrint.

Mais ça, c’est une autre histoire…
