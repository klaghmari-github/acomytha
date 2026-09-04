# Règles éditoriales AcoMytha — génération d’histoires

Source : spécification fonctionnelle v2.0, validation VAL-HIST-001, taxonomie v1, Source Unique v3.0, Corrections v3.1.

Public : enfants 3–6 ans (N1 = 3–4, N2 = 4–5, N3 = 5–6). Audio seulement. Français quotidien.

## Non négociable

1. **Formulation positive** (POS-001 à POS-006). Dire *quoi faire*. Ne jamais décrire le geste dangereux, même pour l’interdire. Un choix de sécurité n’oppose jamais une option sûre à une option dangereuse imitable. Après une erreur, répéter seulement la conduite sûre.
2. **Monde jardin** (NEUT / GARDEN). Papa, maman, frère, sœur, école, parc, maison, repas, animaux, règles simples. **Absents** (on n’explique pas pour rejeter) : religion, politique, guerre, crime, tuerie, discours de genre, deux papas / deux mamans.
3. **Famille racontée** : `father_mother_children`. Pas de parent générique à la place de papa/maman.
4. **Comportement, pas étiquette** (NEU-002). Interdit : « il est méchant / bizarre / nul / hyperactif ». Attendu : geste, émotion, besoin.
5. **Pas de menace affective**. Jamais « maman ne t’aimera plus ».
6. **Pas de diagnostic nommé** dans l’audio enfant.
7. **Pas de franchise** (NAR-005). Personnages originaux.
8. **Compréhensible sans image** (NAR-004). Aucune consigne visuelle indispensable.
9. **Une leçon = un objectif observable**. Pas un thème flou.
10. **Preuve pédagogique minimale par chemin** (PED-010) : situation audible, enjeu, modèle de conduite sûre, mobilisation (question), confirmation positive, conséquence qui ne récompense pas l’inverse.
11. **Questions** : 1 à 3 mots de réponse, intentions fermées, relance, `NO_ANSWER` / défaut. Négation non fusionnée avec l’intention positive.
12. **N1** : phrases très courtes, 2 options max, répétition. **N2** : cause-conséquence. **N3** : jusqu’à 3 choix, transfert de leçon.
13. **Framing `positive_only_critical`** : sensibilité `enhanced`. Mains, pieds, place du corps, adulte nommé. Jamais d’opératoire du danger.
14. **Deux leçons critiques** (feu + prises, rue + balcon) ne s’empilent pas dans la même scène. On peut les enchaîner dans un arbre, scènes séparées.
15. **Moquerie** : brève, jamais le gag, jamais un surnom enseigné, réparation immédiate (NEU-004).
16. **Émotion** (EMO-001) : nom + cause simple + indice du corps + geste sûr. L’émotion n’est pas honteuse.
17. **Différences** : on joue ensemble. On ne commente pas le corps pour rabaisser.
18. **Secret** : surprise gentille ≠ malaise. Ce qui fait peur se raconte à papa ou maman (FAM.SEC.002).
19. **Respecter un adulte** n’efface pas le droit de dire non, de s’éloigner et de tout raconter à papa ou maman.
20. **Le générateur ne s’auto-approuve pas** (VAL-001). Statut initial : `PENDING`.
21. **Troupe enfant fermée.** Les enfants nommés sont seulement : **Amir, Aniss, Sarah, Chouchou, Mila, Nino, Nina, Raphaël, Victorino, Victorina**. Pas d’autre prénom d’enfant. Dans **une** histoire : un seul héros, au plus **un** autre enfant de la liste, plus papa et/ou maman. Pas de foule : l’enfant se perd.
22. **Adultes parlent** (D20). Papa et maman ont des répliques, adaptées à la scène. Interdit de remplacer leur voix par un remplissage (« papa sourit », « maman est là »). Bon geste : féliciter (« Bravo, tu as fait du bon travail. »). Bêtise : discuter, demander la conduite (« Tu as fini de ranger tes jouets ? »), sans décrire le geste interdit, sans humilier (POS-001).
23. **Ouverture et monde** (D25). On n’entre jamais dans l’action comme un constat sec (« X joue au salon. »). D’abord un monde : lieu, famille, temps, atmosphère, détails sensoriels ; ensuite seulement « en ce moment ». Chaque histoire a **sa** façon de commencer. Les formules du type « il était une fois » sont des **exemples**, pas un modèle à recopier. L’enfant aime les détails : textures, bruits, lumières, odeurs, petits gestes. Interdit : deux histoires qui s’ouvrent pareil.

## Troupe (enfants)

