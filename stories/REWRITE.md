# F-NAR-008 — Récit captivant (texte d’abord)

Les histoires actuelles enchaînent des **scénarios de leçon**. L’enfant n’a pas l’impression qu’une histoire **commence** et **se termine**. On dirait un cours.

## Principe

Un **fil rouge** (aventure, envie, petit fait) **dirige** le récit. Les leçons **se greffent** dessus, elles ne le remplacent pas.

| Oui | Non |
| --- | --- |
| Un début (quelque chose commence) | Entrer direct dans la consigne |
| Un milieu (on veut, on cherche, on goûte, on attend) | Répéter la leçon à chaque phrase |
| Une fin (c’est fini, on a vécu ça) | « L’histoire est finie » seul, sans clôture |
| Leçon dans l’action | Leçon = tout le texte |

## Processus (ne pas toucher l’xlsx d’origine avant fusion)

1. Extraire : `python stories/outils/rewrite_story.py dump <story_id>`
2. **N agents en parallèle** écrivent `stories/rewrites/<story_id>/agent_<n>.json` (l’xlsx source reste intact).
3. Fusion : `python stories/outils/rewrite_story.py merge <story_id>` → `merged.json`
4. Remplacement : `python stories/outils/rewrite_story.py apply <story_id>` (l’ancien xlsx est remplacé).

Une histoire à la fois **par agent**. Plusieurs histoires en parallèle (dossiers `rewrites/<id>/` distincts). **D38 : tout le catalogue**, pas seulement deux ramifiés. Texte d’abord ; audio ensuite.

**Depuis F-NAR-024 (6 sept. 2026).** La **source** reste l’xlsx (`stories/arbres/`) : texte **et** params de prosodie. Un moteur en fait un JSON ; le TTS en fait l’audio. On n’écrit pas les histoires dans le JSON. Contrat : `stories/FORMAT_JSON_TTS.md`. **Priorité : qualité du texte Excel.**

**Interdit.** Liste de gestes : « Alice range le triangle. Alice range le rectangle. » Ce n’est pas une histoire. Personne n’achète ça.

**Obligatoire.** Monde (village, maison, jardin, saison) → désir du héros → petit imprévu → résolution → fin heureuse. La leçon se greffe. Papa/maman parlent. Troupe D16. POS-001. Ouverture inventée (D25).

## Passe 2 (3–6 ans)

La fusion n’est **pas** « le texte le plus long gagne ». C’est une **fusion éditoriale**.

| Oui | Non |
| --- | --- |
| Un enfant de 3–6 ans comprend sans aide | Phrases collées, slogans, « fesses sur la chaise » |
| Un seul fil (envie, poursuite, bateau…) | Tout le plot dans `P0000`, le reste répète |
| `P0000` = début + action, s’arrête avant la leçon | Dump goût + leçon + bilan dès le premier chunk |
| Question simple (1–3 mots de réponse) | Question qui recopie le slogan |
| Fin = ce qu’on a **vécu**, puis « L’histoire est finie. » | « L’histoire est finie. » seul, ou consigne de cours |
| Papa/maman parlent (bravo, question, discussion, adaptés à la scène) | « Papa sourit. » « Maman est là. » à la place de leur voix |
| Monde d’abord, détails, amorce **inventée** pour cette histoire (D25) | « X joue au salon. » / « Aujourd’hui X est avec papa. On va apprendre : … » / recopier « il était une fois » partout |

N1 : ~8 mots par phrase. N2 : < 16. Leçon **greffée**, jamais collée en recap.

**Durée ≥ 3 min.** Plusieurs passages. Certains portent une leçon, d’autres racontent. Une atomique peut greffer plusieurs leçons pour tenir 3 min. Allonger si le récit le demande.

Enfants nommés : Amir, Aniss, Sarah, Chouchou, Mila, Nino, Nina, Raphaël, Victorino, Victorina seulement. Un héros, au plus un copain/copine de la liste, papa et/ou maman.

## Passe 3 — ouverture du monde (F-NAR-009, D25)

L’entrée n’est plus un constat. Le premier passage **raconte un monde**, puis seulement l’action présente.

Les amorces « Il était une fois… » et « Ceci est l’histoire d’un enfant… » (textes complets Constantin / Luca / Céline dans `gestion_projet/decisions/ECHANGES.md` §7) sont des **exemples de manières**. Ce n’est **pas** un moule. Il faut être créatif. Deux histoires ne commencent pas pareil. Détails sensoriels (pluie, lumière, odeur, tapis, jouets, fenêtre). Puis : en ce moment.

Ramifiées : interdiction de « On va apprendre : {titre}. Voici le geste ». Le fil rouge porte la leçon.

Texte d’abord. **Pas d’audio** dans cette passe.

## Grille éditoriale (écoute, pas un cours)

Référence : `gestion_projet/feedback_chatgpt/exemple.txt` (Chouchou, *La boîte trop haute*).

| Oui | Non |
| --- | --- |
| Une envie concrète du héros (finir le bateau du puzzle) | Obtenir l’objet / la leçon comme tout le récit |
| Un obstacle (la boîte est trop haute) | La leçon résolue dès l’ouverture, puis on répète |
| L’enfant agit : prépare, demande, assemble, retrouve | L’adulte fait tout ; l’enfant écoute la consigne |
| La question arrive **au moment du besoin** | Question-slogan collée n’importe où |
| L’aide débloque l’aventure (papa donne la boîte) | Discours « il faut demander de l’aide » |
| La fin tient la promesse du début (le bateau est fini, on souffle sur la voile) | « Bravo, bon travail » sans clôture vécue |
| Après silence / mauvaise réponse : la narration reprend, sans verdict d’échec | « Non, ce n’est pas ça » |

Papa accompagne sans tout faire. La félicitation est rare et liée à un geste vu, pas un refrain.

## Passe 4 — étalon (F-NAR-018, `avis2.txt`)

TREE-AUT-001 (*Le bateau d’Amir et la rivière du jardin*) donne la **logique** : monde, désir concret, déclencheur, préparation, obstacle propre au lieu, résolution qui change la fin, retour à la maison. Ce n’est **pas** un moule de phrases.

- Oral : alterner très court et un peu plus lié. Pas une suite de « X, Y. »
- Pas de morale dite (« changer de chemin, ce n’est pas perdre »). L’enfant la voit.
- Un ramifié n’a pas 27 histoires distinctes si T1 ne change que l’accessoire. T1 doit changer le voyage.
- ATOM : un imprévu **pendant** le projet. Interdit le récap « J’ai dit… Bravo. » en fin.

Détail opérationnel (features) : **F-NAR-010 à F-NAR-015**, consignes `gestion_projet/feedback_chatgpt/f_04.txt`.

## JSON agent

Mêmes `chunk_id` et `kind`. Champs : `fil_rouge`, `title`, `chunks[]` avec `text`, `script`, `sons`, `length_scale_piper`, `rate_label`.

`sons` vide = silence. Bruit **puis** calme, jamais nappe. Script `role|phrase`. N1 phrases courtes. REGLES.md + D25.
