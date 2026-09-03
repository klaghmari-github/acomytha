# Étude — Restitution vocale des arbres d’histoires Sentier

**Document :** ETU-AUD-001  
**Version :** 1.2  
**Date :** 3 septembre 2026  
**Statut :** étude de cadrage, pas une spécification figée  
**Public :** fondateurs, éditorial, production audio, technique  
**Sources internes :** spec fonctionnelle v2.0 (AUD-001 à AUD-003, GEN-003), validation VAL-HIST-001, schéma `stories/schema.json`, corpus `feat/F-GEN-001-corpus-histoires` (685 atomiques + 760 ramifiées = 1445 arbres).  
**Sources externes :** API xAI TTS (docs 2026), SSML 1.1 W3C, Piper / Kokoro / MeloTTS / XTTS, plus une analyse ChatGPT du 3 septembre 2026 (idées retenues ou écartées en §12).  
**Contrainte machine :** ~3,8 Go VRAM GPU, ~30 Go RAM, 8 cœurs CPU. Pas de gros LLM local.

**Changelog 1.0 → 1.1.** L’API xAI TTS existe (`POST /v1/tts`, 15 USD / million de caractères, français, balises expressives). Le rythme n’est plus collé au JSON enfant : un `narration_plan.json` porte l’intention, des adaptateurs compilent vers xAI / SSML / Piper. Le paquet publié adresse les fichiers par `node_id` ; l’arborescence forêt/arbre/branches reste une **vue d’écoute** générée. Licences, loudness, cache, QA ASR et coût réel du corpus sont ajoutés. On n’adopte pas la limite « deux options » de l’analyse externe : le corpus ramifié Sentier est 3 × 3 × 3.

**Changelog 1.1 → 1.2.** Texte ChatGPT relu en entier (le collage précédent était tronqué). Ajouts opérationnels : type `DIALOGUE`, durées locales **par heure** d’audio, table RTF xAI, délais de développement (PoC / MVP / prod), pipeline de bake, clone voix ~2 min, annexes prompt compilateur (adapté : **3 options**, pas 2). Rien de contradictoire avec la v1.1.

---

## 0. Verdict en une page

**Objectif.** Chaque nœud d’un arbre JSON devient un (ou plusieurs) fichiers audio. L’enfant entend une histoire, une question ou un choix, puis une branche. À la feuille : une conclusion qui reformule la leçon. Rien n’est généré pendant l’écoute (GEN-001).

**Architecture.** Hybride et indépendante du moteur :

1. Le JSON validé (`APPROVED_TEXT`) reste la source narrative. On n’y mélange pas de balises TTS.
2. Un `narration_plan.json` décrit **comment dire** chaque segment (rôle, débit, énergie, pauses, emphases). C’est le contrat universel.
3. Des **adaptateurs** compilent ce plan vers les balises xAI, vers SSML 1.1, ou vers des pauses ffmpeg + `length_scale` Piper.
4. On ne promet **pas** la même waveform d’un moteur à l’autre. On promet la même **intention** (où on ralentit, où on pose, quel mot est porté).
5. L’audio publié est adressé par `node_id`, versionné, checksummé. Une vue récursive forêt → arbre → branches est générée pour écouter / déboguer, ce n’est pas le format canonique.

**Recommandation MVP.**

| Couche | Choix | Pourquoi |
| --- | --- | --- |
| Intention de dire | **`narration_plan.json`** (neutre) | Survité un moteur. Le texte enfant ne contient jamais `[pause]` ni `<slow>`. |
| Export riche | SSML 1.1 + profil `sentier-prosody-v1` | Format d’échange le plus répandu (Azure, Google, Amazon). Piper l’ignore : on compile. |
| Qualité finale | **API xAI TTS** (`language=fr`, voix unique par arbre, WAV master) | Expressivité, français, 15 k caractères / requête, 50 req/s. Coût corpus ~**170–280 USD** une fois, pas un abonnement. |
| Préécoute / secours local | **Piper** CPU, puis **Kokoro-82M** si le FR passe le test | 0 GPU. Une nuit pour 260 h. Qualité « lisible », pas encore « conteur ». |
| Clone de voix | API xAI Custom Voices (**~2 min** de référence selon xAI) **ou** rien | Stabilité narrative FR et droits à tester. XTTS-v2 : VRAM juste **et** licence CPML non commerciale → **hors produit**. |
| Entraînement local | **Non** | Piper documente 24–48 Go VRAM habituels, plancher communautaire ~8 Go. 3,8 Go = inférence seulement. |

**Temps d’ordre de grandeur pour tout le corpus actuel** (~260 h d’audio unique, ~57 000 fichiers) :

| Voie | Temps machine | Coût indicatif | Commentaire |
| --- | --- | --- | --- |
| API xAI TTS, cache + reprise, ~10 requêtes parallèles | **quelques heures à 1–2 jours** | **~170–280 USD** + régénérations | Le goulot est l’écoute humaine, pas la synthèse. |
| Piper, 8 cœurs, parallèle | **4 à 12 heures** | 0 € | Prévisible. Qualité moyenne. |
| Kokoro CPU 8 cœurs | **15 à 40 heures** | 0 € | Plus naturel. Français à valider (`ff_siwis`, &lt; 11 h de data). |
| XTTS-v2 sur 3,8 Go | **4 à 15 jours** | 0 € mais CPML | Hors produit commercial. |

**Décision proposée (inchangée dans l’esprit, précisée dans les moyens).**

1. Figer le schéma `narration_plan` + le profil `sentier-prosody-v1`. Les JSON histoires restent valides sans ça.
2. Maquette : **1 ramifié + 1 atomique**, quatre moteurs (xAI, Piper, Kokoro, MeloTTS) sur **les mêmes nœuds**.
3. Si xAI + plan suffit pour N1 (mots compris du premier coup, pas de cri, leçon claire) : on industrialise l’API avec cache. Piper reste le dry-run et le plan B hors-ligne.
4. On **n’entraîne pas** un TTS sur cette machine.
5. Les textes restent publiables en `APPROVED_TEXT` sans audio. L’audio est `APPROVED_PACKAGE`.

---

## 1. Ce que l’enfant doit entendre

L’expérience n’a **pas d’image** (NAR-004, AUD-001). Tout passe par la voix.

### 1.1 Trois régimes de parole (contrat pédagogique)

Les valeurs sont des **réglages initiaux** à mesurer sur de vrais enfants, pas des normes.

