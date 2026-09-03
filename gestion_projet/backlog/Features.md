# Sentier — backlog features

**Version :** 3.0 — 3 septembre 2026. Remplace `Sentier_Backlog_Features_v2.0.xlsx`.  
**Branche :** `feat/<ID>-<slug>` (voir `consignes.txt`). L’ID ne change plus.  
**Spec :** `specification/Sentier_Specification.md`. Les colonnes *Strat* pointent le document d’architecture, pas une copie.

Priorités : **P0** première écoute réelle · **P1** MVP familles · **P2** juste après · **P3** v2 (ne pas démarrer).

Phases : 0 cadrage · 1 contenu · 2 MVP mobile · 3 interaction fermée · 4 renouvellement · 5 leçons parentales · 6–7 hors MVP.

---

## Nouveautés v3 (à faire en premier après les textes)

| ID | Epic | Titre | Prio | Phase | Strat | Dépendances |
| --- | --- | --- | --- | --- | --- | --- |
| F-NAR-007 | Moteur | Identifiants chunks path-encodés + compilateur JSON→chunks | P0 | 0 | STRAT-003 | F-NAR-001 |
| F-DAT-001 | Référentiel | SQLite histoire ↔ leçon ↔ chunk, dossier `chunks/` plat | P0 | 0 | STRAT-003 | F-NAR-007, F-TAX-002 |
| F-AUD-004 | Audio | Chiffrement AES-GCM, lecture RAM, prefetch N+1 | P0 | 2 | STRAT-002 | F-AUD-001, F-SEC-001 |
| F-AUD-005 | Audio | Bake Piper → MP3 64k, 0 €, plans via Heavy | P0 | 1 | STRAT-002 | F-AUD-001, F-GEN-001 |
| F-PLY-005 | Lecture | Délai 3 s, une relance, choix auto ; nuit saute questions et branchements | P0 | 2 | STRAT-004 | F-PLY-002, F-PLY-003 |
| F-INT-005 | Interactions | `passage_question` : attente, similarité future, phrases moteur « oui / presque » | P0 | 2 | STRAT-004 | F-INT-001, F-PLY-005 |

### F-NAR-007 — Identifiants chunks

Racine `CHK_T0000_P0000`. Branchement `CHK_T0001_P0000`, options `…_O000k`, suites `…_P000k`. Trois niveaux max par concatenation `_T000n`. Pas de `…_Txxxx_P0000` fils = fin. Compilateur depuis `stories/*.json`. Détail : **STRAT-003**.

### F-DAT-001 — Catalogue relationnel

Tables `lesson`, `story`, `story_lesson`, `chunk`, `chunk_link` (exceptions). Le parent coche des `lesson_id` → téléchargement de **histoires entières**. Duplication des passages entre histoires : voulue. Un dossier `chunks/`. **STRAT-003**.

### F-AUD-004 — Protection

`.chk` = AES-256-GCM(MP3). Clé au Keystore/Keychain. Jamais de MP3 en clair sur disque. Décryptage chunk par chunk en RAM. **STRAT-002** §5.

### F-AUD-005 — Synthèse sans API payante

Heavy = `narration_plan` seulement. Fichiers = Piper local + ffmpeg MP3. Pas de `POST /v1/tts`. **STRAT-002** §2.

### F-INT-005 — Question d’écoute (ne branche pas)

Chunk `passage_question` : une question, **une** fois, `wait_ms` (défaut 3000). Le cours de l’histoire **ne change pas**. Ensuite le moteur enchaîne le passage de confirmation (conduite sûre).

Aujourd’hui : timeout → on continue.  
Plus tard : capter la réponse enfant, similarité avec `expected_answer` / `accepted_examples`.

Phrases moteur (colonnes Excel + audio court réutilisable) :

- similarité haute → `engine_ok_text` : « Oui, c’est la bonne réponse. »
- moyenne → `engine_near_text` : « Tu étais presque. »
- silence → `engine_timeout_text` : « On continue. »

