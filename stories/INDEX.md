# Index du corpus AcoMytha

Vague du 3 septembre 2026. Branche `feat/F-GEN-001-corpus-histoires`.

**Source actuelle : Excel, un fichier par arbre.**  
`stories/arbres/<tree_id>.xlsx` — atomiques + **un** ramifié actif (`TREE-AUT-001`). Les autres ramifiés : `stories/archive/arbres/`. Voir `PRIORITE.md`.

Les JSON `atomiques/` et `ramifiees/` ont été convertis puis **supprimés**. Voir `DECISIONS_EXCEL.md`.

| Kind | Actif (`arbres/`) | Archive | Graphe |
| --- | --- | --- | --- |
| Atomique | 685 | 0 | 1 chemin, `passage_question` |
| Ramifiée | 1 (`TREE-AUT-001`) | 763 | 3 niveaux × 3 options = 27 feuilles |

Audio test (Piper, WAV) : `stories/audio/TREE-SEC-001/` (86) et `stories/audio/ATOM-SAN.ALI.001-01/` (5).  
Bake : `python3 stories/outils/xlsx_to_audio.py` (option `--only`, `--limit`).

Outils : `json_to_xlsx.py` (historique), `xlsx_to_audio.py`.  
Leçons : `referentiel/lecons.xlsx`. Liaisons : `referentiel/lecon_histoires.xlsx`.  
Règles : `REGLES.md`.
