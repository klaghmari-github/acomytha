# STRAT-003 — Modèle de données (histoires, leçons, chunks)

**Référencé par :** `F-NAR-001`, `F-NAR-007`, `F-DAT-001`, `F-TAX-001`, `F-TAX-002`, `F-FOR-001`.  
**Fichiers :** `stories/referentiel/lecons.xlsx` (catalogue) · `stories/referentiel/lecon_histoires.xlsx` (leçon → story_id → chunk_id pédagogiques).  
**Exécution :** `STRAT-004`.

## 1. Pourquoi relationnel + IDs path-encodés

Les parents cochent des **leçons**. Une leçon vit dans **plusieurs** histoires. Une histoire a 1 à 3 leçons. On duplique l’audio plutôt que de partager un chunk entre histoires (élagage et téléchargement simples).

Le graphe 3 × 3 × 3 tient dans l’**identifiant** du chunk : pas besoin d’une forêt de dossiers, et souvent pas d’une table d’arêtes. Une table d’arêtes existe **seulement** quand la convention ne suffit pas (question d’écoute, feedback).

**F-NAR-024 — fichiers plats.** `stories/arbres/` (xlsx), `stories/json/` (JSON + `voice_registry.json`), `stories/voices/` (empreintes), `stories/audio/` (WAV histoires). Noms `<story_id>.xlsx` / `<story_id>.json` / `<story_id>_<chunk_id>.wav`. Pas de sous-dossier par titre. Éditeur dans l’app : STRAT-005.

## 2. Identifiants

| Entité | Forme | Exemple |
| --- | --- | --- |
| Histoire | `STO_` + 5 chiffres | `STO_00001` |
| Leçon | déjà `DOM.SOUS.nnn` | `SEC.RUE.002` |
| Chunk | `CHK_` + chemin | ci-dessous |

L’`editorial_id` du corpus actuel (`TREE-SEC-001`, `ATOM-SAN.ALI.001-01`) reste en colonne. On n’écrase pas 1445 fichiers d’un coup : table de correspondance.

### Chemin encodé

Alphabet : `T` transition (branchement), `P` passage, `O` option parlée, `Q` question d’écoute.

| Chunk | ID | Sens |
| --- | --- | --- |
| Premier récit | `CHK_T0000_P0000` | Toujours. S’il manque, l’histoire est invalide. |
| 1re question de branche | `CHK_T0001_P0000` | Après la racine, **toujours** celui-là s’il y a un choix. |
| Option 1 / 2 / 3 (audio du mot) | `CHK_T0001_O0001` … `O0003` | Lus après la question, pauses moteur |
| Suite si l’enfant dit l’option 2 | `CHK_T0001_P0002` | |
| Question d’écoute dans cette suite | `CHK_T0001_P0002_Q0001` | Ne change **pas** la suite |
| Feedback ok / ko | `…_Q0001_FOK` / `…_Q0001_FKO` | Puis **même** suite |
| 2e branchement, après option 2 | `CHK_T0001_P0002_T0002_P0000` | |
| Option 3 de ce 2e choix | `CHK_T0001_P0002_T0002_O0003` | |
| 3e niveau | `CHK_T0001_P0002_T0002_P0003_T0003_P0000` | Max 3 `T` ≥ 1 |
| Fin | le `P` feuille n’a **pas** de `Txxxx_P0000` fils | « L’histoire est finie » est dans ce passage (ou `kind=ending`) |

**Règle de successeur (sans table, 90 % des cas) :**

1. On joue `…_P0000` racine (`T0000`). Successeur forcé : `CHK_T0001_P0000` s’il existe, sinon **fin** (histoire atomique sans choix : la racine enchaîne questions d’écoute puis ending dans le même schéma `T0000_P0000` → `T0000_P0000_Q0001` → ending nommé `CHK_T0000_P0000_END`).
2. Sur un `…_Tnnnn_P0000` (question de branche) : jour → attendre ; nuit → `default_option`. Réponse k → `…_Tnnnn_P000k`.
3. Après un passage `…_P000k` (k ≥ 1) : s’il existe `…_P000k_Q0001`, la jouer (jour seulement). Puis s’il existe `…_P000k_T{n+1}_P0000`, c’est le prochain branchement. **Sinon : fin.**

