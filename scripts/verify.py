#!/usr/bin/env python3
"""Contrôle structurel autonome du parcours Org (sans effets de bord)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHAPTERS = 15
OFFICIAL = {
    2: 6, 5: 6, 8: 4, 9: 3, 10: 8, 11: 6, 12: 9,
}
EXPECTED_NUMBERED = {f"{chapter}.{sub}"
                     for chapter, count in OFFICIAL.items()
                     for sub in range(1, count + 1)}
EXPECTED_TOTAL_EXERCISES = 160
ERRORS: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        ERRORS.append(message)


def read(path: Path) -> str:
    check(path.is_file(), f"Fichier absent : {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8") if path.is_file() else ""


manifest = json.loads(read(ROOT / "curriculum.json"))
chapters = manifest.get("chapters", [])
check(len(chapters) == CHAPTERS, "Il faut exactement 15 chapitres")
check([c["number"] for c in chapters] == list(range(1, CHAPTERS + 1)),
      "Les chapitres doivent être dans l'ordre 1…15")
check(manifest["reference"]["url"] == "https://orgmode.org/orgguide.html",
      "Source officielle inattendue")

seen_ids: set[str] = set()
seen_official: set[str] = set()
all_sections: set[str] = set()
count = 0
for ch in chapters:
    n = ch["number"]
    title = ch["title"]
    exercises_path = ROOT / ch["exercise_file"]
    workshop_path = ROOT / ch["workshop_file"]
    solution_path = ROOT / ch["solution_file"]
    ex_text = read(exercises_path)
    sol_text = read(solution_path)
    workshop = read(workshop_path)
    check(f"* {n} — {title}" in ex_text,
          f"Titre principal manquant au chapitre {n}")
    check(bool(re.search(r"^\* ", workshop, re.M)),
          f"Atelier vide ou sans titre au chapitre {n}")
    seen_topics: set[str] = set()
    for i, topic in enumerate(ch["topics"], 1):
        num = topic["number"]
        key = f"{n}:{num}:{topic['title']}"
        check(key not in all_sections, f"Rubrique répétée : {key}")
        all_sections.add(key)
        if re.fullmatch(r"\d+\.\d+", num):
            check(int(num.split('.')[0]) == n,
                  f"Sous-section mal placée : {num}")
            seen_official.add(num)
        check(num not in seen_topics, f"Numéro/rubrique en double : {num} au chapitre {n}")
        seen_topics.add(num)
        heading = f"** {num} — {topic['title']}"
        check(heading in ex_text, f"Rubrique absente des exercices : {heading}")
        check(heading in sol_text, f"Rubrique absente des corrigés : {heading}")
        check(bool(topic["exercises"]), f"Rubrique sans exercice : {heading}")
        for expected_id in topic["exercises"]:
            count += 1
            check(bool(re.fullmatch(r"E\d{2}-\d{2}-[A-Z]", expected_id)),
                  f"Identifiant invalide : {expected_id}")
            check(expected_id not in seen_ids,
                  f"Identifiant dupliqué : {expected_id}")
            seen_ids.add(expected_id)
            check(len(re.findall(rf"^\*\*\* {re.escape(expected_id)} — ",
                                 ex_text, re.M)) == 1,
                  f"Exercice non unique dans le chapitre {n}: {expected_id}")
            check(len(re.findall(rf"^\*\*\* {re.escape(expected_id)} — ",
                                 sol_text, re.M)) == 1,
                  f"Corrigé non unique dans le chapitre {n}: {expected_id}")
    check("- Consigne ::" in ex_text and "- Validation ::" in ex_text,
          f"Manque des critères dans les exercices du chapitre {n}")

progression = read(ROOT / "PROGRESSION.org")
progress_ids = re.findall(r"^- \[ \] (E\d{2}-\d{2}-[A-Z])$", progression, re.M)
check(len(progress_ids) == EXPECTED_TOTAL_EXERCISES,
      f"Progression incomplète : {len(progress_ids)} cases")
check(set(progress_ids) == seen_ids,
      "Les cases de progression ne correspondent pas aux exercices")

check(seen_official == EXPECTED_NUMBERED,
      "Numérotation officielle incomplète : "
      f"manquantes={sorted(EXPECTED_NUMBERED - seen_official)}, "
      f"supplémentaires={sorted(seen_official - EXPECTED_NUMBERED)}")
check(count == EXPECTED_TOTAL_EXERCISES,
      f"Nombre d'exercices incorrect : {count} au lieu de {EXPECTED_TOTAL_EXERCISES}")

for kind in ("exercices", "ateliers", "corriges"):
    found = sorted((ROOT/kind).glob("[0-9][0-9]-*.org"))
    check(len(found) == CHAPTERS,
          f"{kind}: {len(found)} fichiers de chapitre au lieu de {CHAPTERS}")

for resource in ("assets/donnees.csv", "assets/code-exemple.py",
                 "assets/encart.org", "assets/figure.svg", "assets/site.css",
                 "ateliers/site/accueil.org", "ateliers/site/notes.org",
                 "setup/init.el", "scripts/check_org.el", "PROGRESSION.org",
                 "COUVERTURE.md", "README.md", "LICENSE"):
    check((ROOT/resource).exists(), f"Dépendance manquante : {resource}")

# Contrôle des liens explicites [[file:../...]] des 30 fichiers de cours.
for kind in ("exercices", "corriges"):
    for filename in (ROOT/kind).glob("*.org"):
        txt = filename.read_text(encoding="utf-8")
        for target in re.findall(r"\[\[file:([^\]]+)\]", txt):
            path = target.split("::",1)[0]
            check((filename.parent/path).exists(),
                  f"Lien local cassé : {filename.relative_to(ROOT)} -> {target}")

print("Contrôle d'exhaustivité — Org Mode Compact Guide")
print(f"  Chapitres : {len(chapters)}/{CHAPTERS}")
print(f"  Sous-sections numérotées : {len(seen_official)}/{len(EXPECTED_NUMBERED)}")
print(f"  Rubriques couvertes : {len(all_sections)}")
print(f"  Exercices identifiés : {count}/{EXPECTED_TOTAL_EXERCISES}")
print(f"  Dossiers : exercices, ateliers, corriges")
if ERRORS:
    print(f"ÉCHEC : {len(ERRORS)} erreur(s)",file=sys.stderr)
    for err in ERRORS:
        print(f"  - {err}",file=sys.stderr)
    sys.exit(1)
print("PASS : structure et traçabilité vérifiées")
