# Passe F-NAR-019 — récit humain + voix (ramifiés)

Texte seulement. Pas d’audio. Pas de git. Pas de `pkill`. Décider, ne pas demander.

Lis aussi : `AGENT_PROMPT.md`, `AGENT_BRIEF.md`, `_lib.py`,
`CREATIVITY_BRIEF_EXAMPLE4.md` (**obligatoire** — édition v2 : ouvertures variées, indice du début, corps, 2e ruse),
`CREATIVITY_BRIEF_EXAMPLE3.md` (objets/lieux, pas le gabarit),
`gestion_projet/feedback_chatgpt/examples/example1/RELECTURE.md`,
`gestion_projet/feedback_chatgpt/examples/example2/raw.js` (étalon **vocal**, pas le récit à coller),
`gestion_projet/feedback_chatgpt/examples/example2/RELECTURE (1).md`,
et **trois** fichiers `example4/acomytha_histoires_*.txt` (ceux de ta mission).
La ligne de **ton** arbre dans `example2/AUDIT_EDITORIAL_VOCAL_CATALOGUE (1).md`.

## Barre

Quelqu’un veut quelque chose **maintenant**. Un imprévu concret l’en empêche. La **première idée échoue**. Un choix **change l’action**. La fin **paie** une image du début. La leçon se **voit**, elle n’est pas dite.

Chaque ramification est **une autre histoire** : autre obstacle, autre climax, autre fin (détail unique). Idéalement une nuance de leçon différente (vécue). 27 fins textuellement distinctes. Si T1/T2/T3 ne changent que le lieu, **refaire** le contenu (garder `chunk_id` / graphe).

Style : oral d’humain, 3–6 ans. Vocabulaire simple et **divers**. Pas de tic « tout doux / encore / déjà / tout calme ». Phrases courtes **et** un peu liées. Émotions incarnées (impatience, découragement, fierté calme), pas « X agit ».

TTS, **par chunk**, selon la fonction (voir `raw.js` `profiles`) :
- `length_scale_piper`, `rate_label`, `pause_after_ms`, `pause_before_ms`, `pause_sentence_ms`
- `pitch_label` / `pitch_ssml` / `pitch_xai_tag`, `volume_label` / `volume_db`
- `text_ssml` (prosody + emphasis + break), `text_xai_tags` (`<slow>`, `<soft>`, `<emphasis>`, `[pause]`)
- `notes` : `arc=…; intention=…; emotion=…; intensite=1|2|3; destinataire=…; sous_texte=…; tempo=…; sourire=…; respiration=…`
- `style_energy`, `style_contour`, `noise_scale_piper`
- `slow` seulement : choix, danger doux, émotion sensible. Action = plus vif.

`check()` `_lib.py` doit passer : N1≤10 / N2≤15 / N3≤16 mots/phrase ; `en ce moment` ; papa/maman parlent + une question + **un** merci ou bravo **vécu** ; pas FORBIDDEN ; troupe D16 ; pas 4 puces d’affilée.

## Livrable

```
python3 stories/outils/rewrite_story.py dump <ID>
# écrire stories/rewrites/<ID>/merged.json + RELECTURE.md
# check() OK. Ne pas apply (le parent l’appliquera).
```
