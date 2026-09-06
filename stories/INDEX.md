# Index du corpus AcoMytha

Vague du 3 septembre 2026. Branche `feat/F-GEN-001-corpus-histoires`.

**Manuscrit définitif (F-NAR-024, 6 sept. 2026) : JSON schema 2.0**, compatible AkoMythaTTS.  
`stories/json/<story_id>.json` + `stories/json/voice_registry.json`. Contrat : `stories/FORMAT_JSON_TTS.md`. Profil du parlant ≠ prosodie du passage.

**Runtime actuel de l’app : Excel**, un fichier par arbre.  
`stories/arbres/<tree_id>.xlsx` — atomiques + ramifiés live. Archive : `stories/archive/arbres/`. Voir `PRIORITE.md`. Tant que F-DAT-002 n’importe pas le JSON, le lecteur lit encore l’xlsx.

Les anciens JSON `atomiques/` et `ramifiees/` avaient été convertis puis **supprimés** (`DECISIONS_EXCEL.md`). Ce n’est **pas** le schema 2.0 TTS.

| Kind | Actif (`arbres/`) | Archive | Graphe |
| --- | --- | --- | --- |
| Atomique | 685 | 0 | 1 chemin, `passage_question` |
| Ramifiée | 1 (`TREE-AUT-001`) | 763 | 3 niveaux × 3 options = 27 feuilles |

Audio test (Piper, WAV) : `stories/audio/TREE-SEC-001/` (86) et `stories/audio/ATOM-SAN.ALI.001-01/` (5).  
Bake : `python3 stories/outils/xlsx_to_audio.py` (option `--only`, `--limit`).

Outils : `json_to_xlsx.py` (historique), `xlsx_to_audio.py`.  
Leçons : `referentiel/lecons.xlsx`. Liaisons : `referentiel/lecon_histoires.xlsx`.  
Règles : `REGLES.md`.