| Régime | Quand (JSON Sentier) | Vitesse cible | Intonation | Pauses **dans** l’audio |
| --- | --- | --- | --- | --- |
| **Récit** | `audio`, `transition` | N1 : 110–130 mots/min. N2 : 125–145. N3 : 135–155. | Chaude, phrases courtes, noms répétés. Monte un peu sur un bruit, un goût, un geste. | 400–700 ms en fin de phrase. 800–1200 ms au changement de lieu. |
| **Choix / question** | `choice_story`, `question_lesson`, `question_comprehension` | **Plus lent** que le récit (−15 à −25 %). Plage 100–115 mots/min. | Monte sur chaque option. Isole les options. Jamais une liste plate. | 300–500 ms avant la question. 400–600 ms entre options. **Pas** le silence d’attente (voir §1.5). |
| **Leçon / conclusion** | `feedback`, `wrong_feedback`, `ending` | Lent, posé, **sans dramatiser**. 105–120 mots/min. | Un peu plus grave. Une idée = une phrase. On **répète la conduite sûre**, jamais le danger. | Pause avant la formule de leçon. Pause après. Fin : descente. |

Un adulte lit à ~170–190 mots/min. Un enfant de 3–4 ans **perd** au-delà de ~130. Trop lent (sous 100) endort. Phrase cible : **6–14 mots**, une seule information importante.

### 1.2 Types de nœuds plus fins (couche production)

Les trois régimes suffisent à l’enfant. Le compilateur audio, lui, gagne à étiqueter plus finement (mapping, pas un nouveau schéma histoire) :

| Étiquette production | JSON Sentier | Restitution |
| --- | --- | --- |
| `NARRATION` | `audio` | Vivante, variations modérées |
| `DIALOGUE` | réplique d’un personnage dans un `audio` | Couleur légère, intelligibilité prioritaire, pas une voix « cartoon » |
| `ATTENTION_CUE` | amorce courte dans un `audio` | Bref, un peu plus énergique, jamais un cri |
| `STORY_CHOICE` | `choice_story` | 3 options, rythme **symétrique**, aucun favori |
| `COMPREHENSION_QUESTION` | `question_lesson` / `question_comprehension` | Une idée, réponse 1–3 mots |
| `REPROMPT` | `retry_prompt` | Plus court, plus lent, **mêmes** options / même question |
| `CONFIRMATION` | (moteur, pas un nœud JSON aujourd’hui) | Immédiat, positif, sans exagération — à n’introduire que si le runtime en a besoin |
| `SAFE_CORRECTION` | `wrong_feedback` | Calme, formulation positive, conduite sûre seulement |
| `BRANCH_TRANSITION` | 1re phrase du nœud suivant un choix | Brève, n’est **pas** le prompt de choix |
| `CONCLUSION` | `ending` | Posé, une action mémorisable, « L’histoire est finie. » |

### 1.3 Anti-monotonie (sans spectacle)

Le cerveau d’un enfant de maternelle décroche si le même contour mélodique revient 40 fois. On varie **sans crier**. Changement perceptible toutes les **20 à 40 secondes** par la structure (action, dialogue, question, pause), pas par un bruitage.

| Levier | Usage | Interdit |
| --- | --- | --- |
| Accélérer 5–8 % | Bruit, jeu, course **dans l’espace autorisé** (parc, jardin) | Accélérer une consigne de sécurité |
| Ralentir 15–25 % | Pied sur le trottoir, main, « on attend », « on dit stop » | Dramatiser (« attends… le danger… ») |
| Monte légère | Appel du prénom, option de choix | Cri, surprise violente |
| Descente | Fin de scène, conclusion de leçon | Voix triste / coupable |
| Chuchotement très léger | Surprise **gentille** (FAM.SEC.001) seulement | Peur, malaise, « secret qui se cache » |
| Onomatopée courte | `toc toc`, `miaou`, pluie — **une fois** | Bruitage qui masque la consigne (AUD-002) |

**Règle d’or sécurité (`positive_only_critical`).** Le nœud de leçon (feu, trottoir, prises, balcon, rester assis) est **toujours** en régime lent + clair. On ne « joue » pas le rythme ici.

### 1.4 Que dire à une intersection

Le nœud `choice_story` n’est **pas** un test moral. Les options sont narratives (lieu, objet, camarade). **Les trois** mènent à des suites sûres. On ne propose jamais une option dangereuse « pour voir ».

Séquence orale :

1. **Refermer** la scène précédente (une phrase, descente).
2. Pause 250–500 ms.
3. **Annoncer** le choix : « On peut aller… »
4. **Poser les trois options une par une**, même poids.
   - « …dans la cuisine. » *(pause 500 ms)*
   - « …dans le jardin. » *(pause 500 ms)*
   - « …ou dans la chambre. »
5. **Rendre la main au moteur.** Le fichier audio s’arrête. Pas de « dis-moi vite ».

`question_lesson` (vérification de sécurité) : **une** conduite acceptable. La mauvaise action n’est pas mise en scène comme une branche. Après erreur : uniquement `wrong_feedback` (conduite sûre). Voix jamais moqueuse, jamais plus rapide.

Relance (`retry_prompt`) : plus courte, plus lente, **même** formulation de sens.

### 1.5 Silence d’attente ≠ pause dramatique

Deux silences différents :

| Silence | Où | Durée initiale | Pourquoi séparé |
| --- | --- | --- | --- |
| Pause **dramatique** | Dans le WAV (fin de phrase, entre options) | 300–1500 ms | Fait partie du récit. Versionnée avec le texte. |
| Attente **de réponse** | Runtime mobile (`silence_check`) | 4–6 s jour, configurable nuit | Âge, mode jour/nuit, profil : on change le délai **sans** régénérer 57 000 fichiers. |

Proposition runtime (à mesurer en test utilisateur, pas à figer dans l’audio) :

| Événement | Réglage initial |
| --- | --- |
| Pause avant la question (dans l’audio) | 300–500 ms |
| Attente première réponse | 4–6 s |
| Relance | après silence ou ambiguïté |
| Attente après relance | 4–6 s |
| Absence persistante, jour | `default_next` / chemin neutre |
| Absence persistante, nuit | arrêt doux de session |

### 1.6 Conclusion (feuille)

À la place d’une transition : un fichier `conclusion`.

