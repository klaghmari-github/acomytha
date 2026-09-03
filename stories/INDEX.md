# Index du corpus Sentier

Vague du 3 septembre 2026. Branche `feat/F-GEN-001-corpus-histoires`.

## Volumes

| Kind | Fichiers | Leçons couvertes | Graphe |
| --- | --- | --- | --- |
| Atomique | 176 | 85 / 85 | 1 chemin, `question_lesson` |
| Ramifiée | 154 | 85 / 85 | 3 niveaux × 3 options = 27 feuilles |

Validation déterministe : `python3 stories/outils/validate.py` → APPROVED_TEXT sur tout le corpus (aucune violation bloquante lexique/graphe/contrat).

Le générateur **n’auto-approuve pas** un paquet audio. Statut maximal ici : `APPROVED_TEXT`. TTS/ASR et revue humaine restent en aval (VAL-AUD, HUM).

## Domaines (atomiques)

SAN 19 · SEC 21 · EMO 24 · REL 20 · DIF 15 · AUT 12 · FAM 8 · COL 7 · VIV 9 · TMP 11 · SOC 14 · JEU 9 · LAN 7

## Âges atomiques

N1 (3–4) 52 · N2 (4–5) 78 · N3 (5–6) 46

## Identifiants

- `ATOM-<LECON>-<NN>.json`
- `TREE-<DOMAINE>-<NNN>.json`

## Règles rappel

Voir `REGLES.md`. Famille racontée papa-maman-enfants. Formulation positive des dangers. Pas de religion, politique, guerre, crime, discours de genre.
