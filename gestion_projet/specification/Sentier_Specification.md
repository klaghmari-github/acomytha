# Sentier — spécification unique

**Produit :** akomytha / Sentier.  
**Version de ce document :** 4.0 — 3 septembre 2026.  
**Remplace :** Source Unique v3.0, Spec fonctionnelle v2.0, Spec forêt narrative, Corrections v3.1 (les règles encore vraies sont ici).  
**Détail opératoire :** stratégies `STRAT-001` à `STRAT-004`.  
**Catalogue leçons :** `stories/referentiel/lecons.xlsx`. Liaisons leçon↔histoires↔chunks : `stories/referentiel/lecon_histoires.xlsx`.  
**Corpus texte :** branche `feat/F-GEN-001-corpus-histoires` (1445 JSON `APPROVED_TEXT`).

---

## 1. Qu’est-ce que Sentier

Forêt narrative **audio seulement** pour enfants de 3 à 6 ans. Pas d’image nécessaire pour comprendre. Le parent choisit les **leçons**. Le système choisit **quelle histoire** raconter. L’enfant, en mode jour, choisit des **branches** (lieu, objet, camarade) — jamais « le bien contre le danger ».

Rien n’est généré pendant l’écoute. Le téléphone joue des **chunks chiffrés** déjà validés, déchiffrés **un par un en RAM**.

## 2. Public et rôles

| Rôle | Fait | Ne fait pas |
| --- | --- | --- |
| Parent | Compte, profils, leçons, durée, stock, préécoute, code | Ne raconte pas à la place du moteur |
| Enfant | Écoute, répond (jour), choisit une branche narrative | N’accède ni aux réglages ni au catalogue |
| Moteur | Joue le graphe, applique jour/nuit, défauts | N’appelle pas de LLM |

Âges : **N1** 3–4 ans (phrases très courtes, 2 options max sur les atomiques) · **N2** 4–5 · **N3** 5–6 (jusqu’à 3 options). Famille **racontée** : papa, maman, enfants (`father_mother_children`).

## 3. Règles non négociables (audio enfant)

1. Dire **quoi faire**. Ne jamais décrire le geste dangereux, même pour l’interdire.
2. Un choix de sécurité n’oppose jamais une option sûre à une option dangereuse imitable.
3. Après une erreur : seulement la conduite sûre.
4. Monde jardin. **Absents** (on n’explique pas pour rejeter) : religion, politique, guerre, crime, discours de genre.
5. Comportement, pas étiquette (« il est méchant / hyperactif »).
6. Pas de menace affective, pas de diagnostic nommé, pas de franchise.
7. Compréhensible sans image.
8. Une leçon = un objectif **observable**.
9. Preuve pédagogique par chemin : situation, conduite sûre, question, confirmation, fin qui ne récompense pas l’inverse.
10. Questions : réponse 1–3 mots. Relance. Défaut si silence.
11. Framing `positive_only_critical` : mains, pieds, place du corps, adulte nommé.
12. Deux leçons critiques (feu + prises, rue + balcon) : scènes **séparées**.
13. Le générateur **ne s’auto-approuve pas**.

Détail éditorial : `stories/REGLES.md`. Validateurs : `STRAT-001`.

## 4. Leçons et histoires

- Une **leçon** a un `lesson_id` stable (`SEC.RUE.002`). Elle peut apparaître dans **plusieurs** histoires, racontée autrement.
- Une **histoire** a un `story_id` (`STO_00001`) et 1 à 3 leçons (`story_lesson`).
- Le parent coche des leçons → l’app télécharge les histoires liées, **entières** (les passages « communs » peuvent être dupliqués : on ne factorise pas l’audio entre histoires).
- Toutes les histoires dans **un seul dossier** de blobs chiffrés. Pas d’arbre de répertoires publié.

Modèle SQL et identifiants de chunks : `STRAT-003`.

## 5. Chunks (unité jouable)

L’histoire n’est plus un « nœud JSON joué tel quel ». Elle est une suite de **chunks** audio.

| `kind` | Rôle | Change le cours ? |
| --- | --- | --- |
| `passage` | Récit, scène, conclusion | Non (enchaîne) |
| `transition_question` | « Que veut tu que le chat fasse ? » | Oui, via la réponse |
| `transition_option` | Audio d’**une** option (« le parc ») | Non (étiquette) |
| `listen_question` | « Le feu est-il rouge ? On attend ? » | **Non.** Dans tous les cas on ne traverse qu’au vert / avec l’adulte |
| `feedback_ok` / `feedback_ko` | Confirmation ou conduite sûre | Non |
| `ending` | Leçon + « L’histoire est finie. » | Fin |

Identifiants path-encodés : premier passage `CHK_T0000_P0000`. Ensuite `CHK_T0001_P0000` (1re question de branche). Réponse k → `CHK_T0001_P000k`. S’il n’existe pas de `…_Txxxx_P0000` suivant : **fin**. Détail : `STRAT-003`.

## 6. Jour et nuit

| | Jour | Nuit |
| --- | --- | --- |
| `listen_question` | Posée, relance, défaut | **Sautée** (l’enfant dort) |
| `transition_question` | Posée + options | **Sautée** : le moteur prend `default_option` |
| Voix | Normale, claire | Plus basse, plus lente, pas de pic |
| Silence | Délai paramétrable (défaut **3 s**), **une** relance optionnelle, puis choix auto | Pas d’attente |

Moteur : `STRAT-004`.

## 7. Audio

- **Payload :** MP3 mono 24 kHz, 64 kbit/s (tous les téléphones le décodent : iOS, Samsung, Huawei).
- **Master de prod :** WAV, jamais livré au téléphone.
- **Sur disque :** fichier chiffré `.chk`, **pas** un `.mp3` lisible.
- Seule l’app détient la clé (Keystore / Keychain). Déchiffrement **chunk par chunk** en RAM, préchargement du suivant pendant la lecture.
- Synthèse corpus : **Piper local, 0 €**. L’abonnement **Heavy** sert à écrire les plans de rythme et le code, **pas** à facturer l’API TTS xAI.
- **Immersion (F-AUD-007) :** quand le récit montre un parc, une voiture, une ambulance, un chien, un bruit court le confirme, **sous** la voix, jamais par-dessus.

Détail : `STRAT-002`.

## 8. Statuts

`PENDING` → validateurs texte → `APPROVED_TEXT` | `REVISION_REQUIRED` | `REJECTED`.  
Audio : `APPROVED_AUDIO` (tous les chunks du graphe) puis `APPROVED_PACKAGE` (manifeste + blobs chiffrés).  
Une erreur bloquante sur une branche **invalide toute l’histoire**.

Le générateur s’arrête à `APPROVED_TEXT`.

## 9. Hors exécution enfant

Pas de LLM, pas d’appel réseau, pas de TTS live. Hors-ligne dès que le paquet local est activé.

## 10. Hors MVP

Mini-LLM borné à l’histoire, voice-to-voice, leçons parentales en langage naturel (phase 5+). Ne pas démarrer.
