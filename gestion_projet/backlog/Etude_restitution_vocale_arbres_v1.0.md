# Étude — Restitution vocale des arbres d’histoires Sentier

**Document :** ETU-AUD-001  
**Version :** 1.0  
**Date :** 3 septembre 2026  
**Statut :** étude de cadrage, pas une spécification figée  
**Public :** fondateurs, éditorial, production audio, technique  
**Sources :** spec fonctionnelle v2.0 (AUD-001 à AUD-003, GEN-003), validation VAL-HIST-001, schéma `stories/schema.json`, corpus `feat/F-GEN-001-corpus-histoires` (685 atomiques + 760 ramifiées = 1445 arbres).  
**Contrainte machine :** ~3,8 Go VRAM GPU, ~30 Go RAM, 8 cœurs CPU. Pas de gros LLM local.

---

## 0. Verdict en une page

**Objectif.** Chaque nœud d’un arbre JSON devient un (ou plusieurs) fichiers audio. L’enfant entend une histoire, une question ou un choix, puis une branche. À la feuille : une conclusion qui reformule la leçon. Rien n’est généré pendant l’écoute (GEN-001).

**Recommandation.**

| Couche | Choix | Pourquoi |
| --- | --- | --- |
| Texte à dire | **SSML 1.1** (W3C) + un profil Sentier (`sentier-prosody-v1`) | Format le plus universel. Piper, Kokoro, cloud, Grok, Azure, Google le comprennent ou s’y mappent. Le rythme vit **dans le texte**, pas dans un modèle unique. |
| Synthèse locale pilote | **Piper** (CPU, ONNX) voix `fr_FR-siwis-medium` ou `fr_FR-tom-medium` | Tient largement dans 3,8 Go (en pratique 0 GPU). ~10× temps réel sur 8 cœurs. Qualité « lisible » pour un enfant, pas encore « conteur ». |
| Qualité / voix unique | **Kokoro-82M** (CPU ou GPU, ~0,4–0,8 Go VRAM) | Meilleur rapport naturel / ressources. Français imparfait (peu d’heures d’entraînement), à tester. Fine-tune léger possible, pas un clone expressif. |
| Clone de voix / expressivité | **XTTS-v2** en **lot nocturne**, FP16, chunks courts | ~2–4 Go VRAM : **juste** sur 3,8 Go. Pas de LLM. Fine-tune sérieux **impossible** à 3,8 Go. Inférence possible, lente, risquée (OOM). |
| Déléguer à Grok | **Oui pour le pilote Parc (12 leçons, 1 arbre)** | Qualité de conteur, prompt unique, zéro install. Coût = files d’attente + re-téléchargement + **pas de SSML figé** (reproductibilité faible). Le volume total (milliers de fichiers) n’est pas un job « une nuit Grok » sans API TTS dédiée et quota. |

**Temps d’ordre de grandeur pour tout le corpus actuel** (voir §5 pour le détail) : environ **260 heures d’audio unique** à produire.

| Voie | Temps machine estimé | Commentaire |
| --- | --- | --- |
| Piper, 8 cœurs, fichiers indépendants en parallèle | **4 à 12 heures** | Le plus prévisible. Qualité moyenne. |
| Kokoro CPU 8 cœurs, parallèle | **15 à 40 heures** | Plus naturel. Français à valider. |
| XTTS-v2 sur 3,8 Go VRAM, séquentiel | **4 à 15 jours** | Si ça tient en VRAM. Sinon CPU = semaines. |
| Grok / API cloud, 1 fichier / quelques secondes | **1 à 4 jours** calendaires | Plus le temps humain de relire et de ranger. Re-génération si le texte bouge (AUD-001). |

**Décision proposée pour le MVP.**

1. Figer un **profil SSML Sentier** dans chaque nœud (`ssml` à côté de `text`).
2. Produire le **pilote TREE-PARC / 12 leçons** deux fois : Grok (référence qualitative) et Piper (référence reproductible).
3. Écouter les deux. Si Piper + SSML suffit pour N1, on industrialise en local. Si l’écart est trop grand, on réserve Grok (ou un cloud) aux nœuds « choix » et « conclusion », Piper au récit.
4. On **n’entraîne pas** un gros TTS sur cette machine. On peut au mieux adapter Piper/Kokoro (quelques heures de voix lue, pas un LLM).

