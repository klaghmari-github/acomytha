# STRAT-002 — Audio : format, rythme, synthèse, chiffrement

**Référencé par :** `F-AUD-001` à `F-AUD-007`, `F-GEN-001`, `F-LOC-002`, `F-PLY-001`.  
**Graphe / IDs :** `STRAT-003`. **Lecture :** `STRAT-004`.

## 1. Décision format

| Étape | Format | Pourquoi |
| --- | --- | --- |
| Master de prod (disque atelier, jamais le téléphone) | WAV mono 24 kHz 16-bit | Sortie native Piper, sans perte, post-prod |
| Payload **dans** le blob chiffré | **MP3** mono 24 kHz **64 kbit/s** CBR | Décodé nativement iPhone, Samsung, Huawei, petit Android. Plus simple à livrer que WAV (10× plus lourd) ou AAC (fragmentation Huawei / vieux Android) |
| Fichier sur le téléphone | `{chunk_id}.chk` | **Pas** un `.mp3` : un lecteur galerie / Files ne joue rien |

Piper produit du WAV. Une ligne `ffmpeg` fait le MP3. Ce n’est pas plus difficile que du WAV ; c’est l’étape de **livraison**. On ne chiffre pas du WAV : trop gros pour les téléphones pauvres.

Opus est un peu plus petit. MP3 gagne sur **la compatibilité réelle** (exigence : Apple, Samsung, Huawei). On reste sur MP3.

## 2. Contrainte argent : Heavy seulement

L’abonnement **SuperGrok Heavy** paie le **chat / Grok Build** (plans de rythme, code, specs). Il **n’inclut pas** l’API `POST /v1/tts` (15 USD / M caractères). Consigne fondateur : **0 centime de plus**.

Donc :

| Passe | Outil | Coût |
| --- | --- | --- |
| 1. Enrichir le rythme (texte) | Heavy / Grok Build → `narration_plan` | Inclus Heavy |
| 2. Fabriquer les MP3 | **Piper CPU** sur la machine locale (8 cœurs, 30 Go RAM, 0 GPU requis) | 0 € |
| 3. Chiffrer, manifeste | Script local | 0 € |

On **n’appelle pas** l’API xAI TTS. Grok Voice dans l’app n’exporte pas 57 000 fichiers.

Piper : voix `fr_FR-siwis-medium` ou `fr_FR-tom-medium`, `length_scale` 1,15–1,35 selon N1–N3. Qualité « lisible », pas « comédien ». Suffisant pour le MVP si le plan de rythme est bon. Bench de 20 chunks **sur cette machine** avant de promettre une nuit pour tout le corpus.

Licence : moteur `piper1-gpl` **GPL-3.0** — on **n’embarque pas** Piper dans l’app, on embarque des MP3 chiffrés. Tracer la licence de **chaque voix** dans `licenses.json`.

XTTS-v2 : exclu (CPML non commercial).

## 3. Rythme : plan, pas de balises dans le texte enfant

Le JSON `text` reste du français quotidien. À côté, un `narration_plan` par chunk :

- régime : récit / choix / question / correction / conclusion
- pauses en ms **dans** l’audio (300–700 entre options)
- lent / doux / un mot d’emphase (`trottoir`)
- `wait_in_audio: false` — l’attente 3 s est au moteur, pas dans le MP3

Compilation Piper : phrases + silences ffmpeg + `length_scale`.  
Hypothèses WPM (à tester avec des enfants, pas des normes) : récit N1 110–130, question 100–115, conclusion 105–120.

Interdit dans l’audio enfant : cri, rire moqueur, musique qui couvre, volume brutal, chuchotement de peur.

Passe 1 (Heavy) : générer les plans pour le pilote, pas coller `[pause]` dans `text` (l’ASR et l’enfant verraient des scories).

## 4. Voix : narrateur ≠ personnages (F-AUD-006)

Le narrateur **raconte et décrit**. Les personnages **parlent**. On n’annonce plus « maman dit / papa dit » : le timbre suffit.

| Rôle | Timbre Piper (0 €) | Trait |
| --- | --- | --- |
| narrateur | `fr_FR-tom-medium` | adulte masculin, pose |
| maman | `fr_FR-siwis-medium` | adulte féminin |
| papa | `fr_FR-upmc-medium` speaker Pierre | adulte masculin ≠ narrateur |
| maîtresse / directrice | `fr_FR-upmc-medium` speaker Jessica | adulte féminin ≠ maman |
| directeur | `fr_FR-gilles-low` | adulte masculin posé |
| grand-mère | siwis, plus lent, pitch −3 | voix âgée |
| grand-père | gilles, plus lent, pitch −2 | voix âgée |
| héros fille | siwis, pitch +4 | enfant |
| héros garçon | tom, pitch +5 | enfant |
| copine / copain | jessica / pierre, pitch enfant différent du héros | pas la même voix que le héros |

