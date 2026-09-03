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

## Interdits CHILD_AUDIO (liste non exhaustive)

Religion, prière, église, mosquée, synagogue, dieu comme culte, politique, élection, guerre, soldat, arme, bombe, tuer, crime, sang, vengeance, deux papas, deux mamans, LGBT, transgenre, pronom choisi, hyperactif, autiste, TDAH, « maman/papa ne t’aimera plus », insultes, surnoms humiliants, mode d’emploi de bagarre, course sur la chaussée, avancer au rouge comme option, objet dans une prise, saut depuis un balcon, ouvrir une portière en marche, couteau/feu comme jeu.

## Structure d’un chemin

Accroche orale → héros, lieu, objectif concret → petit problème lié à la leçon → exploration non humiliante → interaction (question ou choix) → résolution de la branche → fin naturelle.

Types de nœuds : `audio`, `question_comprehension`, `question_lesson`, `choice_story`, `feedback`, `transition`, `silence_check`, `ending`.

## Atomique (sans bifurcation)

- Un seul chemin racine → feuille.
- Une leçon principale. Secondaires interdites si framing critique.
- Une `question_lesson` (ou compréhension) + feedback positif + ending.
- Durée cible 90–180 s (N1) / 120–240 s (N2/N3). Texte parlé, phrases courtes.

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
