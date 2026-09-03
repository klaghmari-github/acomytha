# Décisions — passage JSON → Excel + audio test

Date : 3 septembre 2026. Pas d’approbation demandée (consigne fondateur).

## Format

- **Un fichier Excel par arbre** = `stories/arbres/<tree_id>.xlsx`.
- Identifiant d’histoire = **nom de fichier** (`TREE-SEC-001`, `ATOM-SAN.ALI.001-01`). Colonne `story_id` identique (pas de `STO_00001` pour ne pas casser le corpus).
- Feuilles : `meta`, `chunks`, `journal`, `legend`.
- Types de chunks : `passage_debut` | `passage` | `passage_question` | `transition_question` | `passage_fin`.
- Options de choix : colonnes `option_k_label` / `option_k_next_chunk` sur la ligne `transition_question` (pas de type `transition_option` : le texte des options est dans la question « On peut prendre A, B, ou C. »).
- TTS : colonnes Piper / SSML / xAI / Kokoro / Melo / eSpeak. Bake actuel = **Piper ou eSpeak**, 0 €. `text` reste nu ; `text_ssml` et `text_xai_tags` sont des exports.

## Optimisations faites à la conversion

- Prompts de choix réécrits pour **coller aux labels** (ex. plus « quelle couleur ? » si les options sont seau / doudou).
- `question_lesson` → `passage_question` + passage de **confirmation** (feedback fusionné). N’altère pas le cours.
- Si un chemin n’avait aucune question d’écoute avant la feuille : insertion d’une `passage_question` + confirmation (journalisée).
- `ending` scindé : corps en `passage` / `passage_fin` = « L'histoire est finie. »
- Profil TTS selon `kind` + `age_band` + `positive_only_critical` (plus lent sur leçon / fin).

## Audio test

- Dossier `stories/audio/<tree_id>/<chunk_id>.wav` **et** `.mp3`
- **Bug muet (2026-09-03) :** Piper écrit du PCM 16-bit **22050 Hz mono**. Les échantillons n’étaient **pas** à zéro (crête 32767, RMS ~5000). `aplay` lisait le fichier. En revanche 22050 Hz mono WAV est souvent **inaudible / refusé** par lecteurs Windows, iPhone, Android, aperçu navigateur. Cause = format de livraison, pas un TTS vide.
- **Correctif :** rééchantillonner à **44100 Hz**, normaliser à −1 dBFS, écrire WAV PCM propre **+ MP3 64 kbit/s**. Vérif automatique : `peak >= 500` et MP3 > 400 octets.
- Script : `stories/outils/xlsx_to_audio.py` (`--fix-existing` pour les 22050 déjà là ; bake normal fait 44100+mp3).

## JSON

Après 1445 xlsx OK (0 erreur), les JSON `atomiques/` et `ramifiees/` sont **supprimés**.  
Référentiel : `lecons.xlsx` (catalogue) + `lecon_histoires.xlsx` (liaisons). `lecons.json` retiré. Restent : `schema.json` (archive), `REGLES.md`, outils.

## Compteurs

1445 xlsx, **68787** chunks.