1. Ce qui s’est passé (1–2 phrases, récit calme).
2. La conduite sûre, affirmative (`safe_actions`).
3. Les `required_messages` reformulés, sans jargon.
4. Fermeture : « L’histoire est finie. » Descente. Pas de « à demain » commercial.

### 1.7 Profil sonore de livraison

- Master : **WAV mono 24 kHz 16-bit** (ou 48 kHz si le moteur le sort natif). Une fréquence par arbre, pas de mélange.
- Paquet mobile : **Opus 24 kbit/s** (cible taille) **ou** MP3 24 kHz 64–96 kbit/s (compatibilité maximale). Décision à la maquette.
- Loudness initiale : **−19 LUFS** (mono). Crête vraie max **−1,5 dBTP**.
- Pas de musique continue. Bruitages rares, plus faibles que la voix, jamais une récompense d’un choix dangereux.

---

## 2. Deux couches de dossiers : canonique et vue d’écoute

Un JSON = un **arbre**. La forêt = la collection d’arbres. Un **chemin** est ce que l’enfant parcourt ; il est plus court que l’audio unique stocké (27 feuilles × scènes exclusives).

### 2.1 Pourquoi le graphe, pas la récursion, est la source publiée

Une arborescence calquée sur les chemins est la bonne **métaphore** (forêt → arbres → branches). En format publié, elle pose quatre problèmes :

- un nœud accessible depuis deux choix serait **dupliqué** (deux fichiers, deux checksums, deux régénérations) ;
- deux branches qui convergeraient plus tard exploseraient le volume ;
- chemins trop longs à versionner ;
- un mot changé dans un nœud partagé invaliderait N fichiers au lieu d’un.

**Décision.** Le manifeste déclare le graphe. Les fichiers audio sont adressés par `node_id` (+ rôle si un nœud a plusieurs champs parlés : prompt, retry, ok, ko). La vue récursive est **générée** pour l’écoute humaine et le débogage (`tree`, lecteur local). Elle n’est pas le paquet téléchargé par l’app.

### 2.2 Paquet canonique (publié)

```
foret/
  trees/
    <tree_id>/
      <tree_version>/
        story.json                  # copie du JSON APPROVED_TEXT
        narration_plan.json         # intention de dire
        manifest.json               # graphe + assets + hashes + durées
        audio/
          fr-FR/
            <voice_id>/
              <node_id>.<role>.wav
              <node_id>.<role>.wav.sha256
        synthesis/
          <node_id>.<role>.request.json   # requête exacte (reproductibilité)
        qa/
          <node_id>.<role>.qa.json
        listen/                     # vue d’écoute générée, non publiée dans l’app
          racine.wav -> ../../audio/...
          choix_ch1/transition.wav -> ...
          ...
```

Un fichier par combinaison :

```
(node_id, rôle, texte approuvé, plan, locale, voix, moteur, version moteur)
```

L’empreinte SHA-256 de cette combinaison est la **clé de cache**. Si rien n’a changé, on ne régénère pas et on ne refacture pas. Si un mot change, l’ancien fichier ne peut plus être publié sous la nouvelle `tree_version`. On n’écrase jamais une version publiée.

### 2.3 Vue d’écoute (ce que tu as demandé : forêt / arbres / branches)

Générée depuis le manifeste, avec des liens, **sans dupliquer les WAV**.

```
listen/
  racine.wav                        # → audio root
  choix_ch1/
    transition.wav                  # prompt du choix
    relance.wav
    brA/
      scene.wav
      question.wav
      feedback_ok.wav
      feedback_ko.wav
      choix_ch2A/
        ...
        endA1X/conclusion.wav       # feuille : plus de transition
```

**Atomique :**

```
listen/
  racine.wav
  question.wav
  question_relance.wav
  feedback_ok.wav
  feedback_ko.wav
  conclusion.wav
```

Règles :

- Un dossier porte **l’id du nœud** (`brA` reste `brA`).
- `transition` = ce qu’on entend **pour choisir**. Jamais la suite.
- `conclusion` **remplace** `transition` dès que `type == ending`.
- `silence_check` : pas de fichier.
- Une version de texte = une version d’audio (AUD-001).

### 2.4 Mapping nœud JSON → fichiers

| `node.type` | Fichiers (rôle) | Vue d’écoute |
| --- | --- | --- |
| `audio` (root) | `racine` | racine de l’arbre |
| `audio` (après un choix) | `scene` | dossier de l’option |
| `choice_story` | `transition` (+ `relance`) | `choix_<id>/` |
| `question_lesson` / `question_comprehension` | `question`, `question_relance`, `feedback_ok`, `feedback_ko` | même dossier que la scène |
| `feedback` | `feedback_ok` | même dossier |
| `ending` | `conclusion` | feuille, plus de sous-dossier |
| `silence_check` | aucun | — |
| `transition` (type JSON) | `scene` court | même dossier |

---

## 3. Le rythme dans un plan, pas dans un LLM

### 3.1 Pourquoi SSML seul ne suffit pas, et pourquoi on ne l’écrit pas dans le texte enfant

- Un TTS neural **sans** balises produit une courbe moyenne. Deux moteurs ≠ deux lectures.
- Le W3C le dit : SSML 1.1 est riche, le **rendu varie** selon le synthétiseur. Kokoro n’a pas de SSML natif. Piper parse peu. xAI a ses **propres** balises (`[pause]`, `<slow>`, `<emphasis>`), pas du SSML.
- Coller du SSML dans `text` risque qu’un moteur le **lise à voix haute**.
- Improviser casse les durées min/moy/max exigées par la spec.

Donc : le texte enfant reste du français quotidien. **À côté**, un plan neutre. Les adaptateurs traduisent. Si un moteur ignore une balise, on dégrade en `<break>` / silences concatenés, qui passent presque partout.

### 3.2 `narration_plan.json` (contrat universel)

```json
{
  "schema_version": "1.0",
  "tree_id": "TREE-SEC-001",
  "locale": "fr-FR",
  "nodes": [
    {
      "node_id": "ch1",
      "role": "transition",
      "kind": "STORY_CHOICE",
      "segments": [
        {
          "text": "Sami a bien attendu.",
          "delivery": {
            "role": "close_scene",
            "rate_wpm": 118,
            "energy": "calm",
            "pitch": "fall",
            "emphasis": []
          },
          "pause_after_ms": 700
        },
        {
          "text": "On peut prendre le seau.",
          "delivery": {
            "role": "option",
            "rate_wpm": 105,
            "energy": "warm",
            "pitch": "slight_rise",
            "emphasis": []
          },
          "pause_after_ms": 500
        }
      ]
    }
  ]
}
```

