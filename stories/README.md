# Corpus d’histoires AcoMytha

Un **Excel par arbre** (`arbres/<tree_id>.xlsx`). Une histoire = un chemin racine→feuille. Un arbre = toutes les branches.

## Dossiers

| Chemin | Contenu |
| --- | --- |
| `arbres/` | 1445 xlsx (source actuelle) |
| `audio/` | WAV de test Piper (`<tree_id>/<chunk_id>.wav`) |
| `referentiel/lecons.xlsx` | Catalogue des 85 leçons (domaines, attributs) |
| `referentiel/lecon_histoires.xlsx` | Leçon → histoires → chunks pédagogiques |
| `outils/xlsx_to_audio.py` | Bake WAV |
| `outils/json_to_xlsx.py` | Convertisseur historique JSON→xlsx |
| `REGLES.md` | Contraintes éditoriales |
| `DECISIONS_EXCEL.md` | Choix de ce passage |
| `schema.json` | Ancien schéma JSON (archive) |

## Identifiants

Nom de fichier = `story_id` : `ATOM-SAN.ALI.001-01`, `TREE-SEC-001`.  
Chunks : `CHK_T0000_P0000`, `CHK_T0001_P0000`, `…_Q0001`, `…_F0001`.

## Audio

```bash
# voix Piper (une fois)
# voir outils/voices/README.md
python3 stories/outils/xlsx_to_audio.py --only TREE-SEC-001 ATOM-SAN.ALI.001-01
python3 stories/outils/xlsx_to_audio.py --limit 10
```
