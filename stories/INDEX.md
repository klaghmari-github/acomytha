# Index du corpus AcoMytha

Vague du 3 septembre 2026. Branche `feat/F-GEN-001-corpus-histoires`.

**Source (F-NAR-024) : Excel**, un fichier par histoire, texte **et** prosodie.  
Chaîne : `arbres/*.xlsx` → moteur → `json/<story_id>.json` → TTS → `audio/<story_id>_<chunk_id>.wav` → catalogue de l’app. Trois dossiers, **pas** de sous-dossiers : les IDs font les noms. Contrat : `stories/FORMAT_JSON_TTS.md`.

Live : `stories/arbres/<story_id>.xlsx`. Archive encore à part : `stories/archive/arbres/`. Voir `PRIORITE.md`. Audio actuel encore en sous-dossiers `audio/<story_id>/` (bake Piper) — cible = plat.

Les anciens JSON `atomiques/` et `ramifiees/` avaient été convertis puis **supprimés** (`DECISIONS_EXCEL.md`). Ce n’est **pas** le schema 2.0 TTS (produit du moteur, pas un manuscrit).

| Kind | Actif (`arbres/`) | Archive | Graphe |
| --- | --- | --- | --- |
| Atomique | 685 | 0 | 1 chemin, `passage_question` |
| Ramifiée | 1 (`TREE-AUT-001`) | 763 | 3 niveaux × 3 options = 27 feuilles |

Audio test (Piper, WAV) : `stories/audio/TREE-SEC-001/` (86) et `stories/audio/ATOM-SAN.ALI.001-01/` (5).  
Bake : `python3 stories/outils/xlsx_to_audio.py` (option `--only`, `--limit`).

Outils : `json_to_xlsx.py` (historique), `xlsx_to_audio.py`.  
Leçons : `referentiel/lecons.xlsx`. Liaisons : `referentiel/lecon_histoires.xlsx`.  
Règles : `REGLES.md`.