Les `text` du plan sont des **copies** du texte approuvé (ou des phrases déjà dans le JSON). Le compilateur refuse un plan dont le texte diverge du JSON (hors ponctuation de pause).

### 3.3 Adaptateurs

| Cible | Compilation |
| --- | --- |
| **xAI TTS** | `[pause]` / `[long-pause]`, `<slow>`, `<soft>`, `<emphasis>`, `<lower-pitch>`. **Interdit** dans Sentier : `[laugh]`, `[whisper]` (sauf FAM.SEC.001), volume `loud`, chant. `speed` API 0,85–0,95 pour N1. `language=fr`. `replace` pour les prénoms / IPA si un nom est mal lu. |
| **SSML 1.1** | Profil `sentier-prosody-v1` ci-dessous. |
| **Piper** | Phrases + silences ffmpeg (`anullsrc`) + `length_scale` 1,15–1,35. |
| **Kokoro / MeloTTS** | Segmentation + ponctuation + vitesse globale. Pas de SSML natif. |

Profil `sentier-prosody-v1` (SSML, sous-ensemble volontairement petit) :

| Balise | Usage Sentier |
| --- | --- |
| `<speak>` `<p>` `<s>` | racine / phrase |
| `<break time="400ms"/>` | **levier obligatoire.** 400 fin de phrase ; 800 lieu ; 1500 **n’est plus** l’attente de réponse (retirée de l’audio, §1.5) — 500–700 entre options |
| `<prosody rate="slow">` | leçon, choix, conclusion. Valeurs : `x-slow` / `slow` / `medium` |
| `<prosody pitch="low">` | conclusion, conduite sûre |
| `<emphasis level="moderate">` | un mot de leçon (`trottoir`, `main`, `stop`) — **un par phrase max** |
| `<say-as interpret-as="characters">` | jamais |
| `<audio>` | jamais dans le MVP |
| `<prosody volume="loud">` | **interdit** |

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

Plan B ASCII (artefact de build, pas la source) : `/` = 400 ms, `//` = 800 ms, `///` = 1500 ms, `*mot*` = emphase si le moteur a un token.

### 3.4 Entraîner un synthétiseur « conteur » sur cette machine

| Travail | Faisable à 3,8 Go VRAM + 30 Go RAM ? | Temps / donnée |
| --- | --- | --- |
| Rien (Piper/Kokoro off-the-shelf) | Oui | 0 |
| Ajuster vitesse/pitch Piper (config, pas de training) | Oui | minutes |
| Fine-tune Piper/VITS | **Non recommandé ici.** Docs : configs habituelles 24–48 Go VRAM ; retours communautaires dès ~8 Go | projet GPU loué |
| Fine-tune Kokoro / Melo / Parler | VRAM parfois ok, savoir-faire élevé, corpus annoté (scènes, questions, conclusions) | jours + GPU loué |
| Fine-tune XTTS-v2 | OOM même à 8–12 Go en batch &gt; 1 | — |
| Entraîner from scratch / LLM audio | **Non** | — |
| Cloner une voix via **API xAI Custom Voices** | Oui, hors machine | quelques minutes de référence + droits |
| Cloner avec XTTS sans fine-tune | Inférence peut-être, **licence CPML** | hors produit |

L’entraînement d’une voix **n’apprend pas** le métier de conteur. Il faudrait un corpus de scènes / questions / transitions / conclusions annoté, diction cohérente. Pour un MVP, ce coût éditorial dépasse celui de l’API TTS.

---

## 4. Prompts

### 4.1 Prompt conteur (un nœud, production audio)

À coller pour un nœud. Un appel = un fichier. Le compilateur injecte le plan déjà compilé (balises xAI ou SSML), pas un roman d’instructions.

```
Tu es le conteur de Sentier. Public : enfant de {N1|N2|N3} (3–6 ans). Audio seulement.

VOIX
- Français quotidien, articulation nette, un peu plus lente qu’un adulte.
- Chaude, calme, jamais moqueuse, jamais effrayée, jamais « dessin animé criard ».
- N1 : très posé. N3 : un peu plus de vie, jamais précipité.
- Même locuteur que les autres nœuds de {tree_id}, voix {voice_id}.

RÉGIME : {recit | choix | question | correction | conclusion}
FRAMING : {standard | positive_only_critical}

RÈGLES
- Choix : chaque option isolée, même poids, aucune n’est « la bonne ». Trois options.
- Question : une idée, puis tu t’arrêtes. Relance = plus courte, plus lente, même sens.
- Correction : seulement la conduite sûre. Ne pas décrire un geste dangereux.
- Conclusion : leçon affirmative + « L’histoire est finie. » Descente.
- positive_only_critical : ralentir sur pieds / mains / trottoir / adulte. Pas de jeu rythmique.
- Interdit : musique dominante, cri, rire, [laugh], volume loud, bruitage qui couvre les mots,
  religion, politique, deux papas/mamans. Aucune balise interne ne doit être lue à voix haute.

TEXTE (déjà compilé, respecte les balises) :
{compiled_text}
```

### 4.2 Limite Grok Build vs API xAI

Dans **cette** session Grok Build, il n’y a pas d’outil TTS (seulement image / vidéo). La production de masse passe par l’**API** `POST https://api.x.ai/v1/tts` avec `XAI_API_KEY`, pas par le chat. C’est un compilateur, pas « laisser Grok raconter dans le terminal ».

Paramètres API utiles pour Sentier :

- `language=fr` (pas `auto` : on veut du français stable)
- `voice_id` unique par arbre (voix built-in calme, à A/B : `eve` / `ara` / `leo`… **à écouter** ; pas de voix criarde)
- `output_format`: WAV 24 kHz master, puis encode mobile
- `speed` 0,85–1,0 selon N1–N3
- `text` ≤ 15 000 caractères (nos nœuds sont très en-dessous)
- `replace` pour les prénoms mal prononcés
- pas de streaming (on pré-génère, GEN-001)

### 4.3 Prompt compilateur (implémentation, pas la voix)

