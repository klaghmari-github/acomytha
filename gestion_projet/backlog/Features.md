# AcoMytha — backlog features

**Version :** 4.11 — 6 septembre 2026. Remplace `AcoMytha_Backlog_Features_v2.0.xlsx`. Gel : `gestion_projet/ETAT_REPRISE.md`.  
**Stripe (F-PAY-001, `3e4335b8`).** Checkout hébergé + webhook signé. Plus de paiement démo. Clés uniquement dans l’environnement. Recharge 10–50 € → acm. Abonnement 7,99 € = F-PAY-004 (pas encore).  
**Avis3** (`gestion_projet/feedback_chatgpt/avis3.txt`, commit audité `3d0793c0`) : ne pas vendre le volume. D’abord 24 histoires irréprochables + audio + vitrine/parent/enfant.  
**Chaîne (F-NAR-024).** Source = **Excel** → JSON → TTS **dans AcoMytha** (`TtsApp`, `#/admin/editeur`) → audio. Trois dossiers plats : `arbres/`, `json/`, `audio/` (+ `voices/` pour les empreintes). Branche `AkoMythaTTS`. Détail : `stories/FORMAT_JSON_TTS.md`.  
**Branche :** `main` en routine. **Exception fusion TTS :** `AkoMythaTTS`. Message `feat(F-XXX):` / `docs:`.  
**Demandes + exemples fondateur :** `decisions/ECHANGES.md` (traçabilité).  
**Spec :** `specification/AcoMytha_Specification.md`. Les colonnes *Strat* pointent le document d’architecture, pas une copie.  
**Web :** `STRAT-005`. Statut : **développé** = sur `main`.

Priorités : **P0** première écoute réelle · **P1** MVP familles · **P2** juste après · **P3** v2 (ne pas démarrer).

Phases : 0 cadrage · 1 contenu · 2 MVP web (puis native) · 3 interaction fermée · 4 renouvellement · 5 leçons parentales · 6–7 hors MVP.

### Statut (6 sept. 2026)

| ID | Statut | Note |
| --- | --- | --- |
| F-GEN-001 | **développé** | Corpus 1445 xlsx + audio témoin stéréo 44100. `main` = `837d436`. |
| F-NAR-007 | **développé** | IDs chunks dans les xlsx. |
| F-TAX-001 / F-TAX-002 | **développé** | `lecons.xlsx` + `lecon_histoires.xlsx`. |
| F-AUD-005 | partiel | Piper local, échantillons git + bake disque. |
| F-AUD-002 | **développé** | Loudness : narrateur aligné (plus audible). |
| F-ACC-002 | **reporté** | Contredit F-SEC-003 (une clé = un appareil). |
| F-APP-001 | **développé** | Socle FastAPI + PWA, POO HTML/CSS/JS. |
| F-DAT-001 | **développé** | SQLite. Live xlsx **837** (685 ATOM + 152 TREE). Import **incomplet** pour la voix → F-DAT-002. Corpus 1449. |
| F-ACC-001 | **développé** | Login parent/admin, PIN enfant. |
| F-SEC-003 | **développé** | 1 appareil / clé, alerte admin, reset. |
| F-SEC-002 | **développé** | Mode enfant sans catalogue. |
| F-ADM-004 | **développé** | Console stats, alertes, comptes. |
| F-PAR-001 | **développé** | Liste, filtres, sélection enfant. |
| F-ENF-001 | **développé** | File parentale + lecteur. |
| F-AUD-004 | **développé** | AES-GCM `.chk`, déchiffre RAM, prefetch N+1. |
| F-PLY-001 | **développé** | Lecteur graphe jour/nuit, délai 3 s. |
| F-AUD-006 | **développé** | Scripts 1445 xlsx ; échantillons re-bakés ; bake corpus lancé. |
| F-AUD-003 | **remplacé** | « Une voix / histoire » annulé par F-AUD-006. |
| F-AUD-007 | **à faire** | Immersion **générale** : tout événement du récit a son bruit (toutes les histoires). |
| F-NAR-008 | **en cours** | Fil rouge narratif : l’histoire captive, la leçon se greffe. Texte d’abord. |
| F-NAR-009 | **en cours** | Ouverture non brutale, monde descriptif, créativité d’amorce (exemples non limitatifs). |
| F-NAR-010 | **en cours** | Règle posée. Appliqué AUT-001, COL-001, 2 ATOM. Pas tout le catalogue. |
| F-NAR-011 | **en cours** | Idem. Fins vécues sur l’étalon ; beaucoup d’ATOM encore en récap. |
| F-NAR-012 | **en cours** | Idem. Bravo/bon travail encore trop fréquent hors étalon. |
| F-NAR-013 | **en cours** | Chaîne question corrigée sur les histoires reprises. |
| F-NAR-014 | **en cours** | AUT-001 / COL-001 : choix à conséquences. COL-007–035 et archive : pas encore. |
| F-NAR-015 | **en cours** | `RELECTURE.md` sur les arbres repris. Pas une validation globale. |
| F-NAR-016 | **en cours** | Pilote ramifié fait. **D38** = on continue d’écrire tout le corpus. **Vente** = F-NAR-020 (24 d’abord). |
| F-NAR-017 | **développé** | Veille `feedback_chatgpt/` : nouveau fichier → consignes → histoires gardées (texte). |
| F-NAR-018 | **en cours** | Étalon structurel (avis2) : oral fluide, pas de morale dite, ramification = 9 aventures, ATOM sans récap. |
| F-NAR-019 | **en cours** | Audit vocal example2 : récit humain, 27 chemins vraiment distincts, métadonnées TTS (arc/émotion/tempo). |
| F-NAR-020 | **à faire** | Collection fondatrice **24** (8 N1 + 8 N2 + 8 N3), audio + relecture humaine. Pas vendre 1449. |
| F-NAR-021 | **à faire** | Contrôle tics corpus + titres uniques (avis3). |
| F-NAR-022 | **à faire** | `text` change → invalider SSML / xai / notes / audio. |
| F-NAR-023 | **à faire** | Trois séries personnages (Amir / Nina / Victorina). |
| F-NAR-024 | **en cours** (branche `AkoMythaTTS`) | Chaîne Excel → JSON → audio **dans** l’app. Éditeur admin. Profil ≠ prosodie. |
| F-DAT-002 | **à faire** | Importer métadonnées vocales dans SQLite et le lecteur. |
| F-AUD-008 | **à faire** | Produire l’audio des 24 (puis étendre). Témoins Git = 2 histoires. |
| F-APP-009 | **à faire** | Vitrine conversion : hero + extrait, 6 phares, besoins parent, pas « 1400 leçons ». |
| F-PAR-006 | **à faire** | Espace parent familial (ce soir / enfant / histoires). Retirer voix et commande non finies. |
| F-ENF-002 | **à faire** | Mode enfant illustré : cartes, continuer, pictos, fin vécue. |
| F-PLY-006 | **à faire** | Mode nuit choisi par le parent, pas par l’enfant. |
| F-PAY-004 | **à faire** | Offre euros simple (abo + pack). acm hors premier écran. |
| F-PAY-005 | **plus tard** | Parrainage : acm au parrain = 1er chargement ; le parrain du parrain reçoit 2× sa 1re charge. |
| F-SEC-004 | **à faire** | Durcir la prod : plus de démo en public, recovery, rate limit. |
| F-ADM-005 | **à faire** | Pages légales + dépôt reproductible (deps, CI, Docker). |
| F-UX-001 | **à faire** | Raffinement visuel et UX cohérent des espaces vitrine, parent, enfant audio et éditeur, sans rupture avec l’identité actuelle. |
| F-ACC-005 | **à faire** | Un compte peut cumuler les rôles parent, éditeur et admin ; menus et API suivent les permissions effectives. |
| F-ADM-006 | **à faire** | L’admin affecte ou retire le rôle éditeur aux comptes parents et configure les limites produit. |
| F-PRF-003 | **à faire** | Jusqu’à 10 profils enfants isolés par foyer, plafond configurable par l’admin. Aucun compte enfant. |
| F-PAR-007 | **à faire** | Catalogues distincts par enfant ; affectation d’une histoire à un, plusieurs ou tous les profils. |
| F-ENF-003 | **à faire** | Activation après choix du profil et création d’un code 4 chiffres ; sortie protégée, reconnexion parent comme récupération. |
| F-ENF-004 | **à faire** | Mode enfant sans interface ni boutons : écran verrouillé, conduite entièrement orale, écoute et réponses vocales. |
| F-APP-010 | **à faire** | Catalogue public par histoire, personnage, leçon, lieu et univers bleu/rose ; filtres cumulatifs et réversibles. |
| F-HIS-003 | **à faire** | Journal exhaustif par profil : chaque session, dates/heures, durée, progression, complétion et réécoutes. |
| F-NAR-025 | **à faire** | Recommandation enfant : histoires jamais écoutées d’abord, puis reprise et diversité selon l’historique du profil. |
| F-NAR-002 | **développé** | Enchaînement de tous les passages (atomique et ramifié). |
| F-ACC-003 | **développé** | Inscription e-mail + mot de passe (pas de prénom). Libellé « E-mail ». |
| F-ACC-004 | **développé** | Parent change le PIN 4 chiffres. Même code parent ↔ enfant. |
| F-APP-002 | **développé** | Vitrine publique, catalogue, pop-ups ramifications. Écoute invité : F-APP-006. |
| F-PAY-001 | **développé** | Stripe Checkout + webhook signé. Sans clés : recharge désactivée. Plus de démo. |
| F-PAR-003 | **développé** | Parent non acheté 30 s, acheté / enfant = entier. Visiteur vitrine : F-APP-006. |
| F-PAY-002 | **développé** | Monnaie interne, solde, achats, commandes, voix. Paramètres admin. |
| F-PAY-003 | **développé** | Symbole **acm** (même dessin que le logo), montants partout où l’on obtient un produit ou un service. |
| F-APP-003 | **développé** | Accueil : catalogue par lots (défaut 6), chargement au scroll. Paramètre admin. |
| F-APP-004 | **développé** | Accueil : *Apprendre par l’histoire.* / *AcoMytha : univers d’histoires ludiques et captivantes.* |
| F-APP-005 | **développé** | Vitrine 2026 : chambre d’écoute, typo éditoriale, catalogue dans la scène. |
| F-APP-006 | **développé** | Vitrine : Écouter toutes les histoires, 30 s, puis pop-up compte. Pas de prix acm. |
| F-APP-007 | **développé** | Même identité visuelle (chambre d’écoute) : connexion, inscription, parent, admin, enfant. |
| F-APP-008 | **développé** | POO : champs privés, propriétés, une classe = un rôle (Python, JS, CSS, HTML). |
| F-PLY-002 | **développé** | Bouton Arrêt visible + durée affichée (minutes). |
| F-PAR-002 | **développé** | Libellés : Avec interaction / Avec ramifications vers d’autres histoires. |