---

## 1. Ce que l’enfant doit entendre

L’expérience n’a **pas d’image** (NAR-004, AUD-001). Tout passe par la voix.

### 1.1 Trois régimes de parole

| Régime | Quand | Vitesse cible | Intonation | Pauses |
| --- | --- | --- | --- | --- |
| **Récit** | nœuds `audio`, `transition` | N1 : 110–130 mots/min. N2 : 125–145. N3 : 135–155. | Chaude, phrases courtes, noms répétés. Monte un peu sur un bruit, un goût, un geste. | 400–700 ms en fin de phrase. 800–1200 ms au changement de lieu. |
| **Choix / question** | `choice_story`, `question_lesson`, `question_comprehension` | **Plus lent** que le récit (−15 à −25 %). | Monte sur chaque option. Isole les options. Ne jamais enchaîner les trois mots comme une liste plate. | **Silence 1,2–1,8 s après la question.** Relance plus courte, encore plus lente. |
| **Leçon / conclusion** | `feedback`, `wrong_feedback`, `ending` | Lent, posé, **sans dramatiser**. | Un peu plus grave. Une idée = une phrase. On **répète la conduite sûre**, jamais le danger. | Pause avant la formule de leçon. Pause après. Fin : descente, pas un sourire forcé. |

Un adulte lit à ~170–190 mots/min. Un enfant de 3–4 ans **perd** au-delà de ~130. Trop lent (sous 100) endort. La consigne n’est pas « magique » : c’est une plage, mesurée ensuite sur l’audio réel (AUD, durées min/moy/max).

### 1.2 Anti-monotonie (sans spectacle)

Le cerveau d’un enfant de maternelle décroche si le même contour mélodique revient 40 fois. On varie **sans crier**.

| Levier | Usage | Interdit |
| --- | --- | --- |
| Accélérer 5–8 % | Bruit, jeu, course **dans l’espace autorisé** (parc, jardin) | Accélérer une consigne de sécurité |
| Ralentir 15–25 % | Pied sur le trottoir, main, « on attend », « on dit stop » | Dramatiser (« attends… le danger… ») |
| Monte légère | Appel du prénom, option de choix | Cri, surprise violente |
| Descente | Fin de scène, conclusion de leçon | Voix triste / coupable |
| Chuchotement très léger | Secret de surprise **gentille** (FAM.SEC.001) seulement | Peur, malaise, « secret qui se cache » |
| Onomatopée courte | `toc toc`, `miaou`, pluie — **une fois** | Bruitage qui masque la consigne (AUD-002) |

**Règle d’or sécurité (`positive_only_critical`).** Le nœud de leçon (feu, trottoir, prises, balcon, rester assis) est **toujours** en régime lent + clair. On ne « joue » pas le rythme ici. Le jeu rythmique est pour le récit autour.

### 1.3 Que dire à une intersection (choix)

Le nœud `choice_story` n’est **pas** un test moral. Les options sont narratives (lieu, objet, camarade). La voix doit :

1. **Refermer** la scène précédente (une phrase, descente).
2. **Appeler** l’enfant par rien d’autre que le prénom du héros, ou « et toi » — pas « dis-moi vite ».
3. **Annoncer** qu’il y a un choix : « On peut aller… »
4. **Poser les options une par une**, avec le même poids (aucune n’est « la bonne »).
   - « …dans la cuisine. » *(pause 500 ms)*
   - « …dans le jardin. » *(pause 500 ms)*
   - « …ou dans la chambre. » *(pause 1,5 s)*
5. **Attendre.** Fichier audio **sans** la suite. Le moteur joue ensuite `silence_check` / relance / `default_next`.

Relance (`retry_prompt`) : plus courte, plus lente, **mêmes options**, pas une nouvelle formulation qui change le sens.

Question de leçon (`question_lesson`) : une seule question, réponse 1–3 mots. Après erreur : **uniquement** la conduite sûre (`wrong_feedback`). La voix de correction n’est jamais moqueuse, jamais plus rapide.

### 1.4 Conclusion (feuille)

À la place d’une transition : un fichier `conclusion`.

Structure orale obligatoire (preuve pédagogique PED-010) :

