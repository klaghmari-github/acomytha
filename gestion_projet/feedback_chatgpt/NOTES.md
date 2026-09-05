# Ce que l’audit ChatGPT change dans le travail

Sources (4 sept. 2026, commit `5e403fd`) : `Acomytha_Audit_2026-09-04.md`, `Acomytha_Audit_Histoires_2026-09-04.html`, `exemple.txt`.

Ce n’est **pas** une spec. C’est une lecture externe. On retient ce qui aide à mieux écrire et à ne pas vendre trop tôt.

**Veille (F-NAR-017, D32, D35).** Watchdog **inotify** worktree + SSD. Fichier nouveau → `ACTION_REQUIRED` seulement. Le traitement est fait par l’agent principal, jamais par le scheduler en parallèle.

Passe `avis1.txt` (4 sept. soir, SSD) :

- **Déjà couvert** en règles : monde d’abord (F-NAR-009), désir ≠ leçon (F-NAR-010), vraie fin (F-NAR-011), chemins à conséquences (F-NAR-014), pas de gabarit « il était une fois ».
- **Nouveau et appliqué** sur TREE-AUT-001 seulement : T3 n’est plus le même geste (milieu / bord / sac). Chaque lieu a son obstacle et ses trois issues. Titre : *Le bateau d’Amir et la rivière du jardin*.
- TREE-COL-001 : pas le même gabarit (T3 = qui pousse). Pas réécrit ce tour.
- Commerce « acheter / réécouter » : critère éditorial, pas une feature boutique.

Passe `exemple2.txt` + `Acomytha_Avis_Paquet_Prioritaire_88534be.md` (4 sept. soir) :

- AUT : projet **bateau / flaque** ; le sac sert ; les fins montrent le bateau qui flotte.
- COL : **voyage des pommes** mené par les enfants ; T3 = qui pousse (plus l’heure) ; politesse rare.
- Relances sans « Dis : ». Leçons secondaires : garder seulement si le récit les vit. SSML aligné sur le texte.
- N1 ramifié : **3 options conservées** (structure d’arbre, D33). HTML 24 Mo = déjà l’audit md.

## Déjà appliqué

- **Jour / nuit (F-PLY-001).** `night_policy=auto_default` ne doit plus court-circuiter les choix **le jour**. Nuit = branche par défaut. `StoryEngine.js`.
- **Grille éditoriale** dans `stories/REWRITE.md`, calquée sur *La boîte trop haute* (`exemple.txt`) : envie, obstacle, l’enfant agit, question au bon moment, fin qui tient la promesse.
- **f_04.txt → features F-NAR-010…015, D30.** Désir ≠ leçon, vraie fin, chaîne question, chemins, preuves de relecture.

## À garder en tête (réécritures)

- L’enfant **porte** l’action. L’aide débloque l’aventure, ce n’est pas un cours.
- Question + réponse attendue + correction **ensemble** (éviter « On lève quoi ? » → « attendre »).
- Pas de « Que fait-on ? » en gabarit si ça ne colle pas à la scène.
- Pas « près de le bac » / « à le jardin ».
- Personnages : `characters`, texte et relances **d’accord** (plus Lina si Sarah est dans le récit).
- « Bravo / bon travail » : rare, lié à un geste vu.
- Ramifiées : le choix doit **changer la suite**, pas seulement le lieu ou le goûter.
- Réponses acceptées larges quand c’est juste (« papa », « maman », « un adulte ») ; silence = la narration reprend, sans échec.

Passe `avis2.txt` (4 sept. 23:58, SSD, commit GitHub `ae4eb67` alors) :