---

## Application web (v3.1 — après les textes)

Feature complexe `F-APP-001` : stories (commits) sur `main`. Détail : **STRAT-005**.

| ID | Epic | Titre | Prio | Phase | Strat | Dépendances |
| --- | --- | --- | --- | --- | --- | --- |
| F-APP-001 | App | Socle web PWA, POO HTML/CSS/JS, FastAPI, 3 shells | P0 | 2 | STRAT-005 | F-GEN-001 |
| F-DAT-001 | Référentiel | SQLite histoire ↔ leçon ↔ chunk (import xlsx) | P0 | 2 | STRAT-003 | F-NAR-007, F-APP-001 |
| F-ACC-001 | Compte | Création / connexion parent + admin | P0 | 2 | STRAT-005 | F-APP-001 |
| F-SEC-003 | Sécurité | Une clé d’accès = un appareil, alerte admin sinon | P0 | 2 | STRAT-005 | F-ACC-001 |
| F-SEC-002 | Sécurité | Cloisonnement mode enfant (PIN, pas de catalogue) | P0 | 2 | STRAT-005 | F-ACC-001 |
| F-ADM-004 | Admin | Console : comptes, alertes appareil, reset liaison | P0 | 2 | STRAT-005 | F-SEC-003 |
| F-PAR-001 | Parent | Liste, filtres, sélection des histoires enfant | P0 | 2 | STRAT-005 | F-DAT-001 |
| F-ENF-001 | Enfant | Déroule uniquement la forêt parentale | P0 | 2 | STRAT-005 | F-SEC-002, F-PAR-001 |
| F-AUD-004 | Audio | AES-GCM, déchiffre en RAM, prefetch N+1 | P0 | 2 | STRAT-002 | F-DAT-001, F-SEC-003 |
| F-PLY-001 | Lecture | Lecteur écran pauvre, graphe jour/nuit, délai 3 s | P0 | 2 | STRAT-004 | F-AUD-004, F-ENF-001 |
| F-APP-002 | App | Vitrine publique, aperçu, pop-ups ramifications | P0 | 2 | STRAT-005 | F-DAT-001 |
| F-APP-003 | App | Accueil : lots + scroll infini (taille admin) | P1 | 2 | STRAT-005 | F-APP-002 |
| F-APP-004 | App | Accueil : titre et sous-titre | P1 | 2 | STRAT-005 | F-APP-002 |
| F-APP-005 | App | Vitrine : design chambre d’écoute 2026 | P1 | 2 | STRAT-005 | F-APP-004 |
| F-APP-006 | App | Vitrine : 30 s d’écoute + pop-up compte ; pas de prix | P0 | 2 | STRAT-005 | F-APP-002, F-PAR-003 |
| F-APP-007 | App | Identité chambre d’écoute hors vitrine (gates, parent, admin, enfant) | P0 | 2 | STRAT-005 | F-APP-005 |
| F-APP-008 | App | Encapsulation POO (privé, propriétés, responsabilités) | P0 | 2 | STRAT-005 | F-APP-001 |
| F-ACC-003 | Compte | Inscription e-mail + mot de passe | P0 | 2 | STRAT-005 | F-ACC-001 |
| F-ACC-004 | Compte | PIN 4 chiffres, parent ↔ enfant | P0 | 2 | STRAT-005 | F-SEC-002 |
| F-PAY-001 | Boutique | Stripe Checkout : recharge 10–50 € → acm, webhook signé, pas de démo | P0 | 2 | STRAT-005 §7 | F-PAY-002 |
| F-PAY-002 | Boutique | Monnaie interne, solde, achats | P1 | 2 | STRAT-005 | F-ACC-003 |
| F-PAY-003 | Marque | Symbole acm + logo (un seul dessin) | P1 | 2 | STRAT-005 | F-PAY-002 |
| F-PLY-002 | Lecture | Arrêt visible + durée sur les cartes | P0 | 2 | STRAT-004 | F-PLY-001 |
| F-PAR-002 | Parent | Libellés interaction / ramifications | P0 | 2 | STRAT-005 | F-PAR-001 |
| F-UX-001 | UX | Élever le design actuel des quatre expériences sans refonte de marque | P0 | 2 | STRAT-005 | F-APP-007 |
| F-ACC-005 | Compte | Rôles cumulables parent / éditeur / admin et autorisations dédiées | P0 | 2 | STRAT-005 | F-ACC-001 |
| F-ADM-006 | Admin | Gestion des rôles et paramètres de limites fonctionnelles | P0 | 2 | STRAT-005 | F-ACC-005 |
| F-PRF-003 | Profils | Profils enfants multiples, isolés, sans compte enfant | P0 | 2 | STRAT-003/005 | F-ACC-001 |
| F-PAR-007 | Parent | Catalogue acheté et sélection propre à chaque profil enfant | P0 | 2 | STRAT-005 | F-PRF-003, F-PAR-001 |
| F-ENF-003 | Enfant | Choix du profil, code de verrouillage 4 chiffres et récupération parent | P0 | 2 | STRAT-005 | F-PRF-003, F-SEC-002 |
| F-ENF-004 | Enfant | Expérience écran verrouillé et interaction exclusivement orale | P0 | 2 | STRAT-004/005 | F-ENF-003, F-INT-002 |
| F-APP-010 | App | Vues catalogue et filtres multi-facettes combinables | P0 | 2 | STRAT-005 | F-APP-002, F-DAT-001 |
| F-HIS-003 | Suivi | Sessions d’écoute détaillées par profil enfant | P0 | 2 | STRAT-003/004 | F-PRF-003, F-NAR-004 |
| F-NAR-025 | Moteur | Priorisation des histoires inédites et reprises pertinentes | P1 | 2 | STRAT-004 | F-HIS-003 |

### F-APP-001 — Socle

`app/` : FastAPI factory, fichiers statiques, custom elements, jetons CSS, hash-router. Comptes démo locaux. Responsive téléphone / tablette / bureau. Encapsulation : F-APP-008.

### F-APP-008 — Encapsulation POO

