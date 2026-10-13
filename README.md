# Login · Bibliothèque d’images SEIVEN

Retrouvez les visuels du dépôt, prévisualisez-les et récupérez leur URL directe pour les utiliser dans vos applications.

## Récupérer une image

- **Prévisualiser :** cliquez sur une vignette pour ouvrir l’image en taille réelle.
- **Copier l’URL :** survolez le bloc contenant l’adresse et cliquez sur le bouton de copie de GitHub, en haut à droite du bloc.
- **Utiliser :** collez cette URL dans votre application, votre page ou votre configuration. Elle pointe directement vers le fichier image.

## Catalogue

<!-- BEGIN IMAGE CATALOG -->

**4 images disponibles.**

<h3>cellule-config-dessin.webp</h3>

<a href="https://raw.githubusercontent.com/Seiven-Public/Login/main/cellule-config-dessin.webp"><img src="https://raw.githubusercontent.com/Seiven-Public/Login/main/cellule-config-dessin.webp" alt="cellule-config-dessin.webp" width="140" align="left"></a>

```text
https://raw.githubusercontent.com/Seiven-Public/Login/main/cellule-config-dessin.webp
```

<a href="https://raw.githubusercontent.com/Seiven-Public/Login/main/cellule-config-dessin.webp">Ouvrir l’image en taille réelle ↗</a>

<br clear="all">

<h3>logo-gpg-carre.webp</h3>

<a href="https://raw.githubusercontent.com/Seiven-Public/Login/main/logo-gpg-carre.webp"><img src="https://raw.githubusercontent.com/Seiven-Public/Login/main/logo-gpg-carre.webp" alt="logo-gpg-carre.webp" width="140" align="left"></a>

```text
https://raw.githubusercontent.com/Seiven-Public/Login/main/logo-gpg-carre.webp
```

<a href="https://raw.githubusercontent.com/Seiven-Public/Login/main/logo-gpg-carre.webp">Ouvrir l’image en taille réelle ↗</a>

<br clear="all">

<h3>logo-isofroid-carre.webp</h3>

<a href="https://raw.githubusercontent.com/Seiven-Public/Login/main/logo-isofroid-carre.webp"><img src="https://raw.githubusercontent.com/Seiven-Public/Login/main/logo-isofroid-carre.webp" alt="logo-isofroid-carre.webp" width="140" align="left"></a>

```text
https://raw.githubusercontent.com/Seiven-Public/Login/main/logo-isofroid-carre.webp
```

<a href="https://raw.githubusercontent.com/Seiven-Public/Login/main/logo-isofroid-carre.webp">Ouvrir l’image en taille réelle ↗</a>

<br clear="all">

<h3>logo-seiven-carre.webp</h3>

<a href="https://raw.githubusercontent.com/Seiven-Public/Login/main/logo-seiven-carre.webp"><img src="https://raw.githubusercontent.com/Seiven-Public/Login/main/logo-seiven-carre.webp" alt="logo-seiven-carre.webp" width="140" align="left"></a>

```text
https://raw.githubusercontent.com/Seiven-Public/Login/main/logo-seiven-carre.webp
```

<a href="https://raw.githubusercontent.com/Seiven-Public/Login/main/logo-seiven-carre.webp">Ouvrir l’image en taille réelle ↗</a>

<br clear="all">

<!-- END IMAGE CATALOG -->

## Ajouter ou remplacer une image

1. [Déposez vos images dans le dépôt](https://github.com/Seiven-Public/Login/upload/main), à la racine ou dans un sous-dossier.
2. Validez l’ajout sur la branche `main` (ou faites fusionner votre pull request).
3. Attendez la fin de l’action [Mettre à jour le catalogue](https://github.com/Seiven-Public/Login/actions/workflows/update-catalogue.yml), puis actualisez cette page.

Le catalogue se met à jour après chaque ajout, renommage ou suppression. Formats reconnus : **APNG, AVIF, BMP, GIF, ICO, JPEG, JPG, PNG, SVG et WebP**, y compris les extensions en majuscules. Les noms contenant des espaces ou des accents sont pris en charge.

Pour remplacer un visuel sans changer son URL, conservez son chemin et son nom de fichier. Renommer ou supprimer un fichier rend son ancienne URL inutilisable. GitHub peut conserver temporairement l’ancienne image en cache après un remplacement.

## Maintenance

La section **Catalogue** est générée automatiquement : les textes situés avant et après restent modifiables. Conservez les deux marqueurs HTML qui la délimitent.

Le script utilise uniquement Python 3.10 ou supérieur, sans dépendance à installer. Pour régénérer le catalogue localement après avoir ajouté vos fichiers à Git :

```sh
python3 scripts/generate_readme.py
```

Pour vérifier le générateur :

```sh
python3 -m unittest discover -s tests -v
```

L’action utilise le jeton automatique de GitHub avec la permission `contents: write` pour enregistrer le README. Si les règles de la branche interdisent les commits de cette action, son exécution échoue : générez alors le README localement et incluez-le dans votre pull request. Une exécution manuelle est également disponible dans l’onglet **Actions**.
