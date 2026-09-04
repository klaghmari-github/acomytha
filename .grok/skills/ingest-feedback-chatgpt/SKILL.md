---
name: ingest-feedback-chatgpt
description: >
  Ingest a new ChatGPT feedback file from gestion_projet/feedback_chatgpt/,
  extract editorial consignes, and improve the kept stories (TREE-AUT-001,
  TREE-COL-001) in text only. Use when a new file appears in feedback_chatgpt,
  when the user mentions ChatGPT audit/feedback/f_04, or when running
  /ingest-feedback-chatgpt.
---

# Ingest feedback ChatGPT (F-NAR-017)

Dossier worktree : `gestion_projet/feedback_chatgpt/`.
Dossier **SSD** (là où les fichiers sont souvent déposés) : `/media/laghmari/ssd-data/dev/akomytha/gestion_projet/feedback_chatgpt/`.
`scan` / `watch` regardent **les deux**. `claim` copie vers le worktree.
Ledger : `gestion_projet/feedback_chatgpt/processed.json`.
Outil : `python3 stories/outils/watch_feedback_chatgpt.py`.

**D35 — pas de conflit.** Le watchdog (inotify / scheduler) **signale seulement**. Il ne `claim` pas, ne réécrit pas, ne commit pas. L’agent de la conversation principale priorise et applique.

## Quand s’arrêter tout de suite

```bash
python3 stories/outils/watch_feedback_chatgpt.py scan
```

Si `"files": []` : une ligne « Rien de nouveau. » et **stop**. Pas de réécriture.

## Sinon, pour chaque fichier

1. **Claim** (évite un double traitement avec le scheduler) :
   `python3 stories/outils/watch_feedback_chatgpt.py claim <path>`
   - exit 2 = déjà `done` pour ce hash → skip.
   - exit 3 = déjà `processing` → skip.
2. **Lire** le fichier. HTML gitignoré / trop gros : extraire le fond (titres, listes, exemples). Ne pas coller 24 Mo dans le récit.
3. **Séparer** :
   - **Éditorial** (envie, obstacle, fin, questions, ramifications, voix, troupe, POS-001) → à appliquer.
   - **Commerce / moteur / ASR / Stripe / audio bake** → une puce dans `NOTES.md` section « Pas maintenant ». Pas une feature de plus ce tour.
4. **Comparer** à ce qui existe déjà : `stories/REWRITE.md`, F-NAR-008…016, `NOTES.md`, `f_04.txt`. Si c’est déjà dit : noter dans `NOTES.md` « déjà couvert » et **ne pas** réécrire les xlsx.
5. **Consignes vraiment nouvelles** : une entrée courte dans `NOTES.md` ; si ça tient en feature, F-NAR-01x dans `Features.md` (pas de doublon).
6. **Histoires** (texte seulement, **pas d’audio**) :
   - Actif : `TREE-AUT-001` (`stories/arbres/`).
   - Archive : `TREE-COL-001` (`stories/archive/arbres/`) — dump à la main depuis ce chemin, `apply` n’y va pas tout seul.
   - Pas les 685 atomiques, pas les 763 autres TREE.
   - Garder `chunk_id`, `kind`, graphe `option_*_next_chunk`.
   - Patcher `expected_answer` / `accepted_examples` / `retry_prompt` / `characters` (apply ne le fait pas).
   - Preuve : `stories/rewrites/<id>/RELECTURE.md` (F-NAR-015).
7. **Contraintes produit** (ne pas les violer pour plaire à ChatGPT) : D16 troupe, papa/maman, POS-001, D20 adultes parlent, D25 monde d’abord, D29 `main` only, `feat(F-XXX):`. Décider, ne pas demander d’avis.
8. **Done** :
   `python3 stories/outils/watch_feedback_chatgpt.py done <path> --note "…"`
9. Commit ciblé (pas `git add -A`) + push origin et github si des xlsx / NOTES ont changé.

`NOTES.md` n’est **pas** un fichier ChatGPT : ne pas l’ingérer.