Une classe = un rôle. État **privé**. Accès public par **propriétés** (invariants, pas un getter vide par champ). Python : `ShopParams`, `WalletBook`, `PreviewStudio`, `Settings`, coffre, graphe, session. JS : champs `#`, `Component` injecte api/router, `Session`, `StoryEngine`, `CryptoPlayer`. CSS : `tokens` / `objects` / `components` / `shells`. HTML = custom elements. D37. Les routeurs FastAPI restent des routeurs (c’est le cadre).

### F-SEC-003 — Un appareil

`device_id` persisté sur le client. Premier login lie. Deuxième empreinte → HTTP 409 + `DeviceAlert`. L’admin peut reset. L’enfant n’ouvre pas une 2ᵉ liaison.

### F-ENF-001 — Enfant

Pas de filtres, pas de compte, pas d’admin. File = histoires cochées par le parent. Grandes cibles, mode jour/nuit.

### Vision UX et comptes — décision fondateur du 6 septembre 2026

Ces fonctionnalités font évoluer l’expérience existante sans remplacer son identité visuelle. Le design améliore la hiérarchie, la fluidité, la lisibilité, les états de chargement et de confirmation, l’accessibilité et la cohérence entre les espaces.

#### F-UX-001 — Quatre expériences cohérentes

- **Vitrine publique** : découvrir le produit et le catalogue, écouter un aperçu, créer un compte parent ou se connecter.
- **Espace parent** : acheter et sélectionner des histoires, gérer les profils enfants, consulter leur activité et activer le mode enfant.
- **Mode enfant** : expérience d’écoute audio, sans compte autonome et sans interface graphique exploitable.
- **Éditeur** : atelier de création et d’édition des histoires, textes, voix, prosodie et audio, visible uniquement avec le rôle éditeur.

Le style « chambre d’écoute » actuel reste la base. Chaque espace possède une hiérarchie et des commandes adaptées tout en partageant les composants et jetons de marque.

#### F-ACC-005 / F-ADM-006 — Rôles cumulables

Le compte de base est un **compte parent**. Un même compte peut cumuler :

| Rôle | Accès |
| --- | --- |
| parent | achats, portefeuille, profils enfants, catalogues, historique et mode enfant |
| editor | accès supplémentaire à l’éditeur graphique et aux API éditoriales |
| admin | gestion des comptes, attribution/retrait du rôle éditeur et paramètres globaux |

Il n’existe **aucun compte enfant**. Un profil enfant est une donnée interne au foyer parent. L’interface et les API appliquent les permissions côté serveur ; masquer un bouton ne suffit pas. Un admin peut attribuer ou retirer le rôle éditeur à un compte parent.

#### F-PRF-003 / F-PAR-007 — Profils et catalogues enfants

- Un parent crée plusieurs profils enfants, jusqu’au paramètre max_child_profiles (défaut **10**, configurable dans l’admin).
- Chaque profil possède son identité d’usage, ses préférences, son catalogue sélectionné et son historique, sans identifiants de connexion.
- Une histoire achetée appartient au foyer. Depuis toute carte ou fiche, **Ajouter à un catalogue enfant** permet de choisir un profil, plusieurs profils ou tous.
- Retirer une histoire d’un catalogue enfant ne supprime ni l’achat familial ni l’historique.
- Avant le mode enfant, le parent choisit le profil. L’enfant n’écoute que les histoires que le parent lui a affectées.
- Les recommandations ne présument pas des goûts selon le sexe du profil : le parent conserve le contrôle.

#### F-ENF-003 — Verrouillage parental du mode enfant

1. Le parent choisit le profil enfant.
2. Il active le mode enfant.
3. L’application demande de créer/saisir un code de **4 chiffres** et rappelle qu’il sera nécessaire pour quitter le mode.
4. L’application ouvre une session enfant cloisonnée.

La sortie volontaire demande le code. Après des échecs répétés, un délai progressif limite les essais. En cas d’oubli, le parent ferme la session puis se reconnecte avec ses propres identifiants ; cette reconnexion réinitialise la session enfant. Le code ne remplace jamais le mot de passe et doit être stocké sous forme dérivée sécurisée, jamais en clair.

#### F-ENF-004 — Audio uniquement

En mode enfant, l’écran ne propose ni catalogue visuel, ni carte, ni bouton de navigation, ni réglage, ni information du compte. Il affiche seulement un état visuel neutre et verrouillé indispensable au système et à l’accessibilité.

Toute l’expérience utile passe par la voix :

- l’application annonce les histoires disponibles et propose d’abord les inédites ;
- l’enfant choisit oralement une histoire ;
- le moteur raconte, pose les questions et énonce les options de branchement ;
- la reconnaissance vocale interprète une réponse dans un vocabulaire fermé, confirme oralement et poursuit ;
- en cas de silence ou d’incompréhension, le moteur répète une fois puis applique le choix par défaut sûr ;
- aucune génération ne se produit pendant la lecture.

Le verrouillage applicatif ne peut pas empêcher seul les gestes système du téléphone. La sécurité visée est le cloisonnement : si l’enfant ferme l’application, il ne possède pas les identifiants pour revenir dans l’espace parent.

#### F-APP-010 — Catalogue multi-vues et filtres combinables

La vitrine permet d’explorer le même catalogue par histoires, personnages, leçons, lieux (maison, école, parc…) et deux univers éditoriaux :

- **bleu** : héros garçon et thèmes associés (train, ascenseur, football, etc.) ;
- **rose** : héroïne fille et thèmes associés (poupée, princesse, robe, chaussures, cheveux, boucles d’oreilles, etc.).

Ces univers sont des vues de découverte, jamais des restrictions de profil. Ils utilisent des métadonnées explicites et révisables, pas une déduction automatique depuis le prénom.

- Un clic active une facette ; un second clic la désactive.
- Les groupes se cumulent par intersection, par exemple bleu + maison.
- Les filtres actifs sont visibles, supprimables séparément et réinitialisables en une action.
- Le total et le chargement progressif reflètent immédiatement la combinaison.
- L’URL conserve les filtres afin de restaurer ou partager la vue.
- Clavier, lecteur d’écran et mobile donnent le même résultat fonctionnel.

#### F-HIS-003 / F-NAR-025 — Historique et ordre de proposition

Chaque tentative crée une session immuable liée au profil et à l’histoire :

- date/heure de début et de fin ;
- durée réellement écoutée et durée totale de la version ;
- progression en pourcentage ;
- chunks et chemin suivis pour une histoire ramifiée ;
- fin atteinte ou interruption ;
- mode jour/nuit et version de l’histoire.

Les agrégats calculent démarrages, écoutes complètes, réécoutes, dernière écoute et meilleure progression. Une progression de 80 % reste partielle ; la complétion exige la fin ou un seuil configurable.

Ordre oral par défaut :

1. histoires affectées jamais commencées ;
2. histoires commencées à reprendre ;
3. histoires terminées, diversifiées selon ancienneté et préférences ;
4. pas de répétition fondée uniquement sur une étiquette bleu/rose.

Le parent dispose d’une synthèse claire par enfant, sans transformer l’écoute en surveillance intrusive.

---

## Nouveautés v3 (à faire en premier après les textes)

