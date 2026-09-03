# Sentier — gestion de projet

Un produit, peu de documents. Chaque fichier a un rôle unique. Les features **pointent** vers les stratégies ; elles ne les recopient pas.

| Fichier | Rôle |
| --- | --- |
| [`specification/Sentier_Specification.md`](specification/Sentier_Specification.md) | **Spec unique** : produit, public, règles, leçons, runtime. Fusionne les anciens docx/xlsx de cadrage. |
| [`backlog/Features.md`](backlog/Features.md) | Backlog développable (`F-…`). Une ligne = une branche Git. |
| [`strategies/STRAT-001-validation.md`](strategies/STRAT-001-validation.md) | Comment un texte / un audio est accepté ou refusé. |
| [`strategies/STRAT-002-audio.md`](strategies/STRAT-002-audio.md) | MP3, rythme, Piper (0 € hors Heavy), chiffrement, lecture RAM. |
| [`strategies/STRAT-003-modele-donnees.md`](strategies/STRAT-003-modele-donnees.md) | Tables relationnelles histoire ↔ leçon ↔ chunk, identifiants. |
| [`strategies/STRAT-004-moteur-lecture.md`](strategies/STRAT-004-moteur-lecture.md) | Jour / nuit, enchaînement des chunks, préchargement. |
| [`consignes.txt`](consignes.txt) | Git : une branche par feature, textes d’abord. |

**Données, pas de spec :** leçons dans `stories/referentiel/lecons.xlsx`, liaisons dans `lecon_histoires.xlsx`. Arbres dans `stories/arbres/*.xlsx`.

**Interdit.** Dupliquer une règle dans trois fichiers. Si ça change, on change **un** endroit (spec ou stratégie) et le backlog ne fait que référencer.
