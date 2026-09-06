# Format manuscrit JSON — AcoMytha ↔ AkoMythaTTS

**Feature :** F-NAR-024.  
**Schema :** `2.0` (celui du renderer AkoMythaTTS).  
**Base importée :** dépôt AkoMythaTTS, branche `feat/catalogue-tts-pipeline`, commit `244ba22`.

Deux projets, un contrat :

| Projet | Rôle |
| --- | --- |
| **AcoMytha** | Écrire les histoires de la plus haute qualité **en texte**. Le manuscrit est un JSON. |
| **AkoMythaTTS** | Transformer ce JSON en parole (Kokoro, puis OpenVoice si échantillon autorisé). |

L’app AcoMytha continue de lire les `.xlsx` tant que F-DAT-002 n’importe pas ce JSON. **On n’écrit plus les histoires définitives dans Excel.** On écrit ici : `stories/json/`.

## Ne pas confondre profil et prosodie

Ce sont **deux objets distincts**. Le JSON n’est pas la voix.

### 1. Profil du parlant (permanent)

Fichier : `stories/json/voice_registry.json`.

Identité **stable** d’un personnage, **la même dans toutes les histoires** :

- `narrator` — narratrice
- `father` / `mother` — papa / maman
- `teacher` — maîtresse (Bernadette si le récit la nomme ; le **profil** reste `teacher`)
- `friend_boy` / `friend_girl`
- `character.amir`, `character.nina`, `character.victorina`, … (troupe D16)

Champs : `display_name`, `gender`, `age_group` (sélection, pas le son), `role`, `kokoro_voice`, `reference_audio` (WAV OpenVoice ; `null` = Kokoro stock), `voice_fingerprint` `{speed, pitch_semitones, gain_db}`, `direction`.

On **ne change pas** le profil d’Amir d’une histoire à l’autre. Le clonage commercial exige une **autorisation vocale explicite**. Papa : vrai échantillon masculin, pas un gros down-pitch de `ff_siwis`.

Aujourd’hui tous les profils pointent `ff_siwis` : différenciation provisoire par l’empreinte. Le timbre réel = AkoMythaTTS.

### 2. Prosodie du passage (par réplique)

Dans `stories/json/<story_id>.json`, chaque `chunks[id].segments[]` a :

```json
{
  "speaker": "character.amir",
  "text": "Papa, mon bateau peut voyager ici !",
  "prosody": {
    "speed": 1.06,
    "gain_db": 0.5,
    "pitch_semitones": 1.0,
    "pause_before_ms": 80,
    "pause_after_ms": 260,
    "emotion": "excited",
    "intonation": "rising",
    "emphasis_words": ["voyager"]
  }
}
```

`speaker` = id du registre. `prosody` = **comment** ce parlant dit **cette** phrase.

Émotions : `neutral`, `calm`, `warm`, `joy`, `excited`, `focused`, `suspense`, `storytelling`, `sadness`, `anger`, `surprise`, `fear`, `whisper`.  
Intonations : `neutral`, `rising`, `falling`, `dramatic`, `storytelling`.  
Vitesse : 0.5–1.6. `emphasis_words` : mots **présents** dans `text` (stockés ; pas encore acoustiques côté TTS).

Rendu TTS : vitesse finale ≈ profil × réplique × preset d’émotion ; pitch additif.  
`pause_after_ms` ≠ `interaction.wait_ms` (questions : 3000–7000 ms, moteur de lecture, pas le WAV).

## Histoire JSON

Racine : `schema_version`, `story_id`, `title`, `language`, `catalogue`, `source`, `editorial_status`, `entry_chunk`, `speaker_profiles` (liste d’ids du registre), `chunks` (**objet** indexé par `chunk_id`, pas une liste).

Chunk : `kind`, `lesson_id`, `segments[]`, `interaction`, `options`, `night_policy`, `sound_cues`, `editorial_notes`, `next_chunk`, `default_next_chunk`.

Renderer (dans AkoMythaTTS, pas ici) :

```bash
python catalogue_renderer.py catalogue/stories/TREE-AUT-001.json \
  --registry catalogue/voice_registry.json \
  [--only-chunk CHK_T0000_P0000] [--without-cloning] --output output
```

## Conversion ChatGPT : base, pas l’écriture

Le bundle `AkoMythaTTS-catalogue-tts.bundle` **ne se clone pas** (historique incomplet : objet `2524e042` manquant, parent de `396e4a9c`). Ne pas l’utiliser.

Les 1 449 JSON sur `feat/catalogue-tts-pipeline` sont une **conversion XLSX → JSON** (`catalogue_converter.py`) : textes et graphes copiés, **prosodie générique** (ex. `emphasis_words: ["sac"]` sur chaque phrase d’ouverture, y compris celles sans « sac »). Statut d’origine : `source_preserved_requires_human_commercial_review`.

Ce n’est **pas** l’écriture définitive. On n’importe pas les 168 Mo dans Git AcoMytha.

Importé ici :

- `stories/json/voice_registry.json` — 50 profils
- `stories/json/TREE-AUT-001.json` — étalon ; `CHK_T0000_P0000` en première passe humaine (`editorial_status: in_human_rewrite`)

Le reste du corpus se réécrit **titre par titre** dans ce format, à partir du texte déjà relu (xlsx / dumps) + prosodie réelle.

## Processus d’écriture

1. Manuscrit = `stories/json/<story_id>.json`.
2. Chaque réplique : un `speaker` du registre + une `prosody` de la scène.
3. `text` change → `prosody` et audio périmés (F-NAR-022).
4. Audio = AkoMythaTTS, pas Piper, pour les histoires nouvelles (Piper reste le bake existant, F-AUD-005).
5. Excel : source **transitoire** du runtime. Plus le lieu de l’écriture définitive.