| ID | Epic | Titre | Prio | Phase | Strat | Dépendances |
| --- | --- | --- | --- | --- | --- | --- |
| F-NAR-007 | Moteur | Identifiants chunks path-encodés + compilateur JSON→chunks | P0 | 0 | STRAT-003 | F-NAR-001 |
| F-DAT-001 | Référentiel | SQLite histoire ↔ leçon ↔ chunk, dossier `chunks/` plat | P0 | 0 | STRAT-003 | F-NAR-007, F-TAX-002 |
| F-AUD-004 | Audio | Chiffrement AES-GCM, lecture RAM, prefetch N+1 | P0 | 2 | STRAT-002 | F-AUD-001, F-SEC-001 |
| F-AUD-005 | Audio | Bake Piper → MP3 64k, 0 €, plans via Heavy | P0 | 1 | STRAT-002 | F-AUD-001, F-GEN-001 |
| F-AUD-006 | Audio | Cast multi-voix (narrateur / famille / école / enfants) | P0 | 1 | STRAT-002 §4 | F-AUD-005 |
| F-AUD-007 | Audio | Immersion sonore de **tout** le récit (monde entendu, pas une liste de cas) | P0 | 1 | STRAT-002 §4b | F-AUD-006 |
| F-NAR-008 | Moteur | Fil rouge, ≥ 3 min, plusieurs passages/leçons, troupe fermée, adultes parlent | P0 | 1 | stories/REWRITE.md | F-GEN-001, F-AUD-006, F-AUD-007 |
| F-NAR-009 | Moteur | Ouverture du monde, détails, chaque histoire racontée autrement | P0 | 1 | stories/REWRITE.md | F-NAR-008 |
| F-NAR-010 | Moteur | Désir ≠ leçon ; réécoute sans questions | P0 | 1 | stories/REWRITE.md | F-NAR-008 |
| F-NAR-011 | Moteur | Progression causes/conséquences ; fin du projet promis | P0 | 1 | stories/REWRITE.md | F-NAR-010 |
| F-NAR-012 | Moteur | Décrire dans l’action ; amusement lié ; héros agit | P0 | 1 | stories/REWRITE.md | F-NAR-010 |
| F-NAR-013 | Moteur | Chaîne question complète ; préférence ≠ connaissance | P0 | 1 | stories/REWRITE.md | F-NAR-008 |
| F-NAR-014 | Moteur | Conséquences des choix ; chemin cohérent ; pas de gabarit | P0 | 1 | stories/REWRITE.md | F-NAR-010 |
| F-NAR-015 | Production | Preuves de relecture, pas d’auto-validation IA | P0 | 1 | STRAT-001 | F-VAL-001 |
| F-NAR-016 | Production | Pilote 2 ramifiés, 1 actif, archive des autres | P0 | 1 | stories/PRIORITE.md | F-NAR-010 |
| F-NAR-017 | Production | Veille dossier ChatGPT → consignes → TREE-AUT-001 / TREE-COL-001 | P0 | 1 | stories/PRIORITE.md | F-NAR-016 |
| F-NAR-018 | Moteur | Étalon AUT-001 : logique reprise, pas les phrases ; oral fluide ; morale vécue | P0 | 1 | stories/REWRITE.md | F-NAR-014 |
| F-NAR-019 | Moteur | Récit humain + métadonnées TTS ; 27 chemins distincts (audit example2) | P0 | 1 | stories/REWRITE.md | F-NAR-018 |
| F-NAR-020 | Production | Collection fondatrice 24 (8×N1/N2/N3, 6 besoins, 12 ATOM + 12 TREE) | P0 | 1 | avis3 §13 | F-NAR-019 |
| F-NAR-021 | Production | Anti-tics + titres uniques | P0 | 1 | avis3 §2 | F-VAL-001 |
| F-NAR-022 | Production | Invalidation vocale si `text` change | P0 | 1 | avis3 §3 | F-AUD-006 |
| F-NAR-023 | Éditorial | Séries Amir / Nina / Victorina | P1 | 1 | avis3 §13 ph.2 | F-NAR-020 |
| F-NAR-024 | Production | Excel source → JSON → TTS → audio ; 3 dossiers plats ; profil ≠ prosodie | P0 | 1 | stories/FORMAT_JSON_TTS.md | F-NAR-019 |
| F-DAT-002 | Référentiel | Import SSML, xai, notes, sons, voix dans SQLite | P0 | 2 | avis3 §3 | F-DAT-001 |
| F-AUD-008 | Audio | Bake + contrôle des 24, puis extension | P0 | 1 | avis3 §4 | F-AUD-005, F-NAR-020 |
| F-APP-009 | App | Vitrine : hero, extrait, 6 phares, collections besoins | P0 | 2 | avis3 §6–8 | F-APP-006 |
| F-PAR-006 | Parent | Accueil familial ; masquer boutique inachevée | P0 | 2 | avis3 §9 | F-PAR-001 |
| F-ENF-002 | Enfant | Cartes illustrées, continuer, pictos, fin émotionnelle | P0 | 2 | avis3 §10 | F-ENF-001 |
| F-PLY-006 | Lecture | Nuit réglée par le parent | P0 | 2 | avis3 §10 | F-PLY-003 |
| F-PAY-004 | Boutique | 7,99 €/mois + pack 9,90 € ; acm en second | P0 | 2 | avis3 §11 | F-PAY-001 |
| F-PAY-005 | Boutique | Parrainage acm (1er chargement / double 1re charge) | P2 | 2 | ECHANGES §14 | F-PAY-002 |
| F-SEC-004 | Sécurité | Plus de comptes démo publics ; recovery ; rate limit | P0 | 2 | avis3 §12 | F-SEC-003 |
| F-ADM-005 | Admin | CGU, confidentialité, deps verrouillées, CI, Docker | P0 | 2 | avis3 §12 | F-APP-001 |
| F-PLY-005 | Lecture | Délai 3 s, une relance, choix auto ; nuit saute questions et branchements | P0 | 2 | STRAT-004 | F-PLY-002, F-PLY-003 |
| F-INT-005 | Interactions | `passage_question` : attente, similarité future, phrases moteur « oui / presque » | P0 | 2 | STRAT-004 | F-INT-001, F-PLY-005 |

### F-NAR-007 — Identifiants chunks

Racine `CHK_T0000_P0000`. Branchement `CHK_T0001_P0000`, options `…_O000k`, suites `…_P000k`. Trois niveaux max par concatenation `_T000n`. Pas de `…_Txxxx_P0000` fils = fin. Compilateur depuis `stories/*.json`. Détail : **STRAT-003**.

### F-DAT-001 — Catalogue relationnel

Tables `lesson`, `story`, `story_lesson`, `chunk`, `chunk_link` (exceptions). Le parent coche des `lesson_id` → téléchargement de **histoires entières**. Duplication des passages entre histoires : voulue. Un dossier `chunks/`. **STRAT-003**.

### F-AUD-004 — Protection

`.chk` = AES-256-GCM(MP3). Clé au Keystore/Keychain. Jamais de MP3 en clair sur disque. Décryptage chunk par chunk en RAM. **STRAT-002** §5.

### F-NAR-008 — Récit captivant (fil rouge)

**Problème :** les textes actuels sont des **scénarios de leçon branchés**, pas des histoires. Pas de début/fin vécus. Impression de **cours**, pas d’écoute.

**Cible :** un fil rouge (envie, petite aventure, fait concret) **dirige** le récit. Les leçons se **greffent**. L’enfant sent que quelque chose **commence** et **se termine**.

Processus : agents en parallèle → fichiers `stories/rewrites/<id>/agent_*.json` (xlsx d’origine intact) → **fusion éditoriale** (pas le texte le plus long) → remplacement. Texte d’abord, chunks + `script` + `sons` + rythme. Détail : `stories/REWRITE.md`.

Passe 2 (3 atomiques alimentation) : compréhensible 3–6 ans, un fil par histoire, un moment par chunk, leçon **vécue** en fin.

**Troupe enfant (D16) :** Amir, Aniss, Sarah, Chouchou, Mila, Nino, Nina, Raphaël, Victorino, Victorina. Les réécritures suivantes remplacent Lina / Noé / Tom par cette liste. Peu de personnages par histoire.

**Durée (D17) :** ≥ 3 min. Plusieurs passages ; certains portent une leçon. Atomique : plusieurs leçons possibles pour tenir 3 min. Allonger si le récit le demande.

**Adultes parlent (D20) :** papa et maman ont des répliques (félicitations, questions, discussion) adaptées à la scène. Interdit : « papa sourit », « maman est là » à la place de leur voix. Bêtise : discuter / demander la conduite, POS-001.

- `ATOM-SAN.ALI.001-01` Sarah — *Le petit soleil dans l'assiette* (N1)
- `ATOM-SAN.ALI.001-02` Amir — *La carotte qui s'échappe* (N2)
- `ATOM-SAN.ALI.002-01` Nino — *Le bateau de Nino* (N1)

### F-NAR-009 — Ouverture du monde (pas d’entrée brutale)

**Problème :** beaucoup d’histoires commencent comme un constat. L’enfant est jeté dans l’action : « Constantin joue au salon. » C’est **brutal**. Pas de village, pas de famille, pas de temps, pas de détails. On dirait une consigne, pas un conte.

**Cible :** chaque histoire **installe un monde** avant l’action. L’enfant voit où on est, avec qui, quel temps il fait, ce que ça sent, ce qu’on entend. Ensuite seulement : « en ce moment… » Les enfants **adorent les détails**. Le récit reste captivant tout du long, pas seulement au début.

**Créativité obligatoire.** Chaque histoire a sa manière. On ne recopie pas une amorce. On n’enchaîne pas deux histoires qui commencent pareil.

