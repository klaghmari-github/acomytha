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

## Pas maintenant (chantier, pas une feature de plus ce tour)

Commerce démo vs Stripe, vente sans audio, voix facturée sans enregistrement, commandes sans livraison, ASR, hors-ligne, FX WAV manquants, durées < 3 min sur les 2 audios témoins, `validate.py` encore collé aux JSON disparus, collection pilote 12+3 avant vente.

La vitrine peut rester chaleureuse ; ne pas compter comme « produit disponible » un fichier sans audio validé.
