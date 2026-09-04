# Ce que l’audit ChatGPT change dans le travail

Sources (4 sept. 2026, commit `5e403fd`) : `Acomytha_Audit_2026-09-04.md`, `Acomytha_Audit_Histoires_2026-09-04.html`, `exemple.txt`.

Ce n’est **pas** une spec. C’est une lecture externe. On retient ce qui aide à mieux écrire et à ne pas vendre trop tôt.

**Veille (F-NAR-017, D32).** Un agent surveille ce dossier. Fichier nouveau ou changé → lecture → consignes éditoriales → TREE-AUT-001 et TREE-COL-001 (texte, pas d’audio). Les fichiers déjà dans `processed.json` ne sont pas relus tant que le contenu ne change pas. `NOTES.md` n’est pas un input ChatGPT.

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
