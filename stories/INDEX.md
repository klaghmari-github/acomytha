# Index du corpus Sentier

Vague du 3 septembre 2026. Branche `feat/F-GEN-001-corpus-histoires`.

## Volumes (validés)

| Kind | Fichiers | Leçons couvertes | Graphe |
| --- | --- | --- | --- |
| Atomique | 316 | 85 / 85 | 1 chemin, `question_lesson` |
| Ramifiée | 331 | 85 / 85 | 3 niveaux × 3 options = 27 feuilles |

Total **647** histoires. Validateur déterministe : `python3 stories/outils/validate.py` → **647 APPROVED_TEXT**, 0 REJECTED, 0 REVISION.

Le générateur **n’auto-approuve pas** un paquet audio. Statut maximal ici : `APPROVED_TEXT`. TTS/ASR et revue humaine restent en aval (VAL-AUD, HUM).

## Domaines (atomiques)

SAN · SEC · EMO · REL · DIF · AUT · FAM · COL · VIV · TMP · SOC · JEU · LAN — tous représentés, plusieurs variantes N1/N2/N3 par leçon.

## Identifiants

- `ATOM-<LECON>-<NN>.json`
- `TREE-<DOMAINE>-<NNN>.json`

## Règles rappel

Voir `REGLES.md`. Famille racontée papa-maman-enfants. Formulation positive des dangers. Pas de religion, politique, guerre, crime, discours de genre.