1. Ce qui s’est passé (1–2 phrases, régime récit calme).
2. La conduite sûre, affirmative (`safe_actions`).
3. Les `required_messages` reformulés, sans jargon.
4. Fermeture : « L’histoire est finie. » Descente. Pas de « à demain » commercial.

---

## 2. Arborescence des dossiers audio

Un JSON = un **arbre**. La forêt = le dossier parent. Les branches = des sous-dossiers. Le moteur d’écoute n’a qu’à suivre les chemins de fichiers ; il ne mélange pas.

### 2.1 Contrat de noms

```
foret/
  <tree_id>/                          # un arbre indépendant
    manifest.json                     # mapping node_id → fichiers
    racine.wav                        # nœud root (type audio)
    ...                               # autres nœuds « avant le 1er choix » à plat
    choix_<nodeId>/                   # un dossier par nœud choice_story
      transition.wav                  # le prompt du choix (les options)
      relance.wav                     # optionnel, retry
      <optionId>/                     # une branche = un sous-dossier
        scene.wav                     # audio de la branche
        question.wav                  # si question_lesson
        question_relance.wav
        feedback_ok.wav
        feedback_ko.wav
        choix_<nodeId>/               # récursion, max 3 niveaux
          transition.wav
          <optionId>/
            ...
            conclusion.wav            # feuille (ending) : plus de transition
```

**Atomique** (pas de `choice_story`) : pas de sous-dossiers de branches.

```
foret/
  ATOM-SAN.ALI.001-01/
    manifest.json
    racine.wav
    question.wav
    question_relance.wav
    feedback_ok.wav
    feedback_ko.wav
    conclusion.wav
```

**Ramifié** (exemple réel `TREE-SEC-001`, nœuds `root → ch1 → brA|brB|brC → … → endA1X`) :

```
foret/
  TREE-SEC-001/
    manifest.json
    racine.wav
    choix_ch1/
      transition.wav
      brA/
        scene.wav
        question.wav
        question_relance.wav
        feedback_ok.wav
        feedback_ko.wav
        choix_ch2A/
          transition.wav
          brA1/
            scene.wav
            choix_ch3A1/
              transition.wav
              endA1X/
                conclusion.wav
              endA1Y/
                conclusion.wav
              endA1Z/
                conclusion.wav
          brA2/ ...
          brA3/ ...
      brB/ ...
      brC/ ...
```

### 2.2 Règles d’implémentation

- Un dossier porte **l’id du nœud** (stable, déjà dans le JSON). On ne traduit pas en français dans le chemin (`brA` reste `brA`).
- `transition.wav` = ce que l’enfant entend **pour choisir**. Jamais la suite de la branche.
- `conclusion.wav` **remplace** `transition.wav` dès que `type == ending`. Pas les deux.
- `feedback_ok.wav` / `feedback_ko.wav` : fichiers distincts. Le ko ne contient que la conduite sûre (POS-005).
- `manifest.json` relie `node_id` + rôle (`racine|scene|transition|relance|question|feedback_ok|feedback_ko|conclusion`) + checksum + durée réelle. C’est ce que le validateur audio lit (AUD-001, AUD-002).
- Format fichier MVP : **WAV 22,05 kHz mono 16-bit** (Piper natif) ou **WAV 24 kHz** (Kokoro). L’app transcode en Opus au paquet. On ne mixe pas les fréquences dans un même arbre.
- Une version de texte = une version d’audio. Si le JSON bouge, le dossier audio est **invalide** (AUD-001). On régénère l’arbre entier, pas un fichier isolé « à la main » sans bump de version.

### 2.3 Mapping nœud JSON → fichiers

| `node.type` | Fichiers | Dossier |
| --- | --- | --- |
| `audio` (root) | `racine.wav` | racine de l’arbre |
| `audio` (après un choix) | `scene.wav` | dossier de l’option |
| `choice_story` | `transition.wav` (+ `relance.wav` si retry) | `choix_<id>/` |
| `question_lesson` / `question_comprehension` | `question.wav`, `question_relance.wav`, puis les feedbacks | même dossier que la scène |
| `feedback` | `feedback_ok.wav` (le `text` du nœud) | même dossier |
| `ending` | `conclusion.wav` | dossier feuille, **plus de sous-dossier** |
| `silence_check` | pas d’audio (silence moteur) | — |
| `transition` (type JSON) | `scene.wav` court, pas un choix | même dossier |

