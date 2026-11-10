# Exercices du *Org Mode Compact Guide*

Parcours **pratique, progressif et en français** suivant l'ordre et la numérotation des 15 chapitres du [*Org Mode Compact Guide*](https://orgmode.org/orgguide.html) (consulté le **10 novembre 2026**). Les **42 sous-sections numérotées** du sommaire officiel sont traitées, ainsi que les rubriques non numérotées (installation, tables, tags, liens, Babel, etc.). Le parcours comporte **160 exercices** avec critères de réussite.

Le contenu pédagogique est original ; ce dépôt **n'est ni une copie ni une traduction du manuel GNU**. Le guide original reste la référence normative pour les commandes et comportements. Les exercices sont publiés sous CC0-1.0 ; voir [ATTRIBUTION.md](ATTRIBUTION.md) et [LICENSE](LICENSE).

## Organisation

```text
exercices/01-introduction.org               # énoncés, à lire sans les modifier
...
exercices/15-miscellaneous.org
ateliers/01-introduction.org                # fichiers de travail, à modifier
...
ateliers/15-miscellaneous.org
corriges/01-introduction.org                # invariants de correction + exemples
...
corriges/15-miscellaneous.org
ateliers/site/                              # mini-site pour le chapitre 13
assets/                                     # CSV, figure SVG, source, encart, CSS
setup/init.el                              # configuration Emacs isolée et locale
scripts/verify.py                         # audit structurel autonome
scripts/check_org.el                      # validation Org avec Emacs (optionnel)
curriculum.json                           # manifeste des rubriques et exercices
COUVERTURE.md                             # concordance section ↔ fichiers
PROGRESSION.org                            # suivi facultatif
exports/                                   # résultats générés, ignorés par Git
```

Les noms `NN-titre.org` reflètent **exactement les numéros de chapitres du guide**. Dans les fichiers, les sous-sections 2.1, 2.2, …, 12.9 reprennent leur numérotation officielle. Les rubriques internes sans numéro conservent le numéro de leur chapitre et un libellé explicite, pour ne pas inventer de sous-sections officielles.

## Démarrage (Emacs)

Prérequis : Emacs avec Org, Git et Python ≥ 3.9 pour les contrôles (aucune bibliothèque Python tierce). La configuration fournie fonctionne avec Org livré par Emacs, sans installation supplémentaire.

Depuis la racine du dépôt :

```sh
emacs -Q -l setup/init.el exercices/01-introduction.org
```

Lire le chapitre, puis ouvrir son fichier de travail avec le lien « Atelier » présent dans l'énoncé. Les fichiers d'atelier sont volontairement modifiables : utiliser `git diff` pour observer les changements, `git restore` **uniquement** si l'on souhaite effacer son propre travail. Les corrigés sont à consulter **après** la manipulation.

Le drapeau `-Q` ignore la configuration personnelle de l'utilisateur pour garantir un environnement pédagogique reproductible ; il n'altère pas `~/.emacs.d/init.el`. Pour intégrer les exercices à votre Emacs habituel, ouvrir normalement les `.org` et ne charger que les réglages dont vous avez besoin.

### Chapitres interactifs

- **09 et 10** : la configuration ajoute les ateliers 05, 08, 09 et 10 à l'agenda, définit les modèles de capture `t` et `j`, des cibles de refile et les raccourcis `C-c l`, `C-c a`, `C-c c`.
- **11 et 12** : les fichiers de référence sont relatifs à `assets/`. Les sorties HTML/TeX/ICS du dispatcher sont normalement placées près de l'atelier d'origine et sont ignorées par Git. Pour produire un PDF, une distribution LaTeX doit être installée.
- **13** : le projet local `cours` publie les sources de `ateliers/site/` dans `exports/site/`. Il ne transfère rien sur un serveur distant.
- **14** : Org Babel peut **exécuter du code**. Les blocs préchargés sont uniquement des démonstrations ; l'évaluation demande confirmation, et le bloc Python est marqué `:eval never`. Le tangling écrit un fichier sous `exports/` ; inspecter le code avant toute exécution.

Les dates des jeux d'essai (notamment **février 2027**) sont des exemples fixes. Utiliser `j` dans l'agenda pour s'y rendre ou changer les dates depuis `C-c .` / `C-c C-s` lorsque nécessaire ; les dates sont volontairement reproductibles.

## Contrôles

```sh
make check       # contrôle statique : 15 chapitres, 42 sous-sections, 160 exercices
make emacs-check # contrôle supplémentaire de parsing Org, si emacs est installé
```

`make check` ne nécessite pas Emacs. `make emacs-check` utilise `emacs -Q --batch` et contrôle le parsing sans évaluer les blocs source. Aucun contrôle statique ne remplace les exercices demandant une interaction manuelle : capture, clock, agenda, publications et export PDF doivent être testés dans Emacs.

Voir [COUVERTURE.md](COUVERTURE.md) pour la traçabilité exhaustive **par rapport au guide compact**, et non au manuel complet de plusieurs centaines de pages.

## Méthode pédagogique

1. Lire une sous-section du guide officiel, puis les consignes correspondantes ici.
2. Modifier `ateliers/NN-*.org` uniquement, avec les raccourcis Org proposés.
3. Vérifier le résultat observable (structure, recherche, agenda, fichier exporté).
4. Comparer avec `corriges/NN-*.org`, puis noter les différences dues à votre version d'Org.
5. Passer à la sous-section suivante ; les chapitres 08 à 14 réemploient plusieurs acquis.

Tout exercice a un identifiant stable de type `E08-02-A`, une consigne et une validation. Les corrections donnent des **conditions vérifiables** plutôt qu'une fausse capture d'écran pour les opérations dépendant de la date ou de l'installation.

## Publication dans un nouveau dépôt GitHub

Si ce dossier a été livré sous forme d'archive avec un historique Git, depuis la racine extraite :

```sh
gh auth login  # seulement si GitHub CLI n'est pas déjà authentifié
gh repo create fmaillar/org-compact-guide-exercises --public --source=. --remote=origin --push
```

Le dépôt distant n'est créé **que lorsque vous exécutez cette commande**. Pour un dépôt privé, remplacer `--public` par `--private`. Ne pas lancer `git init` une seconde fois : l'historique est déjà présent.

## Limitations et évolution

La version d'Org, le système de fenêtres et les raccourcis globaux peuvent influencer certains comportements. `M-TAB` peut être intercepté par le gestionnaire de fenêtres ; consulter `C-h k` et essayer `M-x completion-at-point`. Les liens Gnus, Rmail, BBDB, IRC et DocView sont couverts par la **connaissance de leur syntaxe**, mais leurs intégrations ne sont pas installées automatiquement. Le projet de publication ne configure aucun accès réseau.

Pour étendre le cours, conserver la concordance des numéros, mettre à jour `curriculum.json`, les trois fichiers par chapitre et `COUVERTURE.md`, puis lancer `make check` ; voir [CONTRIBUTING.md](CONTRIBUTING.md).
