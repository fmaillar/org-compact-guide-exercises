# Maintenir les exercices

Ce dépôt est un parcours pédagogique, pas un miroir du guide. Un changement doit préserver la reproductibilité, l'ordre officiel des chapitres et l'indépendance des ateliers.

Pour une rubrique existante, adapter les consignes dans `exercices/NN-*.org`, le matériel de départ dans `ateliers/NN-*.org` et les vérifications dans `corriges/NN-*.org`. Maintenir les identifiants `ENN-SS-X` stables et mettre à jour `curriculum.json` lorsque le nombre d'exercices change ; régénérer les lignes concernées de `COUVERTURE.md`.

Ne jamais ajouter aux corrigés un résultat horodaté fictif ni exécuter automatiquement des blocs source issus d'une contribution. Toute opération Git ou réseau doit être explicite. Les ressources de démonstration doivent être libres, non personnelles et utilisables hors ligne.

Tester avec `make check`, puis si possible `make emacs-check`. Les tests statiques vérifient la structure ; les exercices interactifs sont à valider manuellement avec la version d'Emacs/Org utilisée et à documenter dans la PR.