Puis lecture du chunk confirmation. Nuit : skip (`night_policy=skip`). Source : feuille `chunks` des `.xlsx`.

### F-PLY-005 — Tempo et nuit

Défaut 3 s, paramétrable, une répétition optionnelle, puis `default_option`. Nuit : skip `listen_question` et skip branchement. **STRAT-004**.

---

## Features existantes (IDs stables)

Les descriptions longues restent celles du v2.0 ; ci-dessous l’index + le lien d’architecture. Statut : textes `F-GEN-001` / validateurs partiellement faits sur la branche corpus.

| ID | Epic | Titre | P | Phase | Strat |
| --- | --- | --- | --- | --- | --- |
| F-ACC-001 | Compte | Création de compte parent | P0 | 2 | spec §2 |
| F-ACC-002 | Compte | Connexion multi-appareils | P1 | 2 | — |
| F-ACC-003 | Compte | Consentements et portabilité | P1 | 2 | — |
| F-SEC-001 | Sécurité app | Code parental | P0 | 2 | STRAT-002 (unwrap clé) |
| F-SEC-002 | Sécurité app | Cloisonnement mode enfant | P0 | 2 | spec §2 |
| F-PRF-001 | Profils | Profils enfants isolés | P0 | 2 | spec §2 |
| F-PRF-002 | Profils | Niveaux N1 N2 N3 | P0 | 1 | spec §2 |
| F-TAX-001 | Référentiel | Taxonomie 3 niveaux | P0 | 0 | STRAT-003, `lecons.xlsx` |
| F-TAX-002 | Référentiel | Fiche leçon versionnée | P0 | 0 | STRAT-003 |
| F-TAX-003 | Référentiel | Priorités / exclusions parent | P0 | 2 | STRAT-003 §3 téléchargement |
| F-TAX-004 | Référentiel | Versions et couverture | P2 | 4 | STRAT-001 |
| F-NEU-001 | Éditorial | Vocabulaire neutre | P0 | 0 | spec §3, REGLES.md |
| F-NEU-002 | Éditorial | Formulation positive | P0 | 0 | spec §3 |
| F-NEU-003 | Éditorial | Émotions nommées | P1 | 1 | REGLES.md |
| F-NEU-004 | Éditorial | Différences / moqueries | P1 | 1 | REGLES.md |
| F-NEU-005 | Éditorial | Validateur neutralité | P0 | 1 | STRAT-001 |
| F-NAR-001 | Moteur | Modèle histoire / chunk / branche | P0 | 0 | **STRAT-003** (remplace l’arbre de dossiers) |
| F-NAR-002 | Moteur | Exécution locale | P0 | 2 | STRAT-004 |
| F-NAR-003 | Moteur | Ordonnanceur d’histoires | P0 | 2 | spec §1 |
| F-NAR-004 | Moteur | Sessions et durées | P1 | 2 | STRAT-002 (duration_ms) |
| F-NAR-005 | Moteur | Reprise | P0 | 2 | STRAT-004 §5 |
| F-NAR-006 | Moteur | Défaut et convergence | P1 | 3 | STRAT-004 |
| F-INT-001 | Interactions | Questions fermées | P1 | 3 | STRAT-004 §3 |
| F-INT-002 | Interactions | Reco vocale fermée | P1 | 3 | STRAT-004 |
| F-INT-003 | Interactions | Correction positive | P1 | 3 | spec §3, STRAT-004 |
| F-INT-004 | Interactions | Repli tactile | P2 | 3 | — |
| F-PLY-001 | Lecture | Lecteur écran pauvre | P0 | 2 | STRAT-004 |
| F-PLY-002 | Lecture | Mode jour | P0 | 2 | STRAT-004 §3 + F-PLY-005 |
| F-PLY-003 | Lecture | Mode nuit | P1 | 2 | STRAT-004 §4 + F-PLY-005 |
| F-PLY-004 | Lecture | Hors connexion | P0 | 2 | STRAT-002, STRAT-004 §6 |
| F-FOR-001 | Forêts | Forêt parentale par leçons | P0 | 2 | STRAT-003 |
| F-FOR-002 | Forêts | Élagage sûr | P1 | 2 | STRAT-003 (histoire entière) |
| F-FOR-003 | Forêts | Jauge | P1 | 2 | — |
| F-LOC-001 | Stock | Politique 10/20/50/100 | P1 | 4 | — |
| F-LOC-002 | Stock | Paquets, checksums, activation atomique | P0 | 2 | STRAT-002 §6 (`.chk` + sqlite) |
| F-LOC-003 | Stock | États AVAILABLE… | P0 | 2 | — |
| F-REN-001 | Renouvellement | Auto | P1 | 4 | — |
| F-REN-002 | Renouvellement | Éviction / cycles | P1 | 4 | — |
| F-REN-003 | Renouvellement | Historique léger | P1 | 4 | — |
| F-PAR-001 | Espace parent | Tableau de bord | P1 | 2 | — |
| F-PAR-002 | Espace parent | Actions sur une histoire | P1 | 2 | — |
| F-PAR-003 | Espace parent | Préécoute (déchiffre, ne compte pas) | P0 | 2 | STRAT-002 |
| F-PAR-004 | Espace parent | Signalement | P1 | 2 | — |
| F-PAR-005 | Espace parent | Politique d’approbation | P2 | 2 | STRAT-001 |
| F-CUS-001 | Leçons parentales | Saisie encadrée | P2 | 5 | hors MVP |
| F-CUS-002 | Leçons parentales | Isolation | P2 | 5 | hors MVP |
| F-GEN-001 | Production | Chaîne amont (textes : **fait** sur feat corpus) | P0 | 1 | STRAT-001 |
| F-GEN-002 | Production | Simulateur de chemins | P0 | 1 | STRAT-001 §4 |
| F-VAL-001 | Production | Validateurs auto | P0 | 1 | STRAT-001 |
| F-VAL-002 | Production | Rapport parent | P1 | 1 | STRAT-001 |
| F-AUD-001 | Audio | Un blob par chunk (plus « nœud dossier ») | P0 | 1 | STRAT-002, STRAT-003 |
| F-AUD-002 | Audio | Durée, loudness, pauses | P0 | 1 | STRAT-002 |
| F-AUD-003 | Audio | Voix unique / histoire | P2 | 2 | STRAT-002 §4 |
| F-HIS-001 | Suivi | Journal d’écoute | P1 | 2 | STRAT-004 |
| F-HIS-002 | Suivi | Vue parent | P2 | 2 | — |
| F-ADM-001 | Admin | Cycle éditorial | P1 | 2 | STRAT-001 |
| F-ADM-002 | Admin | Retrait critique | P2 | 4 | — |
| F-ADM-003 | Admin | Observabilité | P2 | 2 | — |
| F-PRI-001 | Confidentialité | Minimisation, local-first | P0 | 2 | STRAT-002 (pas de MP3 disque) |
| F-V2-001 | v2 | Corpus d’entraînement | P3 | 6 | ne pas démarrer |
| F-V2-002 | v2 | Mini-LLM borné | P3 | 6 | ne pas démarrer |
| F-V2-003 | v2 | Voice-to-voice | P3 | 7 | ne pas démarrer |

---

## Ordre technique recommandé (après validation humaine des textes)

1. `F-NAR-007` + `F-DAT-001` — IDs et SQLite, sans audio.  
2. `F-AUD-005` pilote Piper (1 ramifié + 12 atomiques) → MP3.  
3. `F-AUD-004` chiffrement + lecteur RAM.  
4. `F-PLY-005` + `F-NAR-002` jour/nuit.  
5. `F-LOC-002` paquets.  
6. Compte / profil / forêt parentale (`F-ACC`, `F-PRF`, `F-TAX-003`, `F-FOR-001`).

Pas de merge `main` tant que les textes n’ont pas été relus.