| Prénom | Rôle typique |
| --- | --- |
| Amir, Aniss, Nino, Raphaël, Victorino | héros / copain |
| Sarah, Mila, Nina, Victorina | héroïne / copine |
| Chouchou | enfant (surnom, un seul personnage) |

Adultes : papa, maman (toujours nommés ainsi). Maîtresse, grand-père, grand-mère seulement si la leçon l’exige, un seul adulte extra max.

## Interdits CHILD_AUDIO (liste non exhaustive)

Religion, prière, église, mosquée, synagogue, dieu comme culte, politique, élection, guerre, soldat, arme, bombe, tuer, crime, sang, vengeance, deux papas, deux mamans, LGBT, transgenre, pronom choisi, hyperactif, autiste, TDAH, « maman/papa ne t’aimera plus », insultes, surnoms humiliants, mode d’emploi de bagarre, course sur la chaussée, avancer au rouge comme option, objet dans une prise, saut depuis un balcon, ouvrir une portière en marche, couteau/feu comme jeu.

## Structure d’un chemin

Accroche orale **du monde** (où, qui, quel temps, quelle maison) → on arrive à « en ce moment » → héros, lieu, envie concrète → petit problème lié à la leçon → exploration non humiliante → interaction (question ou choix) → résolution de la branche → fin naturelle, encore vécue (pas un slogan).

Types de nœuds : `audio`, `question_comprehension`, `question_lesson`, `choice_story`, `feedback`, `transition`, `silence_check`, `ending`.

## Durée

- **Minimum 3 minutes** d’écoute (180 s), atomique ou ramifiée. Jamais plus court.
- On **allonge** si le récit le demande. Pas de plafond pédagogique : le fil rouge décide.
- Pour tenir 3 min : **plusieurs passages**. Certains passages portent une leçon, d’autres avancent seulement l’histoire.
- Même **sans ramification**, plusieurs leçons peuvent se greffer (pour compléter les 3 min), sauf si le framing est `positive_only_critical` (alors une seule leçon critique, d’autres leçons non critiques possibles).

## Atomique (sans bifurcation)

- Un seul chemin racine → feuille.
- Une leçon principale. D’autres leçons **autorisées** si elles se vivent dans le récit (pas un cours collé). Secondaire critique interdite.
- Plusieurs passages. Une `question_lesson` (ou compréhension) + confirmation + ending.
- Durée **≥ 3 min**. Plus long si la narration l’exige. Texte parlé, phrases courtes.

## Ramifiée (bifurcation)

- Au moins **3 choix** au premier embranchement.
- Chaque branche de niveau 1 a **au moins 3** sous-branches.
- Chaque sous-branche de niveau 2 a **au moins 3** feuilles (niveau 3).
- **Maximum 3 niveaux** hiérarchiques de choix.
- Les choix narratifs (`choice_story`) sont **neutres** (cuisine / jardin / chambre), pas un test « bien vs dangereux ».
- Chaque chemin racine-feuille porte les `required_messages` de la leçon principale de ce chemin.
- Plusieurs fins distinctes autorisées (NAR-001).
- Silence / ambiguïté / erreur : `default_next` défini, correction positive seulement.

## Ton

Vivant, concret, sensoriel (bruits, goûts, textures) sans spectacle du danger. Répéter les mots-clés de la leçon. Nommer papa ou maman, pas « un parent ».

Papa et maman **parlent**. Le narrateur décrit le décor et les gestes ; il ne mime pas l’adulte par un sourire ou une présence muette. L’adulte félicite, discute, pose une question **de la scène** (pas un slogan collé). Les exemples (« Bravo », « Tu as fini de ranger tes jouets ? ») s’adaptent : repas, jeu, rangement, attente… jamais une phrase unique recopiée.

**Ouverture (D25).** L’entrée n’est pas brutale. On installe un monde avant l’action. Exemples de *manières* (ce ne sont **pas** des textes à coller, il faut inventer à chaque histoire) :

- Conte : « Il était une fois, dans un petit village, une petite famille heureuse… Un jour de pluie, l’enfant n’a pas pu aller au parc. En ce moment même, il joue au salon. »
- Présentation : « Ceci est l’histoire d’un enfant heureux qui s’appelait… Il vivait avec papa et maman dans une belle maison. En ce moment, dans ce village, il pleut… »

D’autres manières existent : une odeur qui entre par la fenêtre, un bruit de gouttière, une lumière sur le plancher, un doudou qui attend, une rue mouillée vue du canapé. **Être créatif.** Ne pas se limiter à ces exemples. Ne pas commencer deux fois de la même façon. Détails concrets, phrases courtes (N1 ~8 mots, N2 < 16). Adultes = papa / maman (pas un prénom d’adulte à la place). Troupe enfant fermée (règle 21).