- **Déjà couvert** : désir ≠ leçon, monde d’abord, vraie fin, chemins à conséquences, AUT-001 bateau/jardin comme direction, Bravo/bon travail.
- **Nouveau — structure, pas le verbe.** TREE-AUT-001 est l’**étalon de logique** (désir, obstacle, action, conséquence, retour), **pas** un gabarit de phrases. Ne pas recopier « capitaine », « plic/ploc », « volet jaune » partout.
- **Nouveau — oral fluide.** Alterner phrases très courtes et phrases un peu plus liées. Éviter l’accumulation « Celle-ci, la coque. / Le manteau, Amir. »
- **Nouveau — pas de morale énoncée.** « Changer de chemin, ce n’est pas perdre » doit sortir de l’action, pas de la bouche de papa.
- **Nouveau — 9 aventures, pas 27.** T1 (manteau / bottes / linge) change le voyage (bruit, mouillé, sécher) ; la diversité vraie = destination × résolution. Ne pas vendre 27 récits distincts.
- **Nouveau — COL-001 trop mécanique.** Il manque un vrai obstacle, T3 décoratif, fin « L’histoire est finie ». À réécrire avant d’en faire une vitrine.
- **Nouveau — gabarit ATOM.** Décor → leçon → question → récap n’est pas une histoire. Exemples cités : *Sarah et le dessin du soleil* (joie répétée), *La boîte trop haute* (j’ai appelé / j’ai dit le besoin).
- **Commerce « 20 histoires irréprochables, arrêter d’en produire »** : **pas maintenant comme politique.** D38 : tout le catalogue. On applique l’étalon, on ne réduit pas le corpus.

## Pas maintenant (chantier, pas une feature de plus ce tour)

Commerce démo vs Stripe, vente sans audio, voix facturée sans enregistrement, commandes sans livraison, ASR, hors-ligne, FX WAV manquants, durées < 3 min sur les 2 audios témoins, `validate.py` encore collé aux JSON disparus, collection pilote 12+3 avant vente.

La vitrine peut rester chaleureuse ; ne pas compter comme « produit disponible » un fichier sans audio validé.

Passe `examples/example2/` (5 sept. matin, SSD) — **F-NAR-019**, commit `45e0e23c` :

- **Nouveau.** `text_xai_tags` était identique à `text` sur 16 499 segments : inutile. Remplir tags expressifs + `notes` (arc, intention, émotion, intensité, destinataire, sous-texte, tempo, sourire, respiration).
- **Nouveau.** Chaque chemin ramifié = une vraie histoire (imprévu, 1re tentative ratée, péripéties, climax, fin qui paie le début). 27 fins distinctes, pas 27 calques.
- **Nouveau.** Vocabulaire simple mais divers ; tics corpus (« tout doux », « encore », « déjà ») à casser. Style humain, pas fiche pédagogique.
- **Étalon.** TREE-COL-015 *Aniss et le secret de la trace d'argent* (example2) : à intégrer après `_lib.check` (couper phrases N2, un merci vécu). Ne pas coller l’escargot ailleurs.
- **Priorité audit.** P0 = 25 ramifiés (score ~37–54), dont COL-015/016/021/025/026/030/031/034. Puis P1 (68), P2 (58). ATOM ensuite.
- Apply/dump : colonnes vocales persistées (`rewrite_story.py`).

Passe `examples/example1/` (5 sept., SSD puis worktree) — **intégré** dans `TREE-AUT-001` :

- **Déjà couvert** : désir bateau/jardin, 9 aventures = destination × résolution, pas de morale dite, graphe 86 chunks.
- **Nouveau et gardé.** T1 ne prive plus d’un objet : on choisit **lequel on prépare d’abord**, puis manteau + bottes + linge partent tous. Les trois réapparaissent à l’arrivée et au retour.
- **Nouveau et gardé.** Urgence douce (le soleil sèche l’eau). Promesse (rapporter une histoire / un trésor) tenue par un souvenir distinct à chaque fin.
- **Nouveau et gardé.** T3 bac : canal ou piste de sable, plus « un autre bateau » (ça cassait le projet promis).
- **Modifié à l’intégration (N1).** Titre catalogue inchangé. « en ce moment » ajouté. « aujourd’hui, » / possède / expédition / proue / immobilise / scintille adoucis. Papa : « Merci, on t’attendra. »
- **Pas copié tel quel.** « Capitaine / navire / volet jaune » restent **dans cette histoire** (c’est l’étalon bateau). Toujours interdit de les recoller ailleurs (avis2).
- **Passe orale.** Les puces « première / deuxième / troisième » et les faits empilés ont été reliés avant le bake audio.