Quand on passera à `F-AUD-001` : compilateur déterministe, interface `TtsProvider`, `XaiTtsProvider` d’abord, Piper/Kokoro ensuite, cache SHA-256, écriture atomique (fichier temp + rename), backoff, dry-run coût, QA, tests d’un nœud partagé par deux branches. Ne pas merger `main`. Prompt d’implémentation en **annexe A** (adapté Sentier : 3 options, mapping `choice_story` / `question_lesson`).

---

## 5. Volume réel du corpus (septembre 2026)

Chiffres du dépôt `feat/F-GEN-001-corpus-histoires`.

| | Atomiques | Ramifiées | Total |
| --- | --- | --- | --- |
| Arbres | 685 | 760 | **1445** |
| Fichiers audio uniques (1 fichier / champ parlé) | ~4 800 | ~52 000 | **~57 000** |
| Durée unique estimée | ~23 h | ~240 h | **~260 h** |

Détail ramifié (ordre de grandeur TREE-SEC-001) : ~68 fichiers / arbre, ~19 min d’audio unique / arbre. Un chemin enfant : ~3–8 min.

Paquet enfant (Opus 24 kbit/s) : ~3,4 Mo / ramifié × 760 ≈ **2,6 Go** + atomiques ~250 Mo ≈ **~3 Go**. Masters WAV ~**40 Go**, hors téléphone.

Caractères facturables xAI (débit enfant ~120 mots/min, ~6 caractères/mot) : ~43 000 caractères / heure d’audio × 260 h ≈ **11,2 millions de caractères**.

---

## 6. Synthétiseurs — ressources, licences, temps, argent

Machine : **3,8 Go VRAM, 30 Go RAM, 8 cœurs.** Pas de LLM 7B+ en même temps que le TTS.

### 6.1 Tableau

| Moteur | VRAM | Licence **produit** | Qualité conte FR | SSML / tags | Temps 260 h | Usage Sentier |
| --- | --- | --- | --- | --- | --- | --- |
| **API xAI TTS** | 0 local | Service payant, CGU xAI à relire au lancement | Forte (à valider N1 FR) | Balises propres, pas SSML | heures–2 j + QA | **Qualité finale MVP** |
| **Piper ONNX** (siwis/tom) | 0 CPU | Moteur actuel **GPL-3.0** (`piper1-gpl`) ; les **WAV générés** ne sont pas contaminés. GPL = sujet seulement si on **embarque** le moteur dans l’app. Voix : licence dataset à vérifier (SIWIS, etc.) | Lisible, un peu plate | Pauses externes | **4–12 h** | Préécoute, dry-run, fallback offline |
| **Kokoro-82M** | 0,4–0,8 Go | Apache-2.0 (poids). Voix FR `ff_siwis` : mention CC-BY SIWIS | EN bon ; FR **B−**, &lt; 11 h | Pas de SSML natif | 15–40 h | Candidat local n°2 si test FR OK |
| **MeloTTS** | ~1 Go | MIT | Correct, moins pilotable | Limité | 1–3 j | Second banc d’essai |
| **Parler-TTS Mini** | limite 3,8 Go | Permissif selon checkpoint | Laboratoire | Description de voix | lent | Hors MVP |
| **XTTS-v2** | 2–4 Go (juste) | **CPML, non commercial** | Bon clone | Faible | 4–15 j | **Exclu du produit** |
| eSpeak-NG | 0 | GPL | Robot | Partiel | &lt; 30 min | Écarté pour l’enfant |
| Bark / F5 / Dia | 6–14 Go | variable | Expressif | Non | Hors machine | Non |

La licence du moteur **ne suffit pas**. Vérifier séparément : code, poids, voix/dataset, droit commercial sur les audios, consentement si clone, obligations si le moteur est **intégré** à l’app (vs simples fichiers pré-générés).

### 6.2 API xAI TTS — coût et débit

Tarif public (docs xAI, 2026) : **15,00 USD / million de caractères**. Limite 15 000 caractères / requête unaire. 50 requêtes/s. Formats WAV/MP3/PCM. Français `fr`. Custom voices (clone) documenté.

| Volume | Caractères | Coût synthèse (1 passe) |
| --- | --- | --- |
| 10 min | ~7 000 | ~0,11 USD |
| 1 h unique | ~43 000 | ~0,65 USD |
| **Corpus 260 h** | **~11,2 M** | **~170 USD** |
| + 40 % régénérations / essais | ~15,7 M | **~235 USD** |
| ASR xAI pour QA (260 h) | — | ~26 USD à 0,10 USD/h REST |

Ce n’est **pas** un argument pour tout écouter à la main : 260 h d’écoute = 260 h humaines. La revue est **échantillonnée** + ASR bloquant (VAL-AUD).

Temps machine xAI (formule) :

```
temps ≈ ceil(nœuds / concurrence)
        × (latence + durée_audio × RTF)
        + reprises + QA
```

xAI ne publie pas un RTF de lot garanti. Il serait trompeur de promettre un temps exact avant benchmark. Illustration sur **120 nœuds de 30 s** (60 min uniques), 4 requêtes parallèles, 1 s de latence :

| RTF observé | Génération théorique | Budget avec reprises et contrôles |
| ---: | ---: | ---: |
| 0,2 | ≈ 3,5 min | 10–20 min |
| 0,5 | ≈ 8 min | 15–30 min |
| 1,0 | ≈ 15,5 min | 25–45 min |

À l’échelle forêt : 57 000 nœuds, 10 en parallèle, ~6 s/requête si RTF 0,3 sur 20 s d’audio → **ordre 10 heures**. Budget calendaire avec erreurs et disque : **1–2 jours**. Écouter 60 min prend au moins 60 min, même si la synthèse en prend 10. La revue d’un échantillon (1 arbre complet + 20 nœuds tirés par domaine) est le vrai délai.

Dry-run obligatoire avant tout appel : nombre de nœuds, caractères, durée, taille, **coût**, sans toucher l’API.

Le coût se calcule sur la somme des caractères de tous les **nœuds uniques**, jamais sur la durée d’un seul chemin enfant.

### 6.3 Piper (secours / préécoute)

- Raspberry Pi 4 le fait : largement dans 8 cœurs / 30 Go.
- `fr_FR-siwis-medium` / `fr_FR-tom-medium`. `length_scale` 1,15–1,30 (N1), 1,35 (choix).
- Build : plan → phrases + silences ffmpeg.
- 260 h, RTF 0,08, 8 workers ~50–70 % → **une nuit (5–12 h)**.
- GPL-3.0 : OK pour générer des fichiers et les embarquer. Pas OK (sans politique licence) pour lier le moteur dans un binaire app distribué.

