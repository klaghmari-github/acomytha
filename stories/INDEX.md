# Index du corpus Sentier

Vague du 3 septembre 2026. Branche `feat/F-GEN-001-corpus-histoires`.

## Volumes

| Kind | Fichiers | Leçons couvertes | Graphe |
| --- | --- | --- | --- |
| Atomique | 204 | 85 / 85 | 1 chemin, `question_lesson` |
| Ramifiée | 178 | 85 / 85 | 3 niveaux × 3 options = 27 feuilles |

Validation déterministe : `python3 stories/outils/validate.py` → APPROVED_TEXT sur tout le corpus (aucune violation bloquante lexique/graphe/contrat).

Le générateur **n’auto-approuve pas** un paquet audio. Statut maximal ici : `APPROVED_TEXT`. TTS/ASR et revue humaine restent en aval (VAL-AUD, HUM).

## Domaines (atomiques)

SAN 21 · SEC 23 · EMO 27 · REL 23 · DIF 18 · AUT 13 · FAM 10 · COL 9 · VIV 10 · TMP 14 · SOC 16 · JEU 12 · LAN 8

## Âges atomiques

N1 (3–4) 52 · N2 (4–5) 83 · N3 (5–6) 69

## Identifiants

- `ATOM-<LECON>-<NN>.json`
- `TREE-<DOMAINE>-<NNN>.json`

## Règles rappel

Voir `REGLES.md`. Famille racontée papa-maman-enfants. Formulation positive des dangers. Pas de religion, politique, guerre, crime, discours de genre.