---

## 3. Le rythme dans le texte : SSML, pas un LLM

### 3.1 Pourquoi ne pas « laisser le modèle improviser l’intonation »

- Un TTS neural **sans** balises produit une courbe moyenne. Deux moteurs ≠ deux lectures.
- Grok (ou tout LLM audio) peut bien raconter **une** fois, et autrement à la régénération. L’enfant et le validateur ont besoin d’**une** version figée.
- La spec exige des durées **mesurées** (min / moy / max par chemin). Improviser casse les durées.

Donc : le texte enfant reste du français quotidien. **À côté**, un champ `ssml` (ou un fichier `.ssml` jumeau) porte le rythme. Le TTS, quel qu’il soit, consomme le SSML. Si un moteur ignore une balise, on dégrade en pauses explicites (`<break>`), qui passent presque partout.

### 3.2 Format retenu : SSML 1.1 (W3C) + profil Sentier

C’est le langage le plus **universel** et le plus **riche** encore lu par des moteurs grand public (Google, Amazon, Microsoft, Apple, beaucoup d’ONNX via préprocesseur).

Profil `sentier-prosody-v1` — sous-ensemble autorisé (volontairement petit) :

| Balise | Usage Sentier |
| --- | --- |
| `<speak>` | racine |
| `<p>` `<s>` | paragraphe / phrase = nos phrases courtes déjà écrites |
| `<break time="400ms"/>` etc. | **seul levier obligatoire.** 400 fin de phrase récit ; 800 lieu ; 1500 après une question |
| `<prosody rate="slow">` | leçon, choix, conclusion. Valeurs : `x-slow` / `slow` / `medium` uniquement |
| `<prosody pitch="low">` | conclusion, conduite sûre |
| `<prosody pitch="medium">` | défaut |
| `<emphasis level="moderate">` | un mot de leçon (`trottoir`, `main`, `stop`) — **un par phrase max** |
| `<say-as interpret-as="characters">` | jamais (épeler = trop scolaire) |
| `<audio>` | jamais dans le MVP (bruitages = fichiers séparés, mixés après, volume bas) |
| `<prosody volume="loud">` | **interdit** (effraie, masque) |

Exemple — choix :

```xml
<speak>
  <s>Sami a bien attendu.</s>
  <break time="700ms"/>
  <s>On peut prendre le seau.</s>
  <break time="500ms"/>
  <s>Ou le doudou.</s>
  <break time="500ms"/>
  <s>Ou le ballon.</s>
  <break time="1500ms"/>
</speak>
```

Exemple — leçon critique :

```xml
<speak>
  <prosody rate="slow">
    <s>Les pieds restent <emphasis level="moderate">sur le trottoir</emphasis>.</s>
    <break time="600ms"/>
    <s>On attend, la main dans la main.</s>
  </prosody>
</speak>
```

### 3.3 Plan B si un moteur n’avale pas le SSML

Compilation vers un **texte à pauses ASCII** :

- `/` = 400 ms  
- `//` = 800 ms  
- `///` = 1500 ms  
- `*mot*` = légère emphase (si le moteur a un token ; sinon ignoré)

C’est moins riche, mais Piper / eSpeak / beaucoup de VITS l’acceptent si on pré-insert des silences en post-prod (sox / ffmpeg `silencedetect` + concat). **La source de vérité reste le SSML.** Le texte ASCII est un artefact de build.

### 3.4 Entraîner un synthétiseur « conteur » sur cette machine

| Travail | Faisable à 3,8 Go VRAM + 30 Go RAM ? | Temps / donnée |
| --- | --- | --- |
| Rien (Piper/Kokoro off-the-shelf) | Oui | 0 |
| Ajuster vitesse/pitch Piper (config JSON, pas de training) | Oui | minutes |
| Fine-tune Piper/VITS sur 20–60 min de voix lue (même locuteur, français enfantin) | **Limite CPU** : possible en lot long. GPU 3,8 Go : batch 1, lent, quelques **jours à semaines** | Il faut un locuteur + alignement |
| Fine-tune Kokoro (StyleTTS2, 82 M) | Possible en théorie, **pas documenté comme simple** ; VRAM ok, stabilité non garantie | jours |
| Fine-tune XTTS-v2 | **Non raisonnable.** Les recettes officielles OOM même à 8–12 Go en batch > 1 | — |
| Entraîner un TTS from scratch / un LLM audio | **Non.** | — |
| Cloner une voix (6 s) avec XTTS **sans** fine-tune | Peut-être, FP16, chunks < 15 s, surveillance OOM | inférence seulement |

