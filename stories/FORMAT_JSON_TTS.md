# Chaîne Excel → JSON → audio

**Feature :** F-NAR-024.  
**Schema JSON :** `2.0`.  
**Runtime :** un seul serveur AcoMytha (branche `AkoMythaTTS`). L’éditeur vocal (`#/admin/editeur`) appelle `akomythatts.TtsApp` dans le même processus FastAPI que le parent et l’enfant. Plus de serveur Flask séparé.

## Pipeline

```
Excel (source)  →  CatalogueConverter  →  JSON  →  TtsApp (Kokoro / OpenVoice)  →  audio  →  catalogue de l’app
```

| Étape | Qui | Quoi |
| --- | --- | --- |
| 1. Source | Excel `stories/arbres/` | Texte des passages **et** paramètres de prosodie. On écrit ici. |
| 2. Conversion | `CatalogueConverter` + bouton *Excel → JSON* | Un JSON plat `stories/json/<story_id>.json`. |
| 3. Empreintes | `VoiceStudio` dans l’éditeur | Générer (genre / âge / tempérament) ou enregistrer au micro → `stories/voices/` + `voice_registry.json`. |
| 4. Parole | `ConversionQueue` + `ReplicaBook` | JSON → WAV, répliques éditables (régénérer / réenregistrer). |
| 5. App | parent / enfant | Le catalogue affiche les histoires **branchées sur les audio générés**. |

Le JSON n’est **pas** le manuscrit. L’Excel l’est. Le JSON n’est **pas** la voix. Le TTS l’est.

## Trois dossiers, pas une forêt

Un seul dossier par nature. **Pas** de sous-dossier par histoire. Les **noms de fichiers** portent l’histoire, la transition et le passage (IDs Excel, STRAT-003 : `T` = transition, `P` = passage).

| Dossier | Contenu | Nom de fichier |
| --- | --- | --- |
| `stories/arbres/` | Tous les Excel | `<story_id>.xlsx` — ex. `TREE-AUT-001.xlsx` |
| `stories/json/` | JSON générés + registre vocal | `<story_id>.json`, `voice_registry.json` |
| `poubelle/` | Rapports, pas du travail | `conversion_report.json` (gitignoré) |
| `stories/voices/` | Empreintes (référence OpenVoice) | `characters/character_amir.wav`, `defaults/narrator.wav` |
| `stories/audio/` | Audio des histoires | cible `<story_id>_<chunk_id>.wav` ; jobs d’atelier dans `app/data/tts_jobs/` |

Le `chunk_id` (`CHK_T0001_P0002_Q0001`…) identifie déjà transition et passage : inutile de recréer cette arborescence en dossiers.

**Aujourd’hui (à corriger plus tard, pas maintenant) :** le bake Piper pose encore `stories/audio/<story_id>/<chunk_id>.wav`. Cible = plat, préfixe `story_id_`. `stories/archive/arbres/` est un second tas Excel (ramifiés non live) : à fusionner dans `arbres/` quand on y touchera.

Le moteur de conversion **sait déjà** dériver ces noms : `story_id` = stem de l’xlsx, `chunk_id` = colonne Excel, JSON = `catalogue/stories/<story_id>.json` (à poser ici à plat dans `stories/json/`).

## Profil du parlant ≠ prosodie du passage

Toujours deux objets. La **source** des deux, pour une histoire, est l’Excel (texte + params). Le JSON les recopie pour le TTS.

### 1. Profil (permanent)

`stories/json/voice_registry.json` — identité **stable** d’un personnage, toutes histoires :

- `narrator`, `father`, `mother`, `teacher`
- `friend_boy` / `friend_girl`
- `character.amir`, `character.nina`, … (troupe D16)

Champs : `display_name`, `gender`, `age_group`, `role`, `kokoro_voice`, `reference_audio`, `voice_fingerprint`, `direction`.

On ne change pas le profil d’Amir d’une histoire à l’autre. Clonage commercial = autorisation vocale explicite.

### 2. Prosodie (cette réplique, dans l’Excel puis le JSON)

Dans l’xlsx : colonnes vocales du chunk (`script` / rôle, `notes`, pitch, volume, pauses, émotion, tempo…).  
Dans le JSON généré : `chunks[chunk_id].segments[]` :

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

Émotions : `neutral`, `calm`, `warm`, `joy`, `excited`, `focused`, `suspense`, `storytelling`, `sadness`, `anger`, `surprise`, `fear`, `whisper`.  
Intonations : `neutral`, `rising`, `falling`, `dramatic`, `storytelling`.  
`emphasis_words` : mots **présents** dans `text`.  
`pause_after_ms` ≠ `wait_ms` des questions (moteur de lecture).

`text` change → JSON et audio périmés (F-NAR-022).

## JSON (produit du moteur, pas un manuscrit)

Racine : `schema_version`, `story_id`, `title`, `language`, `catalogue`, `source`, `editorial_status`, `entry_chunk`, `speaker_profiles`, `chunks` (**objet** indexé par `chunk_id`).

Chunk : `kind`, `lesson_id`, `segments[]`, `interaction`, `options`, `night_policy`, `sound_cues`, `editorial_notes`, `next_chunk`, `default_next_chunk`.

Renderer TTS : l’éditeur (`POST /api/editor/convert`) ou, hors HTTP :

```python
from akomythatts import TtsApp
tts = TtsApp.assemble()
tts.convert(story_id="ATOM-AUT.AFF.001-01", assignments={})
```

## Conversion mécanique déjà faite : pas l’écriture

Le bundle `AkoMythaTTS-catalogue-tts.bundle` **ne se clone pas** (historique incomplet). Base du schema : AkoMythaTTS `feat/catalogue-tts-pipeline` @ `244ba22`.

Les 1 449 JSON convertis recopient l’xlsx avec une **prosodie générique**. Ce n’est pas la qualité visée. On n’importe pas les 168 Mo. Échantillons locaux : `voice_registry.json` + `TREE-AUT-001.json`.

## Éditeur (déjà dans l’app)

Branche `AkoMythaTTS`, page `#/admin/editeur`, API `/api/editor/`. Détail lancement : `app/README.md`.

## Ce qu’on fait maintenant

Améliorer la **qualité des histoires dans les Excel**. L’atelier vocal est branché dans l’app ; on n’aplatit pas encore tout le corpus en `stories/audio/<story_id>_<chunk_id>.wav` (Piper historique encore en sous-dossiers).