Fourchettes **par heure d’audio final** (planification, à confirmer par un bench de 20 segments : chargement, pic RAM/VRAM, RTF, débit par lot, taux d’échec, qualité FR) :

| Moteur | Mémoire | Temps pour 1 h d’audio | Risque |
| --- | --- | --- | --- |
| Piper | Faible, CPU | ≈ 3–20 min | Prosodie longue trop régulière |
| Kokoro-82M | Faible à modérée | ≈ 10–60 min | FR et contrôle d’intonation |
| MeloTTS | Modérée, CPU possible | ≈ 15–90 min | Expressivité, maintenance |
| Parler-TTS Mini | ~1,8 Go FP16 + exécution | ≈ 1–5 h CPU ; GPU possiblement OOM | Lenteur, mémoire |

### 6.4 Kokoro

- 82 M, Apache-2.0, VRAM FP16 400–800 Mo : **entre**.
- FR `ff_siwis` note B−. Risque `eu`, `un`, liaisons.
- Adopter seulement si 20 phrases N1 passent « on comprend du premier coup ».

### 6.5 Ce qu’on n’utilise pas

- XTTS-v2 : CPML + VRAM juste.
- Fine-tune local : hors 3,8 Go.
- Génération **pendant** l’écoute : interdit (GEN-001). L’API xAI sert à **compiler le paquet**, pas à parler en live dans l’app enfant.

---

## 7. Scénarios de réalisation

### Scénario A — API xAI + plan neutre (recommandé qualité MVP)

1. Schéma `narration_plan` + compilateur + cache SHA-256.
2. Dry-run coût sur 1 arbre, puis forêt.
3. Bake xAI, masters WAV, Opus/MP3, manifeste, QA ASR.
4. **Durée projet** (schéma JSON déjà stable, exécution supervisée) :

| Niveau | Contenu | Estimation |
| --- | --- | ---: |
| Preuve de concept | Parse un arbre, génère quelques nœuds, écrit le manifeste | 0,5–1,5 jour |
| MVP robuste | Cache, reprise, concurrence, graphe, normalisation, logs | 3–6 jours |
| Production | QA ASR/acoustique, retrait de version, métriques, secrets | 7–12 jours |

« Laisser Grok faire » **ne supprime pas** les tests, la revue du code ni l’écoute de validation. Pas 57 000 écoutes humaines : échantillon + ASR bloquant.

### Scénario B — Local Piper d’abord, xAI sur choix + conclusions

Si l’API n’est pas dispo au moment du bake, ou pour zéro coût. Même plan, autre adaptateur. Calage des pauses sur un master xAI de 1 arbre.

### Scénario C — Tout local Kokoro/Melo

Seulement si le test FR enfant passe. 1–2 jours machine.

### Scénario D — Tout « à la main dans Grok chat »

**Irréaliste** à 57 000 fichiers. Le chat n’est pas l’API. On ne fait ça que pour la maquette (≤ 70 fichiers).

---

## 8. Plan de travail (sans bloquer le MR histoires)

Le MR `F-GEN-001` (textes) part **sans** audio. L’audio est `F-AUD-001`.

Pipeline de bake :

```
story.json APPROVED_TEXT
        ↓
validation graphe (root unique, ids, arêtes, feuilles, pas de cycle, chemins terminables)
        ↓
narration_plan.json neutre
        ↓
adaptateur + dry-run (nœuds, caractères, durée, taille, coût) — zéro appel TTS
        ↓
synthèse par (nœud, rôle) + cache SHA-256 + reprise
        ↓
normalisation −19 LUFS / −1,5 dBTP + encode mobile
        ↓
QA acoustique + ASR vs texte approuvé
        ↓
écoute humaine selon matrice de risque (sécurité = toujours ; récit = échantillon)
        ↓
manifest signé + paquet téléchargeable → APPROVED_PACKAGE
```

Le paquet n’est `APPROVED_PACKAGE` que si **tous** les nœuds accessibles sont validés. Une erreur bloquante sur une branche invalide l’arbre complet.

| ID | Prio | Livrable | Sortie |
| --- | --- | --- | --- |
| AUD-TREE-001 | P0 | Schéma `narration_plan` | JSON Schema + fixtures valides/invalides. JSON histoires encore valides sans plan. |
| AUD-TREE-002 | P0 | Schéma `manifest` audio | Graphe, assets, hashes, durées, versions |
| AUD-TREE-003 | P0 | Compilateur graphe → 1 fichier / (nœud, rôle) | Pas de duplication par chemin |
| AUD-TREE-004 | P0 | Adaptateur xAI TTS | `language=fr`, balises autorisées, `XAI_API_KEY` jamais loggée |
| AUD-TREE-005 | P0 | Cache, reprise, écriture atomique | Relance sans refacturer un nœud identique |
| AUD-TREE-006 | P0 | Normalisation −19 LUFS / −1,5 dBTP + encode mobile | Master + paquet |
| AUD-TREE-007 | P0 | QA : fichier lisible, durée, clipping, silences, ASR vs texte | Une erreur bloquante invalide l’arbre (politique actuelle) |
| AUD-TREE-008 | P0 | Dry-run coût / durée / taille | Zéro appel API |
| AUD-TREE-009 | P0 | Vue `listen/` générée (liens) | `tree` Unix = contrat §2.3 sur TREE-SEC-001 + 1 atomique |
| AUD-TREE-010 | P1 | Adaptateur Piper + benchmark Kokoro/Melo | Même corpus de 12–20 nœuds, RTF / RAM / note humaine |
| AUD-TREE-011 | P1 | Écoute A/B enfants 3–4 et 5–6 + parents | Intelligibilité, question du premier coup, 5 puis 10 min d’attention, noms propres |
| AUD-TREE-012 | P2 | Voix propriétaire (clone xAI, droits, contrat) | Seulement si les built-in ne suffisent pas |

Prototype de décision **avant** industrialisation : mini-arbre 12–20 nœuds (récit, action, question, choix 3 options, relance, correction, 2 conclusions) × 4 moteurs.

---

## 9. Risques