**Conclusion training.** On n’achète pas la musicalité du conte par un fine-tune sur cette machine. On l’achète par **le SSML + un bon lecteur de référence** (Grok ou comédien) sur un petit corpus, puis on cale Piper/Kokoro pour s’en rapprocher. Si un jour on clone une voix : XTTS en **inférence** nocturne, pas en training.

---

## 4. Prompt Grok (production audio)

À coller tel quel pour un arbre. Un appel = **un nœud** (pas l’arbre entier : les fichiers doivent matcher le dossier).

```
Tu es le conteur de Sentier. Public : enfant de {N1|N2|N3} (3–6 ans). Audio seulement, pas d’image.

VOIX
- Français quotidien, articulation nette, un peu plus lente qu’un adulte.
- Chaude, calme, jamais moqueuse, jamais effrayée, jamais « dessin animé criard ».
- N1 : très posé, beaucoup de pauses. N3 : un peu plus de vie, jamais précipité.

RÉGIME : {recit | choix | question | correction | conclusion}

RÈGLES
- Si régime = choix : chaque option isolée, même poids, pause longue à la fin. Aucune option n’est « la bonne ».
- Si régime = question : une question, puis silence. Relance = plus courte, plus lente.
- Si régime = correction : seulement la conduite sûre. Ne pas décrire un geste dangereux.
- Si régime = conclusion : leçon affirmative + « L’histoire est finie. » Descente.
- Si framing = positive_only_critical : ralentir sur pieds / mains / trottoir / adulte. Pas de jeu rythmique.
- Interdit : musique dominante, cri, rire sarcastique, bruitage qui couvre les mots, religion, politique, deux papas/mamans.

TEXTE À DIRE (respecte les pauses du SSML s’il est fourni) :
{ssml_ou_texte}

Génère un unique fichier audio WAV, voix unique pour tout l’arbre, même locuteur que les autres nœuds de {tree_id}.
```

**Limite actuelle.** Dans Grok Build (cette session), il n’y a **pas** d’outil TTS exposé (seulement image / vidéo). Déléguer à Grok suppose : l’app Grok vocale, une API xAI TTS quand elle existe, ou un export manuel. L’étude traite Grok comme **voie qualitative de référence**, pas comme un bouton déjà branché ici.

Pour un arbre ramifié 3×3×3 : **~60–70 appels** (un par fichier). Pour 760 ramifiées : **~50 000 appels**. Ce n’est industrialisable que si l’API est batchable et que le dossier est écrit par un script, pas à la main.

---

## 5. Volume réel du corpus (septembre 2026)

Chiffres du dépôt `feat/F-GEN-001-corpus-histoires`.

| | Atomiques | Ramifiées | Total |
| --- | --- | --- | --- |
| Arbres | 685 | 760 | **1445** |
| Fichiers audio uniques (estimation haute, 1 fichier / champ parlé) | ~4 800 | ~52 000 | **~57 000** |
| Durée unique estimée | ~23 h | ~240 h | **~260 h** |

Détail ramifié (59 nœuds types TREE-SEC-001, champs parlés éclatés) :

- 13 `audio` + 27 `ending` + 3 `feedback` + 13 prompts de choix + 3 questions × (prompt + retry + ok + ko) ≈ **68 fichiers / arbre**.
- Durée moyenne par fichier ~15–25 s → ~19 min d’audio unique / arbre (beaucoup plus que la durée d’**un** chemin enfant, ~3–8 min, parce qu’on enregistre **toutes** les branches).

