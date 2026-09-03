# STRAT-001 — Validation

**Référencé par :** `F-VAL-001`, `F-VAL-002`, `F-NEU-005`, `F-GEN-002`, `F-AUD-002`.  
**Règles métier :** `specification/AcoMytha_Specification.md` §3, `stories/REGLES.md`.

## 1. Principe

Un outil ne s’auto-approuve pas. **Règle bloquante > score moyen.** Une histoire n’est publiable que si **tous** les chemins accessibles passent.

## 2. Texte (`APPROVED_TEXT`)

Validateur déterministe : `stories/outils/validate.py`.

| Famille | Exemples bloquants |
| --- | --- |
| Structure | Pas de racine unique, id dupliqué, cycle, feuille manquante, chemin non terminable |
| Pédagogie | `required_messages` absents d’un chemin, leçon sans conduite sûre |
| Positif | « ne … pas + verbe dangereux », option qui nomme un geste interdit |
| Neutralité | religion, politique, guerre, crime, étiquette diagnostique |
| Famille | rupture `father_mother_children` dans l’audio enfant |
| Oral | phrase trop longue pour N1, question sans intention 1–3 mots |

Sorties : `APPROVED_TEXT` | `REVISION_REQUIRED` | `REJECTED`. Rapport lisible parent (`F-VAL-002`) : « bloquée parce que… ».

Le corpus actuel (1445 JSON) est `APPROVED_TEXT`. Ce n’est **pas** un paquet audio.

## 3. Audio (`APPROVED_AUDIO`)

Après bake (`STRAT-002`) :

1. Fichier `.chk` lisible (en-tête + tag GCM).
2. Déchiffrement test → MP3 décodable, durée plausible.
3. Loudness ~−19 LUFS, crête &lt; −1,5 dBTP, pas de clipping.
4. ASR vs **texte nu** (sans balises de rythme). Divergence bloquante.
5. Prononciations sensibles : prénoms, `trottoir`, `stop`, `papa`, `maman`.
6. Tous les `chunk_id` du graphe ont un blob. Orphelin = refus.

Écoute humaine : **toutes** les histoires `positive_only_critical` ; **échantillon** du reste. 260 h d’écoute intégrale n’est **pas** un plan.

Puis `APPROVED_PACKAGE` : manifeste signé + blobs. Une branche KO invalide l’histoire.

## 4. Simulateur de chemins (`F-GEN-002`)

Avant publication audio : chaque racine→feuille. Durées, questions, scripts positifs, continuité des personnages. Un chemin non simulable n’est pas publié.