Un chunk = un fichier audio, **mix** de répliques (`script` : `role\|phrase` par ligne). Colonne `text` = enchaînement sans « X dit ».

## 4b. Immersion : le monde s’entend (F-AUD-007)

**Règle générale, tout le corpus.** Dès qu’une action ou un décor est **raconté**, il est **entendu**. Parc, ambulance, chien, assiette qui tombe : ce sont des **exemples**, pas une liste fermée. Objectif : plonger l’enfant dans le monde de **chaque** histoire.

Colonne **`sons`** (feuille `chunks`) : liste d’ids, ou **vide = ce passage est silencieux**.

Ce n’est **pas** un fond sonore. On **n’écoute pas** et on **ne parle pas** en même temps.

Ordre dans le chunk : un peu de récit si besoin → **le bruit tout seul** → **reprise au calme**. Interdit : coller une nappe de parc / rue sous tout le texte.

Le lexique (`stories/outils/fx/lexique.json`) **grandit** avec le corpus. Le bake insère un beat `fx` après le premier récit, puis les répliques.

Décisions :

1. S’applique à **toutes** les histoires. `sons` vide = silence, c’est un cas normal.
2. Jamais de parole **dans** le bruit ; jamais d’histoire entière sur un background bruyant.
3. Mix **dans le chunk** au bake (un WAV/MP3).
4. Interdit : cri de peur, sirène collée à l’oreille, bruit méchant, musique qui couvre.
5. Nuit : atténuer ; skip ce qui réveille.
6. Bibliothèque locale, 0 € API. Ajouter un FX dès qu’un geste du récit n’a pas encore de son.

## 5. Protection

Objectif : un parent (ou un copain) qui copie le dossier `chunks/` n’obtient **pas** une bibliothèque MP3.

```
chunks/{chunk_id}.chk =
  header (version, story_id, chunk_id, codec=mp3, duration_ms)
  nonce
  ciphertext = AES-256-GCM(MP3)
  tag
```

- Clé d’histoire `K_story` tirée à la publication, enveloppée pour le compte parent (`K_wrap`) et déverrouillée par **Android Keystore / iOS Keychain** (biométrie ou code parental, jamais en clair dans les prefs).
- L’app déchiffre **un** chunk vers un buffer RAM, décode le MP3, joue, **efface** le buffer.
- Pendant la lecture de N, déchiffrement de N+1 (un seul chunk d’avance). Téléphones pauvres : ~200–400 Ko RAM par chunk à 64 kbit/s pour 20–40 s.
- **Interdit** d’écrire le MP3 déchiffré sur le disque (y compris cache « pour aller plus vite »).
- Checksum du ciphertext dans le manifeste. Tamponner ≠ sécurité cryptographique : le GCM authentifie.

Ce n’est pas une DRM de studio indestructible (un téléphone rooté peut dumper la RAM). C’est assez pour que Files / iTunes / WhatsApp ne voient pas des MP3 d’histoires.

## 6. Dossier plat

```
foret_locale/
  catalog.sqlite          # STRAT-003, lui aussi peut être chiffré au repos
  chunks/
    CHK_T0000_P0000.chk
    CHK_T0001_P0000.chk
    CHK_T0001_O0001.chk
    …
  manifest.json           # liste chunk_id → sha256, durées, story_id
```

Pas de `choix_ch1/brA/…`. L’identifiant **est** le chemin logique.

## 7. Pipeline de bake (0 € API)

```
JSON APPROVED_TEXT
  → narration_plan (Heavy, une fois par chunk)
  → Piper WAV
  → ffmpeg MP3 64k mono 24 kHz
  → loudness
  → AES-GCM → .chk
  → STRAT-001 audio
  → APPROVED_PACKAGE
```

Dry-run : nombre de chunks, minutes, Mo, **sans** synthèse. Cache : si `text_hash` + `narration_hash` + `engine_config_hash` inchangés, on ne refait pas le WAV.

## 8. Pilote avant forêt

1 ramifié + 12 atomiques, N1 et N3, **Piper seulement**, écoute réelle. Puis bake du corpus. Pas de fine-tune.