| Risque | Gravité | Mitigation |
| --- | --- | --- |
| xAI FR enfant trop « adulte » / trop vif | Majeure | A/B voix + `speed` + interdiction `[laugh]` ; fallback Piper |
| Piper trop plat, enfant décroche | Majeure | xAI sur choix+conclusions, ou Kokoro si FR ok |
| Kokoro FR illisible (`un`, liaisons) | Majeure | Test 20 phrases avant tout corpus |
| Quota / 429 API | Majeure | Concurrence bornée, backoff, cache |
| Grok non bit-identique à la régénération | Bloquante VAL-AUD si on régénère sans bump | Cache par hash ; régénérer = nouvelle `tree_version` |
| GPL-3.0 si on embarque Piper dans l’app | Majeure (juridique) | MVP = fichiers pré-générés, pas le moteur |
| XTTS CPML en prod | Bloquante | Exclu |
| 40 Go de WAV | Mineure | Disque prod ; Opus dans le paquet |
| Bruitages trop présents | Bloquante AUD | Pas d’`<audio>` dans le plan enfant |
| Monotonie 27 fins | Majeure | Plan différent par feuille (pause, mot d’ancrage) |
| Dossiers récursifs comme format publié | Majeure (ops) | Vue `listen/` seulement |
| Confondre choix narratif et question de sécu | Bloquante PED | Deux kinds, deux restitutions (§1.4) |

---

## 10. Réponse directe aux questions posées

**Comment restituer vocalement un arbre ?**  
Un fichier par champ parlé, adressé par `node_id`. Vue forêt/arbre/branches pour écouter. `transition` aux intersections, `conclusion` aux feuilles. Voix unique par arbre. Régimes récit / choix / leçon. §1–2.

**Intonation, rythme, clarté enfant.**  
110–155 mots/min selon N1–N3. Plus lent aux choix et aux leçons. Pauses chiffrées **dans** l’audio. Attente de réponse **hors** audio. Emphase d’un seul mot de conduite sûre. Pas de cri. §1.

**Prompt Grok.**  
§4. Un nœud à la fois, régime explicite, texte déjà compilé. La masse passe par `POST /v1/tts`, pas par le chat.

**Dossier par JSON, sous-dossiers = branches.**  
Oui comme **vue d’écoute**. Non comme paquet publié (duplication, chemins, cache). §2.

**Temps Grok vs open-source low-resource.**  
xAI API : ~10 h–2 j machine, ~170–280 USD, goulot = QA humaine. Piper : une nuit, 0 €. Kokoro : 1–2 jours. XTTS : 1–2 semaines et hors licence. §5–6.

**Ressources synthétiseur.**  
Piper : CPU, &lt; 0,5 Go RAM. Kokoro : &lt; 1 Go VRAM. xAI : 0 local. XTTS : 2–4 Go, juste, exclu. Bark/F5 : non.

**Entraîner pour le rythme.**  
Pas un LLM. Plan + adaptateur + `speed`/`length_scale`. Fine-tune = GPU loué, pas le MVP. Clone = API xAI si besoin, avec contrat. §3.4.

**Rythme dans le texte, format universel.**  
**`narration_plan.json`** = intention. SSML et balises xAI = exports. On garantit la même intention, **pas** la même waveform. §3.

**Tout déléguer à Grok chat.**  
Excellent pour **calibrer** 1 arbre. Mauvais comme usine. L’usine, c’est l’API + le compilateur. §6.2, scénario A.

---

## 11. Décision à trancher après la maquette (pas maintenant)

1. xAI TTS seul pour le MVP audio ?
2. Hybride Piper (récit) + xAI (choix + conclusion) ?
3. Piper seul (zéro API, qualité moyenne) ?

Tant que ce n’est pas tranché : **les JSON restent publiables en texte** (`APPROVED_TEXT`). L’audio est un paquet à part (`APPROVED_PACKAGE`). Une seule erreur bloquante sur une branche invalide l’arbre complet.

---

## 12. Ce que l’analyse ChatGPT apporte — retenu / écarté / corrigé

Fichier source : collage intégral du 3 sept. 2026 (le premier envoi était tronqué au milieu ; la v1.2 reprend §§10–16 : coûts, RTF, délais de dev, prompt compilateur, pipeline, backlog).

### Retenu (améliore v1.0)

| Idée | Pourquoi on l’intègre |
| --- | --- |
| `narration_plan.json` neutre + adaptateurs | Meilleur que coller du SSML dans le JSON enfant. Survité xAI **et** Piper. |
| Graphe / `node_id` = format publié ; récursion = vue | Évite la duplication et casse le cache. La métaphore forêt/branches est conservée en `listen/`. |
| Silence d’attente dans le runtime, pas dans le MP3 | On change N1/N3 ou jour/nuit sans re-bake. |
| Loudness −19 LUFS / −1,5 dBTP | Manquait. Profil de livraison. |
| Cache SHA-256 (texte+plan+voix+moteur) | AUD-001 disait « tout régénérer » : trop cher. On invalide le nœud, pas la forêt. |
| `*.request.json` + QA ASR par nœud | Reproductibilité et VAL-AUD. |
| Version `tree_id/tree_version` | On n’écrase pas un paquet publié. |
| Licences (Piper GPL-3.0 moteur, XTTS CPML, voix ≠ code) | Trous juridiques de la v1.0. |
| Coût xAI 15 USD / M car. + dry-run | L’usine Grok devient **chiffrable** (~170–280 USD le corpus). |
| L’écoute humaine est plus longue que la synthèse | Corrige l’illusion « une nuit et c’est fini ». |
| Types de nœuds production (REPROMPT, SAFE_CORRECTION…) | Mapping, pas un nouveau JSON histoire. |
| Distinction choix narratif / question de sécurité | Déjà dans Sentier ; l’analyse le formule clairement. |
| Custom voices xAI plutôt que fine-tune local | Aligné 3,8 Go. |
| Sources / liens docs | Ajoutées §13. |

### Écarté ou corrigé (on ne copie pas)