Le paquet enfant ne télécharge pas 19 min : il télécharge les fichiers des chemins possibles, ou tout l’arbre compressé. Opus 24 kbit/s × 19 min ≈ **3,4 Mo / arbre ramifié**. 760 arbres ≈ **2,6 Go** forêt complète. Atomiques : 685 × ~2 min × 24 kbit/s ≈ **250 Mo**. Forêt totale audio ≈ **3 Go** (hors WAV de master, 10× plus lourds).

Masters WAV 22 kHz mono 16-bit : ~2,6 Mo / minute → 260 h × 156 Mo/h ≈ **40 Go** de masters. À garder hors téléphone, sur le disque de prod.

---

## 6. Synthétiseurs locaux vs Grok — ressources et temps

Machine : **3,8 Go VRAM, 30 Go RAM, 8 cœurs.** On ne fait **pas** tourner un LLM 7B+ en même temps que le TTS.

### 6.1 Tableau

| Moteur | VRAM | RAM | RTF typique (1 = temps réel) | Qualité conte FR | SSML | Training ici | Temps corpus 260 h audio |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **eSpeak-NG** | 0 | ~20 Mo | 0,001 | Inacceptable (robot) | Partiel | Non | < 30 min — **à écarter pour l’enfant** |
| **Piper ONNX** (siwis/tom medium) | 0 (CPU) | ~200–400 Mo | 0,05–0,12 sur 8 cœurs (≈ 8–20× plus vite que le temps réel) | Lisible, un peu plate | Faible natif ; on injecte des `<break>` en pré/post | Fine-tune VITS lourd ; **config rate/pitch = oui** | **4–12 h** parallèle |
| **Kokoro-82M** | ~0,4–0,8 Go | ~1–3 Go | CPU 8 cœurs ~0,3–0,6 (≈ 2–3× temps réel) ; GPU petit ~0,05 | Bonne en EN ; **FR moyen** (peu d’heures, voix `ff_siwis`) | Via phonèmes + pauses | Fine-tune délicat, VRAM ok, savoir-faire élevé | **15–40 h** CPU parallèle |
| **MeloTTS** | ~1 Go | ~2–4 Go | ~0,1 GPU / plus lent CPU | Correct multilingual | Limité | Non prioritaire | 1–3 jours |
| **XTTS-v2** clone | **~2–4 Go** (juste) | 8 Go+ | GPU 3,8 Go : ~0,5–2 (parfois plus lent que le temps réel) ; CPU : 5–20 | Bon si voix source claire | Faible | Fine-tune **non** (OOM) | **4–15 jours** GPU si stable ; sinon abandon |
| **Bark / F5 / Dia** | 6–14 Go | élevé | Lent | Expressif | Non | Non | **Hors machine** |
| **Grok / cloud TTS** | 0 local | 0 | File d’attente | Potentiellement le meilleur conteur | Si l’API prend SSML : oui ; sinon non | Non | **1–4 jours** + relectures ; risque de quota |

RTF = *real-time factor*. 0,1 = 1 minute d’audio en 6 secondes.

### 6.2 Piper en détail (candidat n°1 local)

- Tourne sur Raspberry Pi 4 : **largement** dans 8 cœurs / 30 Go.
- Voix FR : `fr_FR-siwis-medium` (~50 Mo, plus régulière en prose), `fr_FR-tom-medium` (plus chaude). Tester les deux sur N1.
- Pas besoin du GPU. On **garde les 3,8 Go libres** (ou éteints).
- Contrôle du rythme : `length_scale` (vitesse), `noise_scale` (variété). Un `length_scale` 1,15–1,30 pour N1. Pour les choix : 1,35.
- SSML : Piper ne parse pas tout. **Build step** : SSML → liste de phrases + silences ffmpeg (`aevalsrc=0` / `anullsrc`) concatenés. C’est fiable.
- Entraînement : possible (VITS) mais c’est un projet à part (données, alignement Montreal Forced Aligner, jours de GPU **plus gros** que 3,8 Go). Hors MVP.

**Calcul Piper.** 260 h d’audio, RTF 0,08, un processus. Temps = 260 × 0,08 = **21 h**. Huit workers sur des fichiers indépendants, efficacité ~50–70 % (disque) → **5–10 h**. Marge disque / échecs : afficher **une nuit (12 h)**.

### 6.3 Kokoro en détail (candidat n°2 local)