Atomique (pas de `choice_story`) :

```
CHK_T0000_P0000          récit
CHK_T0000_P0000_Q0001    question de leçon (écoute, ne branche pas)
CHK_T0000_P0000_Q0001_FOK / FKO
CHK_T0000_P0000_END      conclusion
```

## 3. Tables SQLite (catalogue appareil + atelier)

```sql
lesson (
  lesson_id        TEXT PRIMARY KEY,  -- SEC.RUE.002
  title            TEXT NOT NULL,
  domain           TEXT NOT NULL,
  framing          TEXT NOT NULL,
  age_bands        TEXT NOT NULL,     -- N1,N2,N3
  version          INTEGER NOT NULL
);

story (
  story_id         TEXT PRIMARY KEY,  -- STO_00001
  editorial_id     TEXT UNIQUE,       -- TREE-SEC-001
  title            TEXT NOT NULL,
  kind             TEXT NOT NULL,     -- atomic | ramifiee
  age_band         TEXT NOT NULL,
  version          INTEGER NOT NULL,
  default_option   INTEGER NOT NULL DEFAULT 1,
  night_skip_branch INTEGER NOT NULL DEFAULT 1,
  status           TEXT NOT NULL      -- APPROVED_TEXT | APPROVED_AUDIO | APPROVED_PACKAGE
);

story_lesson (
  story_id         TEXT NOT NULL,
  lesson_id        TEXT NOT NULL,
  role             TEXT NOT NULL,     -- principal | secondaire
  PRIMARY KEY (story_id, lesson_id)
);

chunk (
  chunk_id         TEXT PRIMARY KEY,  -- CHK_…
  story_id         TEXT NOT NULL,
  kind             TEXT NOT NULL,     -- passage | transition_question | transition_option
                                      -- | listen_question | feedback_ok | feedback_ko | ending
  option_index     INTEGER,           -- 1..3 pour O et P de branche
  night_policy     TEXT NOT NULL,     -- play | skip | auto_default
  default_option   INTEGER,           -- sur transition_question
  duration_ms      INTEGER NOT NULL,
  text_hash        TEXT NOT NULL,
  narration_hash   TEXT NOT NULL,
  engine_config_hash TEXT NOT NULL,
  audio_hash       TEXT NOT NULL,     -- sha256 du .chk
  file_name        TEXT NOT NULL      -- CHK_….chk
);

-- Uniquement si la convention d'ID ne suffit pas (écoute, feedback, exception).
chunk_link (
  story_id         TEXT NOT NULL,
  from_chunk_id    TEXT NOT NULL,
  intent           TEXT NOT NULL,     -- match | wrong | timeout | next
  to_chunk_id      TEXT NOT NULL,
  PRIMARY KEY (from_chunk_id, intent)
);
```

Téléchargement parent : `SELECT story_id FROM story_lesson WHERE lesson_id IN (leçons cochées)` puis **tous** les chunks de ces `story_id`. Pas de chunk partagé entre deux `story_id`.

## 4. Duplication volontaire

« Traverser avec l’adulte » dans deux histoires = deux jeux de chunks, deux récits. Ça coûte des Mo, ça évite un graphe global impossible à élaguer.

## 5. Correspondance JSON actuel → chunks

Le `stories/schema.json` (`audio`, `choice_story`, `question_lesson`, …) reste la **source texte**. Un compilateur (`F-NAR-007`) pose les `chunk_id` :

| JSON | Chunks |
| --- | --- |
| `audio` racine | `CHK_T0000_P0000` |
| `choice_story` | `…_Tnnnn_P0000` + un `…_O000k` par option |
| `audio` après option | `…_Tnnnn_P000k` |
| `question_lesson` / `question_comprehension` | `…_Q0001` + FOK/FKO |
| `ending` | `…_END` ou `kind=ending` sur le dernier `P` |

On ne maintient pas deux graphes à la main.