Les textes ci-dessous sont des **exemples de manières**, pas des modèles à coller, pas une liste fermée. Il **faut inventer** d’autres ouvertures. Traçabilité : `decisions/ECHANGES.md` §7 (citation intégrale).

Les prénoms Constantin / Luca / Céline sont **dans l’exemple fondateur**. Le corpus, lui, utilise la troupe D16 et **papa / maman**.

*Manière conte (exemple fondateur, à ne pas recopier) :*

> il etait une fois, dans un petit village, une petite famille heureuse, un enfant constentin, un papa luca, et une maman celine. un jour pluvieux constentin n'a paas pu sortir au paroc il est resté à la maison. en ce moment même, constentin joue au salon.

*Manière présentation (exemple fondateur, à ne pas recopier) :*

> ceci est l'histoire d'un enfant heureux qui s'appelait constentin, il vivait avec son papa lucas et sa maman celine dans une belle maison. la maison se trouvait dans un village très lointin. en ce moment dans ce village il pleut. constentin ne peut pas sortir au parc. il est au salon entrain de jouer avec des legos, ....

*D’autres manières (toujours des exemples) :* une gouttière qui chante, une odeur de soupe qui monte l’escalier, un rayon sur le tapis, des chaussures qui sèchent près de la porte, le doudou qui attend dans le canapé, la fenêtre embuée, le marché qu’on entend d’en bas… **Inventer.**

Contraintes inchangées : troupe D16, papa/maman (pas un prénom d’adulte à la place), POS-001, adultes qui parlent (D20), ≥ 3 min, phrases courtes. Audio **après** les textes.

Processus : mêmes agents / `stories/REWRITE.md`. Passe sur **tout** le corpus (atomiques + ramifiées). Colonne `script` à jour. Pas de bake audio dans cette passe.

Source consignes : `gestion_projet/feedback_chatgpt/f_04.txt`. Exemple : `exemple.txt` (Chouchou, *La boîte trop haute*).

### F-NAR-010 — Désir du héros, pas la leçon

L’histoire doit donner envie d’être **réécoutée même si l’on retire les questions**.

Séparer le **désir du héros** de l’**objectif pédagogique**. Chouchou veut construire son bateau, pas « apprendre à demander de l’aide ». L’apprentissage devient utile lorsque quelque chose **l’empêche d’avancer**.

### F-NAR-011 — Progression et vraie fin

Construire une progression avec des causes et des conséquences : une envie, un obstacle, une tentative, un résultat, un ajustement, une résolution. **Naturelle** : ce n’est pas une formule à réciter dans chaque histoire.

Donner une **vraie fin** au projet commencé. Obtenir la boîte ne suffit pas si le récit promettait un puzzle. Laisser découvrir ce que le héros en fait, puis terminer sur un geste, une réplique ou une surprise.

### F-NAR-012 — Écrire pendant que ça se passe

Décrire **pendant** que les choses se passent : bruit des pièces dans la boîte, un coin de tapis qui se replie, une manche mouillée. Une succession de lumières, d’odeurs et de textures **sans rapport** avec l’action alourdit.

Créer un **amusement lié à la situation** : découverte inattendue, petit décalage, jeu sonore, un adulte qui cache involontairement la pièce. Aucun gag sur l’humiliation, une difficulté ou un danger.

Laisser le **héros agir** : il remarque, essaie, demande, choisit, ajuste. L’adulte accompagne ; il ne résout pas chaque problème à sa place.

Supprimer les **leçons récitées** et les **félicitations automatiques**. « J’ai dit le besoin » ou « Bravo, tu as fait du bon travail » répété ne remplace pas un dialogue vivant. La conséquence concrète peut suffire.

**Ne jamais ajouter une leçon pour remplir une durée.** Enrichir par une tentative, une exploration ou une relation. Si rien ne mérite d’être développé, l’idée narrative est trop mince.

### F-NAR-013 — Chaîne de la question

Écrire chaque question **avec toute sa chaîne** : contexte, question, réponse principale, variantes admises, relance, continuation. Modifier la question sans ces champs est une source d’erreurs déjà observée.

Distinguer une **préférence** d’une **connaissance**. Choisir le jardin ou la chambre n’appelle pas un verdict de justesse. Une question factuelle exige une réponse compatible avec ce qui a **réellement** été raconté.

### F-NAR-014 — Chemins, changements, pas de gabarit

Donner des **conséquences** aux ramifications. Changer uniquement le lieu ou le goûter ne crée pas une aventure différente. Un choix peut modifier une action, une information, une collaboration ou le résultat.

Relire **chaque chemin** comme une histoire continue. Personnages, objets, quantités, informations : cohérents. Des passages corrects séparément peuvent produire une histoire incohérente une fois assemblés.

Corriger **toutes les dépendances** d’un changement. Un nouveau prénom ou objet se répercute dans dialogues, questions, relances, métadonnées et audio concernés.

Empêcher l’apparition d’un **nouveau gabarit** répétitif. Même une bonne trouvaille (objet perdu, surprise finale, rappel du début) devient pauvre si elle est reproduite partout. Varier envies, obstacles, rythmes, humour, résolutions.

### F-NAR-015 — Preuves de contrôle

L’IA indique les passages **réellement relus**, les vérifications faites, et ce qui **reste non vérifié**. Une auto-évaluation enthousiaste ne vaut pas validation. (VAL-001 : le générateur ne s’auto-approuve pas.)

### F-NAR-016 — Pilote ramifié

Avant d’appliquer F-NAR-010…015 à **tous** les ramifiés : deux arbres, à fond. Puis le reste.

| ID | Rôle |
| --- | --- |
| `TREE-AUT-001` | Premier ramifié actif |
| `TREE-COL-001` | Second chantier, maintenant aussi dans `stories/arbres/` |

Corpus : **1449** histoires (**685** atomiques, **764** ramifiées), **toutes avec question**. **85** leçons, **13** thèmes. Live `arbres/` : 764 (685 ATOM + 79 TREE). Archive : 685 TREE. Détail : `stories/CHIFFRES.md`. D31 (un seul ramifié live) est dépassé : les ramifiés repris y rentrent au fur et à mesure.

Passe **texte** faite sur les deux (F-NAR-010…015, sans audio). Preuves dans `stories/rewrites/TREE-AUT-001/RELECTURE.md` et `stories/rewrites/TREE-COL-001/RELECTURE.md`.

### F-NAR-017 — Veille feedback ChatGPT

Dès qu’un fichier **nouveau** (ou changé) arrive dans `gestion_projet/feedback_chatgpt/` : le lire, en tirer des consignes éditoriales, les appliquer aux histoires **gardées** (TREE-AUT-001, TREE-COL-001), texte d’abord, pas d’audio.

- Outil : `python3 stories/outils/watch_feedback_chatgpt.py` (`scan` / `claim` / `done` / `watch`).
- Ledger : `gestion_projet/feedback_chatgpt/processed.json` (les audits déjà lus y sont).
- Skill : `.grok/skills/ingest-feedback-chatgpt/SKILL.md`. Workflow : `.grok/workflows/ingest-feedback-chatgpt.rhai`.

### F-NAR-018 — Étalon structurel (avis2)

`avis2.txt` : le bateau d’Amir est la première base commercialisable. On en reprend la **logique**, pas le verbe.

| Oui | Non |
| --- | --- |
| Désir → obstacle → tentative → conséquence → retour | Recopier capitaine / plic-ploc / volet jaune |
| Phrases courtes **et** un peu liées, à l’oral | Télégraphe : « Celle-ci, la coque. » « Le manteau, Amir. » |
| La morale se voit (Amir part sur l’autre flaque) | « Changer de chemin, ce n’est pas perdre. » |
| T1 change le voyage (bottes qui claquent, linge qui sèche) | 27 fins vendues alors que T1 ne change que 2 phrases |
| ATOM : un imprévu **après** le désir, joie/aide **une** fois | Décor → leçon → question → « J’ai dit le besoin. Bravo. » |
| Fin = un détail à raconter (brindille sur la voile, pomme sauvée) | « L’histoire est finie. » |

D38 inchangé : on ne réduit pas le catalogue à 20 titres. On hausse la barre partout.
- Commerce, Stripe, ASR, bake audio : `NOTES.md` « Pas maintenant », pas une réécriture.
- `NOTES.md` n’est pas un fichier ChatGPT.

D32.

### F-NAR-019 — Récit humain + voix (example2)

Source : `gestion_projet/feedback_chatgpt/examples/example2/` (audit vocal 5 sept., étalon `TREE-COL-015`).

