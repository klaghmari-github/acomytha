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

Une histoire à la fois (plusieurs agents **sur la même** histoire). Texte d’abord ; audio plus tard.

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

## JSON agent

Mêmes `chunk_id` et `kind`. Champs : `fil_rouge`, `title`, `chunks[]` avec `text`, `script`, `sons`, `length_scale_piper`, `rate_label`.

`sons` vide = silence. Bruit **puis** calme, jamais nappe. Script `role|phrase`. N1 phrases courtes. REGLES.md + D25.