| Idée ChatGPT | Décision Sentier |
| --- | --- |
| **Maximum deux options** au choix narratif | **Non.** Corpus et spec : 3 branches × 3 niveaux. Les trois sont sûres. |
| Exemple « le petit bonhomme est rouge » | **Non.** PED-011 : pas de rouge/vert type feu. On garde seau / doudou / ballon. |
| SSML « ne suffit pas » ⇒ on jette SSML | **Non.** SSML reste l’export cloud générique. Le plan est au-dessus, pas à la place. |
| Grok TTS = qualité finale **sans** maquette | **Pas encore.** On A/B avec Piper/Kokoro sur 12–20 nœuds enfants. |
| MP3 64–96 kbit/s comme cible unique | On garde **Opus** en option (taille). Décision à la maquette. |
| WPM unique 115–135 (tous âges) | On **garde N1/N2/N3**. La plage ChatGPT recouvre N1–N2 ; N3 peut aller à 155. |
| Parler-TTS Mini comme candidat sérieux | Laboratoire seulement (VRAM). |
| Prompt « implémente le compilateur maintenant » | Hors de **cette** étude. Backlog `F-AUD-001`, après validation des textes. |

### Corrections factuelles de la v1.0 grâce à cette relecture

- v1.0 : « pas d’outil TTS dans Grok Build, donc pas d’usine ». **Vrai pour le chat.** Faux pour le produit : l’API `POST /v1/tts` existe, batchable, français, ~170 USD le corpus.
- v1.0 : « SSML donne quasiment le même rendu partout ». **Trop fort.** Même intention, pas même waveform.
- v1.0 : 1,5 s de silence **dans** le fichier de choix. On le **sort** du fichier (attente runtime).
- v1.0 : régénérer l’arbre entier si le JSON bouge. On régénère les **nœuds dont le hash a changé**, nouvelle `tree_version` si déjà publié.

---

## 13. Sources techniques

- [xAI Text to Speech](https://docs.x.ai/developers/model-capabilities/audio/text-to-speech) — `POST /v1/tts`, balises, `language=fr`, 15 000 car., WAV/MP3
- [xAI Pricing — Voice](https://docs.x.ai/developers/pricing) — TTS 15,00 USD / 1 M caractères ; STT 0,10 USD/h REST
- [SSML 1.1 W3C](https://www.w3.org/TR/speech-synthesis11/)
- [Piper (OHF, GPL-3.0)](https://github.com/OHF-Voice/piper1-gpl) et [doc entraînement](https://github.com/OHF-Voice/piper1-gpl/blob/main/docs/TRAINING.md)
- [Kokoro-82M](https://github.com/hexgrad/kokoro) — Apache-2.0 ; voix FR `ff_siwis` &lt; 11 h, note B−
- [MeloTTS](https://github.com/myshell-ai/MeloTTS) — MIT
- [Parler-TTS](https://github.com/huggingface/parler-tts)
- Analyse ChatGPT `ETUDE_RESTITUTION_VOCALE_ARBRES.md` (3 sept. 2026) — non normative, filtrée en §12

---

---

## Annexe A — Prompt compilateur (F-AUD-001, pas maintenant)

À adapter aux noms **réels** du schéma avant exécution. Écarts à lister avant de coder. **Trois options** de choix, pas deux. Ne pas merger `main`.

```
Tu conçois puis implémentes un compilateur audio déterministe pour les arbres
narratifs de ce dépôt. Lis stories/schema.json, stories/outils/validate.py,
stories/REGLES.md et gestion_projet/backlog/Etude_restitution_vocale_arbres_v1.0.md.
Ne modifie pas main. Ne fusionne rien.

OBJECTIF
À partir d’un JSON APPROVED_TEXT, produire un paquet versionné :
1 fichier par (node_id, rôle), narration_plan.json, manifest.json,
*.request.json, checksums, rapports QA. Le graphe JSON est la source.
Pas de duplication par chemin. La vue listen/ est générée (liens), pas publiée.

ÉTAPES
1. Mapping explicite des types JSON → étiquettes production (NARRATION, DIALOGUE,
   STORY_CHOICE, COMPREHENSION_QUESTION, REPROMPT, SAFE_CORRECTION, CONCLUSION…).
   Ne pas inventer de champs.
2. Valider avant synthèse : root unique, ids uniques, destinations existantes,
   feuilles, nœuds accessibles, pas de cycle, réponses attendues, chemins terminables.
3. Générer ou lire narration_plan.json (segments : texte approuvé, rôle, wpm,
   énergie, pitch, emphases, pause_after_ms). Le texte du plan = texte du JSON.
4. Interface TtsProvider. Implémenter XaiTtsProvider d’abord. Préparer Piper
   et Kokoro sans les imposer au cœur.
5. Compiler vers balises xAI autorisées : [pause], [long-pause], <soft>, <slow>,
   <emphasis>, <lower-pitch>. Interdit Sentier : [laugh], volume loud, <whisper>
   hors FAM.SEC.001.
6. POST /v1/tts language=fr, voix configurable, WAV master, speed configurable.
   Clé uniquement XAI_API_KEY. Ne jamais journaliser le secret.
7. Cache SHA-256 (texte + plan + locale + voix + fournisseur + version moteur
   + paramètres). Identique = pas de refacturation.
8. Écriture atomique, reprise, backoff, concurrence bornée, erreurs partielles.
9. Master WAV puis Opus ou MP3 mobile normalisé (−19 LUFS, −1,5 dBTP).
   Ne jamais écraser une tree_version publiée.
10. manifest.json : tree_id, version, root_node_id, edges, node_id, role, kind,
    asset_path, duration_ms, sha256, locale, voice_id, provider, model_version,
    source_hash, narration_plan_hash, qa_status.
11. QA : fichier lisible, durée plausible, clipping, silences, loudness,
    ASR vs texte. Une erreur bloquante invalide l’arbre.
12. Dry-run : nœuds, caractères, durée, taille, coût xAI — zéro appel API.
13. Tests : embranchements 3×3, reprise après panne, nœud partagé par deux branches.
14. Documenter generate / validate / resume / publish.

RESTITUTION
- 3–6 ans, clair, chaud. Question plus lente, une idée.
- Choix narratif : TROIS options, toutes sûres, rythme symétrique.
- question_lesson : jamais une branche dangereuse attrayante.
- Correction positive. Conclusion : conduite concrète + « L’histoire est finie. »
- Aucune balise interne lue à l’enfant.

LIVRABLES : schéma narration_plan + manifest, code, tests, fixture TREE-SEC-001
+ 1 atomique, rapport bench (temps, coût, RAM/VRAM, RTF, taille).
Après code : exécuter les tests, donner les résultats exacts. Ne merge pas.
```

---

*Fin de l’étude v1.2. Prochaine itération : maquette `listen/TREE-SEC-001/` + 1 atomique, quatre moteurs, compte-rendu d’écoute. Pas de merge `main`.*