| Oui | Non |
| --- | --- |
| Style oral d’humain : rythme variable, vocabulaire simple et **divers** | Gabarit IA, tics « tout doux / encore / déjà », mêmes phrases d’un titre à l’autre |
| Arc **sur chaque chemin** : monde, désir, imprévu, 1re tentative ratée, péripéties, climax, dénouement | Décor + consigne + validation ; même aventure avec 3 goûters |
| T1/T2/T3 changent **l’enquête et la fin** (27 fins textuellement distinctes) | 27 copies avec un mot différent |
| TTS : `notes` + params dans l’**xlsx** ; le JSON généré recopie `speaker` + `prosody` | `text_xai_tags` = copie de `text` ; un seul `length_scale` partout ; `emphasis_words: ["sac"]` sur chaque phrase |
| Un merci/bravo **vécu une fois**, lié au geste | Refrain « Bravo, bon travail » ; zéro reconnaissance |

Étalon vocal : `examples/example2/raw.js` (profils opening/choice/clue/obstacle/resolution/ending). Ne **pas** recopier l’escargot ailleurs. Piper : `slow` seulement choix, danger doux, émotion sensible. **Suite :** F-NAR-024 — ces params vivent dans l’**Excel** ; le JSON et l’audio sont générés.

---

## Après avis3 — préparer la vente (pas de code dans cette passe)

Source : `gestion_projet/feedback_chatgpt/avis3.txt` (5 sept. 17:08, audit `3d0793c0`). Verdict : atelier fort, **pas un produit vendable**. Priorité = petite collection irréprochable + audio + expérience, **pas** plus de fonctions boutique.

**D38 inchangé pour l’écriture** du corpus. **La vitrine et Stripe** ne s’appuient plus sur « 1 449 histoires ».

### F-NAR-020 — Collection fondatrice (24)

8 N1 + 8 N2 + 8 N3. Moitié ATOM, moitié ramifiées. 6 besoins parentaux : calme, autonomie, vivre avec les autres, faire attention à soi, émotions, langage/quotidien.

Chaque titre : relecture humaine, vocabulaire, psychopédagogie, méta vocale synchrone, audio, écoute enfant + parent. TREE-AUT-001 reste l’étalon structurel. Ne pas commercialiser *Le citron de Victorina* tel quel (protocole éducatif, « sent le vert »).

Ensuite seulement : 60, puis 120, puis le reste.

### F-NAR-021 — Tics et titres

Comptages avis3 (837 actives) : « en ce moment » 818, « bravo » 1 575 (surtout ATOM), « tout doux » 500, « sans se presser » 300, « refuse de foncer » 836 (surtout TREE). Contrôle automatique + passe humaine. Huit titres en double (nappe à carreaux, pain chaud de Nino, etc.) : un titre unique par `story_id`.

### F-NAR-022 — Invalidation vocale

Si `text` change : SSML, `text_xai_tags`, `notes`, audio **périmés** jusqu’à régénération. TREE-AUT-001 a déjà du texte et des tags désynchronisés.

### F-NAR-023 — Séries

Continuité affective, après les 24 :

- *Amir et les petits défis* — autonomie, sécurité  
- *Nina trouve une idée* — émotions, relations  
- *Les journées de Victorina* — découverte, langage, quotidien  

L’enfant s’attache au personnage ; le parent choisit la compétence.

### F-NAR-024 — Chaîne Excel → JSON → audio

Un produit, un serveur. **AcoMytha** écrit les histoires (Excel) **et** les dit (`TtsApp` dans le même FastAPI). L’ancien dépôt AkoMythaTTS est fusionné sur la branche `AkoMythaTTS`. Contrat : `stories/FORMAT_JSON_TTS.md`. Éditeur : `#/admin/editeur`.

**Source = Excel.** Chaque xlsx porte le texte des passages **et** les paramètres de prosodie. Un moteur convertit l’Excel en JSON (schema 2.0). Le TTS prend le JSON et produit l’audio. L’app affiche le catalogue **branché sur ces audio**.

**Trois dossiers, fichiers plats** (les IDs Excel font les noms ; pas de sous-dossier par histoire) :

| Dossier | Fichiers |
| --- | --- |
| `stories/arbres/` | `<story_id>.xlsx` |
| `stories/json/` | `<story_id>.json` (+ `voice_registry.json`) |
| `stories/audio/` | `<story_id>_<chunk_id>.wav` — le `chunk_id` porte transition (`T`) et passage (`P`) |

Le moteur de conversion **le fait déjà** (`story_id` = stem xlsx, `chunk_id` = colonne). Bake actuel encore `audio/<story_id>/<chunk_id>.*` : à aplatir plus tard.

**Séparer profil et prosodie** (la prosodie s’écrit dans l’Excel, le JSON la recopie) :

| Couche | Où | Quoi |
| --- | --- | --- |
| Profil du parlant | `stories/json/voice_registry.json` | Identité permanente : narrateur, papa, maman, enfant Amir, maîtresse, troupe D16. Pas la scène. |
| Prosodie du passage | colonnes Excel du chunk → `segments[].prosody` | Comment **cette** réplique est dite : vitesse, pitch, pauses, émotion, intonation, emphase. |

Ne pas fusionner les deux. Amir reste Amir ; il ne parle pas pareil selon la scène.

**Atelier :** conversion, empreintes et JSON→audio sont dans l’éditeur. Aplatir tout le corpus en `stories/audio/<story_id>_<chunk_id>.wav` et brancher le catalogue enfant dessus : suite. Qualité Excel inchangée.

### F-DAT-002 — Métadonnées vocales dans l’app

`catalog.py` n’importe aujourd’hui que texte, réponses, graphe, attente, nuit depuis l’xlsx. Cible F-NAR-024 : le **catalogue de l’app est branché sur les audio générés** (noms `story_id` + `chunk_id`), pas sur un manuscrit JSON. JSON = entrée TTS seulement.

### F-AUD-008 — Audio des 24

Git : 2 témoins (`ATOM-SAN.ALI.001-01`, `TREE-SEC-001`). Pas de vente tant que les 24 n’ont pas d’audio contrôlé. Puis étendre. F-AUD-007 (bruits) sur cette collection d’abord.

### F-APP-009 — Vitrine qui convertit

Remplace le hero actuel (F-APP-004) pour la vente :

- Sur-titre : histoires audio interactives 3–6 ans  
- Titre : *Des aventures qu’il adore. Des gestes qui l’aident à grandir.*  
- CTA : **Écouter une aventure** (extrait 30 s dans le hero)  
- Signature : *Ce soir, une aventure. Demain, un petit geste en plus.*  
- Six phares, pas un catalogue de centaines de cartes  
- Collections par besoin, pas par ID technique  
- Jour/nuit expliqués sans promettre l’endormissement  
- FAQ, confiance, prix en euros  
- Interdit : « leçons », « > 1400 histoires » en argument principal, « respect du feu rouge » comme exemple sec  

### F-PAR-006 — Parent familial

Accueil : « Pour ce soir », continuer, reco âge. Onglets : Mon enfant, Histoires (besoins), Mes histoires, Compte. **Hors barre** tant que ce n’est pas vrai : commande personnalisée, enregistrement de voix (l’UI débite 5 acm sans fichier). La recharge Stripe (F-PAY-001) est réelle quand les clés env sont là : ne plus afficher un badge « Stripe prêt » fictif. F-PAR-004 (signalement) reste une autre feature.

### F-ENF-002 — Enfant illustré

3–5 grandes cartes : héros, couleur, titre lu à voix haute, nouveau/continuer. Choix = gros pictogrammes. Fin ≠ « C’est fini » : souvenir + « Écouter encore ».

### F-PLY-006 — Nuit parentale

Le parent règle jour/nuit **avant** de passer l’appareil. L’enfant ne bascule plus tout seul (F-PLY-003 existe, le réglage enfant reste ouvert).

### F-PAY-004 — Offre euros

- AcoMytha Famille **7,99 € / mois** : aventures publiées, jour/nuit, sélection, nouveautés  
- Pack Découverte **9,90 €** : 10 aventures  

**Pas encore dans Stripe.** F-PAY-001 ne fait que la recharge portefeuille 10–50 € → acm. L’abo et le pack Découverte restent à brancher (Checkout ou Billing). acm seulement pour des extras plus tard. Pas de démo paiement dans l’espace client public.

### F-PAY-005 — Parrainage (plus tard, ne pas coder)

Quand quelqu’un **parraine** un nouveau compte :