- 82 M paramètres, StyleTTS2, Apache-2.0.
- VRAM FP16 ~400–800 Mo : **entre largement** dans 3,8 Go.
- CPU : ~2–6× temps réel sur un laptop récent ; sur 8 cœurs desktop, viser 2–3×.
- Français : pack `ff_siwis`, **moins de 11 h** de data — note B−. Risque d’accent / phonèmes FR faibles (`eu`, `un`, liaisons).
- Temps corpus : 260 / 2,5 ≈ **100 h** séquentiel CPU ; parallèle 6 jobs → **20–40 h**.

À n’adopter que si un test d’écoute FR enfant (10 nœuds pilotes) passe le seuil « on comprend du premier coup ».

### 6.4 XTTS-v2 (clone, pas un LLM)

- Utile **seulement** si on a une voix de conteur (parent, comédien, ou piste Grok de référence) à cloner.
- 3,8 Go = **minimum vital** en FP16, chunks **< 12–15 s**. Un nœud trop long = OOM. D’où le découpage nœud-par-nœud, déjà dans le contrat dossiers.
- Fine-tune : non. Clone 6 secondes : oui, à tester.
- Temps : si RTF 1,0 sur cette carte, **260 h** = 11 jours non-stop. Si RTF 0,5, **5,5 jours**. Fragile.

### 6.5 Grok / API

| Pour | Contre |
| --- | --- |
| Intonation de conteur sans fine-tune | Pas d’outil TTS dans Grok Build aujourd’hui |
| Zéro VRAM | ~57 000 fichiers = industrialisation API, pas un chat |
| Bon pour le **pilote** (1 arbre, ~70 fichiers) | Reproductibilité : un re-roll ≠ le même audio |
| | Si le JSON change, tout refaire (AUD-001) |
| | Coût / quota inconnus ; files d’attente |
| | Moins bon pour figer le SSML (le modèle ignore souvent les balises) |

**Temps Grok réaliste.** 70 fichiers pilote : une session, **1–3 heures** humain+machine. Corpus entier : sans API batch, **ce n’est pas un plan**. Avec API à 1 fichier / 2 s : 57 000 × 2 s ≈ **32 h** de file brute, plus erreurs, plus rangement. Compter **3–5 jours** calendaires.

---

## 7. Scénarios de réalisation

### Scénario A — Local Piper + SSML (recommandé pour industrialiser)

1. Ajouter `ssml` (ou compiler depuis le texte + type de nœud) dans le schéma.
2. Script `stories/outils/render_audio_tree.py` : JSON → arborescence `foret/<tree_id>/` + WAV Piper + `manifest.json`.
3. Concat silences selon le profil.
4. Mesurer durées, ASR optionnel plus tard (VAL-AUD-002).
5. **Durée projet :** 2–4 jours de script + une nuit de rendu corpus + 2 jours d’écoute spot (pas 57 000 écoutes humaines : échantillon + validateurs).

### Scénario B — Grok référence, puis Piper de masse

1. 1 arbre pilote (Parc) + 12 leçons atomiques : Grok.
2. Caler le profil SSML pour que Piper **imite** les pauses du master Grok (on aligne les `<break>` sur le master, pas la timbre).
3. Reste du corpus : Piper.
4. **Durée :** 1 semaine de calage + une nuit de rendu.

### Scénario C — Tout Grok

1. Seulement si une API TTS xAI existe et accepte le batch.
2. Sinon : irréaliste à 57 000 fichiers.
3. **Durée :** inconnue ; planifier comme un prestataire externe, pas comme un overnight local.

### Scénario D — XTTS clone d’une voix Grok

1. Faire lire 3 minutes par Grok (ou un humain).
2. Cloner. Générer le corpus en chunks.
3. **Durée :** 1–2 semaines machine + stress VRAM. Plan B obligatoire (Piper) si OOM.

---

## 8. Plan de travail (sans bloquer le MR histoires)

Le MR `F-GEN-001` (textes) peut partir **sans** audio. L’audio est `F-AUD-001`.

