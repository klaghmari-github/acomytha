# Index du corpus Sentier

Vague du 3 septembre 2026. Branche `feat/F-GEN-001-corpus-histoires`.

## Volumes

| Kind | Fichiers | Leçons couvertes | Graphe |
| --- | --- | --- | --- |
| Atomique | 130 | 85 / 85 | 1 chemin, `question_lesson` |
| Ramifiée | 120 | 85 / 85 | 3 niveaux × 3 options = 27 feuilles |

Validation déterministe : `python3 stories/outils/validate.py` → APPROVED_TEXT sur tout le corpus (aucune violation bloquante lexique/graphe/contrat).

Le générateur **n’auto-approuve pas** un paquet audio. Statut maximal ici : `APPROVED_TEXT`. TTS/ASR et revue humaine restent en aval (VAL-AUD, HUM).

## Domaines (atomiques)

SAN 11 · SEC 11 · EMO 13 · REL 11 · DIF 10 · AUT 6 · FAM 5 · COL 4 · VIV 4 · TMP 6 · SOC 8 · JEU 6 · LAN 3

## Âges atomiques

N1 (3–4) 46 · N2 (4–5) 60 · N3 (5–6) 24

## Identifiants

- `ATOM-<LECON>-<NN>.json`
- `TREE-<DOMAINE>-<NNN>.json`

## Règles rappel

Voir `REGLES.md`. Famille racontée papa-maman-enfants. Formulation positive des dangers. Pas de religion, politique, guerre, crime, discours de genre.