- Celui qui parraine reçoit des **acm** égaux au **premier chargement / conversion** (€ → acm, F-PAY-001) — lecture : égal au premier chargement **du filleul** (la phrase « de votre parrain » est à confirmer à l’implémentation).
- **Le parrain** reçoit **le double** de **sa** première charge.

Monnaie = acm (F-PAY-003), pas d’euros bonus. Un seul premier chargement compte. À caler après F-PAY-004. **Pas maintenant.**

### F-SEC-004 — Durcir avant prod

Retirer identifiants démo préremplis, mots de passe / PIN par défaut en public, cookie insecure. Ajouter recovery mot de passe, vérif e-mail, rate limit login/PIN. F-ACC-004 garde le PIN 4 chiffres.

### F-ADM-005 — Légal et dépôt

CGU, confidentialité, mentions, consentement, assistance, suppression de compte. `requirements` verrouillé, Dockerfile, CI, `main` protégée, preprod, Stripe réel, sauvegardes.

### F-AUD-007 — Immersion sonore (toutes les histoires)

**Portée : générale.** Ce n’est pas une feature « parc / ambulance / chien ». Ces scènes ne sont que des **exemples**. Dès qu’un événement du monde est raconté, l’enfant qui écoute **l’entend**, dans **chaque** histoire, **chaque** chunk.

Principe : plonger l’écouteur **dans** le monde du récit. Le narrateur décrit ; le décor et les actions **sonnent**.

Exemples (non exhaustifs) :

| Le récit dit | On entend |
| --- | --- |
| On arrive au parc, les enfants s’amusent | Rires / jeux |
| Une voiture ou une ambulance passe | Passage du véhicule |
| Un chien aboie pour dire bonjour | Aboiement amical |
| Un enfant fait tomber une assiette | L’assiette qui tombe |
| On ouvre un robinet, on ferme une porte, on verse de l’eau… | Le geste correspondant |

Colonne Excel **`sons`** sur chaque chunk : ids de bruits, ou **vide = silence** (cas fréquent et voulu).

Règle d’écoute : **ne pas parler dans le bruit.** D’abord le son des choses / de l’environnement, **puis** l’histoire reprend **au calme**. Pas de fond bruyant sur tout le passage.

S’applique à **tout le corpus**. Positif only. Nuit = plus bas, skip ce qui réveille. Lexique extensible : `stories/outils/fx/lexique.json`. **STRAT-002** §4b.

### F-AUD-006 — Voix de rôles

Le narrateur décrit la scène. Maman, papa, maîtresse, grands-parents, héros et copain/copine ont **des timbres distincts**. Interdit dans l’audio enfant : « maman dit », « papa dit ». Colonne `script` dans les xlsx. Outil : `stories/outils/voice_cast.py`. Bake : `xlsx_to_audio.py`.

**D20 :** l’adulte **parle**. Féliciter le bon geste, discuter, poser une question de la scène. Ne pas remplir avec « papa sourit » / « maman est là ». Après une bêtise : dire quoi faire, sans décrire le geste interdit.

### F-AUD-005 — Synthèse sans API payante

Heavy = `narration_plan` seulement. Fichiers **déjà bakés** = Piper local + ffmpeg MP3. Pas de `POST /v1/tts`. **STRAT-002** §2.

**Nouveau pipeline (F-NAR-024) :** Excel → JSON → `TtsApp` (Kokoro, puis OpenVoice si WAV autorisé) dans AcoMytha → `stories/audio/` plat. Piper = bake existant seulement, jusqu’à bascule. Éditeur : `#/admin/editeur`.

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

## Ordre technique recommandé (après avis3)

**Avant toute vente** (pas commencé dans cette passe) :

0. Qualité des histoires **Excel** (F-NAR-008…019). F-NAR-024 : contrat + éditeur déjà dans l’app (branche `AkoMythaTTS`).  
1. `F-NAR-020` — choisir et relire 24 histoires **dans les xlsx**.  
2. `F-NAR-021` + `F-NAR-022` — tics, titres, sync vocale.  
3. `F-AUD-008` — audio des 24 **via Excel → JSON → TtsApp** (éditeur AcoMytha).  
4. `F-DAT-002` — l’app consomme SSML / notes / sons.  
5. `F-APP-009` + `F-PAR-006` + `F-ENF-002` + `F-PLY-006` — vitrine, parent, enfant.  
6. `F-PAY-004` + `F-SEC-004` + `F-ADM-005` — euros, durcissement, légal.  
7. `F-NAR-023` — séries personnages, puis étendre le catalogue.

Plus tard (pas avant vente) : `F-PAY-005` parrainage acm.

Socle déjà sur `main` (ne pas refaire) : `F-NAR-007`, `F-DAT-001`, `F-AUD-004`, `F-PLY-001`.

Ancien ordre (historique) : IDs/SQLite → Piper pilote → chiffrement → jour/nuit → paquets → compte. Graphe git : uniquement `main`. `F-ACC-002` reporté au profit de `F-SEC-003`.

---

## Compte, vitrine, monnaie A (v3.3)

Le parent ne connaît **que** l’e-mail et le mot de passe. Jamais de « clé », jamais de vocabulaire atelier (arbre / forêt) dans l’UI. Tous les montants sont des **paramètres admin**.

### F-ACC-003 — Inscription

Formulaire public : **E-mail** + mot de passe seulement (pas de prénom / nom). Crée le foyer (parent + profil enfant, PIN `2468` par défaut, paramètre `default_child_pin`). À l’activation : crédit `welcome_credit_eur` (défaut **10 €**) → A au taux 1–10 €.

Connexion : e-mail + mot de passe. Compte déjà ouvert ailleurs : *« Ce compte est déjà ouvert sur un autre appareil. Écrivez-nous si vous avez changé de téléphone. »* Pas le mot « clé ».

### F-ACC-004 — Code à 4 chiffres

Le parent modifie le PIN (actuel + nouveau + confirmation). Exactement **4 chiffres**. Le **même** code sert à passer en mode enfant **et** à revenir au parent.

### F-APP-002 — Accueil vitrine

Sans connexion. Catalogue filtrable (recherche, thème, âge en **filtre seulement**, forme). Écoute invité : F-APP-006.

L’accueil **séduit**, ce n’est pas un tutoriel. **Pas** le mot « gratuitement ». **Pas** de formulaire « Proposez une histoire ». **Pas** de pastille « Courte ». **Pas** d’âge sur les cartes (l’âge reste en donnée + filtre).

Contenu affiché :

- Titre : *Apprendre par l’histoire.*
- *AcoMytha l’univers d’histoires ludiques et captivantes.*
- *AcoMytha en chiffres.* Plus de 1000 histoires, une dizaine de thèmes, une centaine de leçons (pas les compteurs exacts).
- *AcoMytha, c’est quoi ?* L’enfant apprend par l’histoire, de façon interactive, uniquement par la voix, sans écran, sans bouton. Leçons variables (ex. feu rouge, partage des jouets, légumes).
- *AcoMytha, deux modes.* Jour : questions / réponses et options d’histoires. Nuit : moins d’interaction, écouter jusqu’à dormir.
- *Offrez à votre enfant l’opportunité d’apprendre par l’histoire.*

Histoires ramifiées : liste de **liens** vers les autres histoires de la même leçon ; clic → **pop-up** avec le panneau de cette histoire (écoute, liens).

Libellés cartes (F-PAR-002) : **Avec interaction** si passages-questions ; **Avec ramifications vers d’autres histoires** si l’histoire en lance d’autres. Rien d’autre.

Histoire offerte (atelier) : paramètre `free_story_ids` (défaut `TREE-SEC-001`).

Le catalogue de l’accueil **ne charge pas** les 1445 cartes d’un coup (F-APP-003).

### F-APP-003 — Accueil par lots (scroll infini)

**Problème :** la vitrine demandait tout le catalogue d’un coup. 1445 cartes, c’est lourd, ça fige, ça n’a pas l’air d’un rayon.

**Cible :** on affiche un **premier lot**. En descendant, on charge le lot suivant. Impression de scroll infini. Le parent ne voit pas « page 1 / 241 ».

Paramètre admin `home_catalog_page_size` (défaut **6**, entre 1 et 48). Même taille pour le premier lot et les suivants.

Filtres (recherche, thème, âge, forme) : on recommence au premier lot, le total reste le nombre d’histoires qui matchent.

API publique : `GET /api/public/stories?limit=&offset=` → `{ items, total, limit, offset }`. Pas tout le corpus dans la première réponse.

L’espace parent n’est pas concerné (sélection, pas vitrine).

