# Index du corpus Sentier

Vague du 3 septembre 2026. Branche `feat/F-GEN-001-corpus-histoires`.

**Source actuelle : Excel, un fichier par arbre.**  
`stories/arbres/<tree_id>.xlsx` — 1445 fichiers, 68787 chunks.

Les JSON `atomiques/` et `ramifiees/` ont été convertis puis **supprimés**. Voir `DECISIONS_EXCEL.md`.

| Kind | Fichiers xlsx | Leçons | Graphe |
| --- | --- | --- | --- |
| Atomique | 685 | 85 / 85 | 1 chemin, `passage_question` |
| Ramifiée | 760 | 85 / 85 | 3 niveaux × 3 options = 27 feuilles |

Audio test (Piper, WAV) : `stories/audio/TREE-SEC-001/` (86) et `stories/audio/ATOM-SAN.ALI.001-01/` (5).  
Bake : `python3 stories/outils/xlsx_to_audio.py` (option `--only`, `--limit`).

Outils : `json_to_xlsx.py` (historique), `xlsx_to_audio.py`.  
Leçons : `referentiel/lecons.json`.  
Règles : `REGLES.md`.
