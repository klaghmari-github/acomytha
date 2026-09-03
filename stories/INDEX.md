# Index du corpus Sentier

Vague du 3 septembre 2026. Branche `feat/F-GEN-001-corpus-histoires`.

## Volumes (validés)

| Kind | Fichiers | Leçons couvertes | Graphe |
| --- | --- | --- | --- |
| Atomique | 685 | 85 / 85 | 1 chemin, `question_lesson` |
| Ramifiée | 760 | 85 / 85 | 3 niveaux × 3 options = 27 feuilles |

Total **1445** histoires. Validateur déterministe : `python3 stories/outils/validate.py` → **1445 APPROVED_TEXT**, 0 REJECTED, 0 REVISION.

Le générateur **n’auto-approuve pas** un paquet audio. Statut maximal ici : `APPROVED_TEXT`. TTS/ASR et revue humaine restent en aval (VAL-AUD, HUM).

## Domaines (atomiques)

SAN 73 · SEC 75 · EMO 88 · REL 81 · DIF 60 · AUT 40 · FAM 37 · COL 35 · VIV 38 · TMP 44 · SOC 49 · JEU 36 · LAN 29 (atomiques). N1 182 · N2 280 · N3 223.

## Identifiants

- `ATOM-<LECON>-<NN>.json`
- `TREE-<DOMAINE>-<NNN>.json`

## Règles rappel

Voir `REGLES.md`. Famille racontée papa-maman-enfants. Formulation positive des dangers. Pas de religion, politique, guerre, crime, discours de genre.