### F-APP-004 — Titre d’accueil

Titre : *Apprendre par l’histoire.*  
Ligne d’ambiance : *AcoMytha : univers d’histoires ludiques et captivantes.*

**Créer un compte** uniquement en haut à droite. Pas de second bouton dans le hero.

*AcoMytha en chiffres* : plus de 1000 histoires, une dizaine de thèmes, une centaine de leçons.

Bloc *AcoMytha, c’est quoi ?* : voix seulement, sans écran, sans bouton ; leçons variables (feu rouge, jouets, légumes…).

### F-APP-005 — Vitrine chambre d’écoute

Accueil public : scène sombre (écoute), catalogue dans la scène. Fraunces + Outfit. Champ acoustique autour du symbole. Jour / nuit en deux matières. Chiffres monumentaux. Cartes verre / or. Copie fondateur conservée. Parent / admin / enfant : F-APP-007.

### F-APP-006 — Écoute vitrine (invité)

Sur l’accueil **sans compte** :

- Chaque carte du catalogue a **Écouter** (toutes les histoires du rayon).
- Un clic joue **30 secondes** de l’histoire (clip serveur, chemin par défaut).
- À la fin des 30 s : **pop-up** — se connecter ou créer un compte pour écouter la suite. Arrêt manuel = pas de pop-up.
- **Aucun prix acm** sur la vitrine. **Aucun solde.** Prix et solde uniquement après connexion (espace parent).
- Paramètre `preview_seconds` = 30 (visiteur). Parent non acheté reste `parent_preview_seconds` (30). Histoire achetée / enfant : entier.

D34. Remplace l’ancien aperçu visiteur de 10 s (D23) pour la vitrine.

### F-APP-007 — Identité hors vitrine

Après F-APP-005, connexion, inscription, espace parent, console admin et mode enfant partagent les **mêmes jetons** (nuit, or, crème, Fraunces). Portes = feuille crème sur la scène (comme le pop-up). Parent / admin / enfant = scène + verre / or. Le parent voit **solde et prix acm**. L’invité, non. D36 (remplace la palette claire/bleu de D14).

### F-NAR-017 — Veille feedback (rappel)

Le watchdog **signale** un fichier nouveau (`ACTION_REQUIRED`). Il **n’applique pas** les réécritures. L’agent de la conversation principale priorise et traite, pour éviter deux mains sur les mêmes xlsx. D35.

### F-PAR-002 — Libellés catalogue

| Condition | Libellé UI |
| --- | --- |
| Passages avec questions | Avec interaction |
| Peut lancer d’autres histoires (`kind=ramifiee`) | Avec ramifications vers d’autres histoires |
| Sinon | pas de pastille sur la vitrine |

### F-PLY-002 — Arrêt et durée

Pendant l’écoute : barre collée **Arrêt** (et bouton carte). Stop coupe l’audio. Chaque carte affiche la **durée** (minutes). L’âge n’est pas affiché sur la carte.

### F-PAY-001 — Stripe Checkout (recharge acm)

Branche `stripe` mergée dans `main` (`3e4335b8`). Code : `app/acomytha/payments.py`, `api/shop.py`, `ParentApp.js`. Procédure : `app/README.md`.

**Ce que c’est.** Le parent verse **10, 20, 30, 40 ou 50 €**. Stripe Checkout **hébergé** encaisse. Aucune carte ne transite par AcoMytha. Le solde acm n’est crédité **que** par un webhook **signé** (`POST /api/shop/stripe/webhook`). Idempotent (un paiement = un crédit, même si Stripe renvoie l’événement deux fois). Change €→acm : F-PAY-002.

**Ce que ce n’est pas.** Pas d’abonnement 7,99 € ni pack 9,90 € (F-PAY-004). Pas de paiement démo, plus de `confirm_demo`, plus de bouton « valider la carte 4242 » dans l’app. La carte `4242…` n’existe que **sur le Checkout Stripe en mode test**.

**Secrets.** Uniquement l’environnement du serveur : `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, `ACOMYTHA_PUBLIC_URL`. Jamais Git, jamais l’admin SQLite (les anciennes clés `stripe_secret` / `stripe_publishable` / `stripe_webhook_secret` sont **effacées** au seed). `.env` gitignoré ; modèle `.env.example`. `Settings` lit `os.environ` : `source .env` avant uvicorn.

**États** (`GET /api/shop/wallet` → `stripe`) :

| Valeur | Sens | Boutons recharge |
| --- | --- | --- |
| `unconfigured` | pas de `sk_…` | désactivés, 503 si POST |
| `webhook_missing` | clé présente, pas de `whsec_…` | désactivés, 503 si POST |
| `invalid` | `sk_live_` sans URL `https://` | désactivés, 503 si POST |
| `test` | `sk_test_…` + webhook | Checkout test |
| `live` | `sk_live_…` + webhook + HTTPS | Checkout réel |
| `planned` | wallet **admin** (pas de recharge) | — |

**Prod.** Endpoint webhook `https://<domaine>/api/shop/stripe/webhook`, `sk_live_…`, nouveau `whsec_…`, `ACOMYTHA_PUBLIC_URL` en HTTPS. F-SEC-004 / F-ADM-005 avant d’ouvrir au public.

### F-PAY-002 — Monnaie et boutique

Unité interne `A` (`balance_a`, `price_*_a`). **Affichage : acm** (F-PAY-003). Plus de « A barré ».

**Change € → acm** (à la recharge, selon le montant versé) :

| Tranche versée | Taux |
| --- | --- |
| 1–10 € | 1 € = 1 acm |
| 11–20 € | 1 € = 1,25 acm |
| 21–30 € | 1 € = 1,50 acm |
| … | +0,25 acm / € tous les 10 € |
| plafond | 1 € = 5 acm |

Paramètres : `fx_rate_start` 1 · `fx_rate_step` 0,25 · `fx_rate_every_eur` 10 · `fx_rate_max` 5.

Crédit d’activation 10 € → **10 acm**. Le parent achète avec ce solde. Quand il est à 0, il recharge (F-PAY-001).

**Dépenses (défauts admin) :**

| Action | Prix | Paramètre |
| --- | --- | --- |
| Histoire déjà au catalogue | 1 acm | `price_story_a` |
| Série complète (histoire avec des choix / arbre atelier) | 1 acm | `price_tree_a` |
| Commander une histoire (contexte → l’équipe la crée sous quelques jours) | 1,5 acm | `price_order_a` |
| Chaque branche demandée en plus (max 3) | +0,5 acm | `price_ramification_a`, `max_ramifications` 3 |
| Enregistrer une voix (puis l’attribuer : narrateur, papa, maman, copain…) | 5 acm | `price_voice_record_a` |
| Appliquer cette voix à toutes les histoires déjà achetées | 5 acm | `price_voice_apply_all_a` |

Les voix nouvelles s’appliquent aux **prochaines** histoires achetées. L’application à tout le déjà-acheté est l’option 5 acm.

Offre catalogue prévue : **10 nouvelles séries** pour **10 €** (`pack_trees_count` 10, `pack_trees_eur` 10) — affichage après compte, paiement via F-PAY-001.

Le parent dépense ses acm : histoires, séries, commandes, voix. L’admin change tous les chiffres sans redéployer.

### F-PAY-003 — Symbole acm et logo

**Un seul dessin** pour la monnaie et la marque. C’est le glyphe organique (chemins + points or), pas un « A » barré.

Où il apparaît :

- **Logo** : accueil, connexion, inscription, barre parent, console, mode enfant, favicon. Mot « AcoMytha » à côté du glyphe.
- **Montants** : chaque fois qu’on peut obtenir un produit ou un service — prix d’une histoire (vitrine et parent), solde, packs de recharge, commande, voix, paiement. Forme `1 250` + glyphe. Libellé accessible « acm ».
- **Tailles** : le glyphe suit la taille du texte (`1em`). Variantes `xs` / `sm` / `md` / `lg` / `xl` pour le logo. Fond sombre : violet clair.

Technique : `<symbol id="acm-mark">` une fois dans `index.html`, `<use href="#acm-mark">` partout. Fichier `assets/acm-mark.svg` pour l’icône. Helper `js/ui/acm.js` (`acmAmount`, `acmLogo`). Pas de JavaScript pour dessiner.

Les deux maquettes HTML fournies sont des **exemples de mise en page**. Le glyphe retenu est le dessin détaillé (chemins du logo). L’autre esquisse (forme simplifiée + pastille) n’est pas un second symbole.