| Étape | Livrable | Condition de sortie |
| --- | --- | --- |
| 1. Schéma | Champ `ssml` optionnel + `audio_role` | JSON encore valides sans SSML |
| 2. Profil | `sentier-prosody-v1.md` (cette étude §3.2) | 1 page, exemples choix / leçon / fin |
| 3. Maquette dossiers | Script qui **crée l’arbre vide** + `manifest.json` pour TREE-SEC-001 et 1 atomique | `tree` Unix = contrat §2 |
| 4. Bake Piper | WAV remplis, 1 atomique + 1 ramifié | Écoute N1 : mots compris |
| 5. Bake Grok (manuel) | Mêmes nœuds | Écoute comparative A/B |
| 6. Décision | Piper seul / hybride / Grok pilote | Compte-rendu 1 page |
| 7. Nuit corpus | Uniquement si étape 6 = local | Checksums + durées dans le manifeste |
| 8. VAL-AUD | ASR plus tard, pas bloquant pour la maquette | Spec déjà écrite |

---

## 9. Risques

| Risque | Gravité | Mitigation |
| --- | --- | --- |
| Piper trop plat, enfant décroche | Majeure | Hybride : Grok sur choix+conclusions ; ou Kokoro si FR ok |
| Kokoro FR illisible (`un`, liaisons) | Majeure | Test 20 phrases avant tout corpus |
| XTTS OOM à 3,8 Go | Majeure | Chunks 12 s max ; fallback Piper automatique |
| 40 Go de WAV masters | Mineure | Disque ; garder Opus dans le paquet app |
| Grok non reproductible | Bloquante pour VAL-AUD | SSML + moteur déterministe = source ; Grok = référence d’écoute seulement |
| Bruitages trop présents | Bloquante AUD | Pas de `<audio>` dans le SSML enfant |
| Monotonie 27 fins d’un même arbre | Majeure | SSML différent par feuille (pause, mot d’ancrage) même si le texte se ressemble |

---

## 10. Réponse directe aux questions posées

**Comment restituer vocalement un arbre ?**  
Un fichier par champ parlé, dossiers = branches, `transition.wav` aux intersections, `conclusion.wav` aux feuilles. Voix unique par arbre. Régimes récit / choix / leçon. Voir §1–2.

**Intonation, rythme, clarté enfant.**  
110–155 mots/min selon N1–N3. Plus lent aux choix et aux leçons. Pauses chiffrées. Emphase d’un seul mot de conduite sûre. Pas de cri. §1.

**Prompt Grok.**  
§4. Un nœud à la fois, régime explicite, même locuteur.

**Dossier par JSON, sous-dossiers = branches.**  
§2. Forêt → arbres → `choix_*` → options → conclusions.

**Temps Grok vs open-source low-resource.**  
§5–6. Piper : une nuit. Kokoro : 1–2 jours. XTTS : une à deux semaines si ça tient. Grok : 3–5 jours avec API ; irréaliste à la main.

**Ressources synthétiseur.**  
Piper : CPU only, < 0,5 Go RAM. Kokoro : < 1 Go VRAM. XTTS : 2–4 Go, juste. Bark/F5 : non.

**Entraîner pour le rythme.**  
Pas un LLM. SSML + `length_scale`. Fine-tune VITS/Kokoro = projet séparé, pas le MVP. Clone XTTS = inférence seulement. §3.4.

**Rythme dans le texte, format universel.**  
**SSML 1.1** + profil Sentier. Plan B : pauses `/ // ///` compilées. C’est ce qui donne le même rendu **relatif** (où on ralentit) d’un moteur à l’autre, pas le même timbre. §3.

**Tout déléguer à Grok.**  
Excellent pour **calibrer** 1 arbre. Mauvais comme usine à 57 000 fichiers tant qu’il n’y a pas d’API batch + SSML respecté + checksums. §6.5, scénario B.

---

## 11. Décision à trancher après la maquette (pas maintenant)

1. Piper seul pour le MVP audio ?
2. Hybride Piper (récit) + Grok (choix + conclusion) ?
3. On attend une API xAI TTS avant tout audio de masse ?

Tant que ce n’est pas tranché : **les JSON restent publiables en texte** (`APPROVED_TEXT`). L’audio est un paquet à part (`APPROVED_PACKAGE`).

---

*Fin de l’étude v1.0. Prochaine itération : maquette `foret/TREE-SEC-001/` + 1 atomique, deux moteurs, compte-rendu d’écoute.*
