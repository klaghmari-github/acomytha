# AcoMytha — backlog features

**Version :** 4.5 — 5 septembre 2026. Remplace `AcoMytha_Backlog_Features_v2.0.xlsx`. Gel : `gestion_projet/ETAT_REPRISE.md`.  
**Branche :** `main` seulement. Message `feat(F-XXX): …` / `fix(F-XXX): …` (voir `consignes.txt`). L’ID ne change plus.  
**Demandes + exemples fondateur :** `decisions/ECHANGES.md` (traçabilité).  
**Spec :** `specification/AcoMytha_Specification.md`. Les colonnes *Strat* pointent le document d’architecture, pas une copie.  
**Web :** `STRAT-005`. Statut : **développé** = sur `main`.

Priorités : **P0** première écoute réelle · **P1** MVP familles · **P2** juste après · **P3** v2 (ne pas démarrer).

Phases : 0 cadrage · 1 contenu · 2 MVP web (puis native) · 3 interaction fermée · 4 renouvellement · 5 leçons parentales · 6–7 hors MVP.

### Statut (5 sept. 2026)

| ID | Statut | Note |
| --- | --- | --- |
| F-GEN-001 | **développé** | Corpus 1445 xlsx + audio témoin stéréo 44100. `main` = `837d436`. |
| F-NAR-007 | **développé** | IDs chunks dans les xlsx. |
| F-TAX-001 / F-TAX-002 | **développé** | `lecons.xlsx` + `lecon_histoires.xlsx`. |
| F-AUD-005 | partiel | Piper local, échantillons git + bake disque. |
| F-AUD-002 | **développé** | Loudness : narrateur aligné (plus audible). |
| F-ACC-002 | **reporté** | Contredit F-SEC-003 (une clé = un appareil). |
| F-APP-001 | **développé** | Socle FastAPI + PWA, POO HTML/CSS/JS. |
| F-DAT-001 | **développé** | SQLite live **764** histoires / **10221** chunks (685 ATOM + 79 TREE). Corpus xlsx 1449. |
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
| F-NAR-016 | **en cours** | Pilote ramifié fait. **D38 : tout le catalogue** (685 ATOM + 764 TREE). Chiffres : `stories/CHIFFRES.md`. |
| F-NAR-017 | **développé** | Veille `feedback_chatgpt/` : nouveau fichier → consignes → histoires gardées (texte). |
| F-NAR-018 | **en cours** | Étalon structurel (avis2) : oral fluide, pas de morale dite, ramification = 9 aventures, ATOM sans récap. |
| F-NAR-002 | **développé** | Enchaînement de tous les passages (atomique et ramifié). |
| F-ACC-003 | **développé** | Inscription e-mail + mot de passe (pas de prénom). Libellé « E-mail ». |
| F-ACC-004 | **développé** | Parent change le PIN 4 chiffres. Même code parent ↔ enfant. |
| F-APP-002 | **développé** | Vitrine publique, catalogue, pop-ups ramifications. Écoute invité : F-APP-006. |
| F-PAY-001 | **développé** | Stripe Checkout + webhook. Sans clé : paiement démo. |
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
| F-PAY-002 | Boutique | Monnaie interne, solde, achats (Stripe plus tard) | P1 | 2 | STRAT-005 | F-ACC-003 |
| F-PAY-003 | Marque | Symbole acm + logo (un seul dessin) | P1 | 2 | STRAT-005 | F-PAY-002 |
| F-PLY-002 | Lecture | Arrêt visible + durée sur les cartes | P0 | 2 | STRAT-004 | F-PLY-001 |
| F-PAR-002 | Parent | Libellés interaction / ramifications | P0 | 2 | STRAT-005 | F-PAR-001 |

### F-APP-001 — Socle

`app/` : FastAPI factory, fichiers statiques, custom elements, jetons CSS, hash-router. Comptes démo locaux. Responsive téléphone / tablette / bureau. Encapsulation : F-APP-008.

### F-APP-008 — Encapsulation POO

Une classe = un rôle. État **privé**. Accès public par **propriétés** (invariants, pas un getter vide par champ). Python : `ShopParams`, `WalletBook`, `PreviewStudio`, `Settings`, coffre, graphe, session. JS : champs `#`, `Component` injecte api/router, `Session`, `StoryEngine`, `CryptoPlayer`. CSS : `tokens` / `objects` / `components` / `shells`. HTML = custom elements. D37. Les routeurs FastAPI restent des routeurs (c’est le cadre).

### F-SEC-003 — Un appareil

`device_id` persisté sur le client. Premier login lie. Deuxième empreinte → HTTP 409 + `DeviceAlert`. L’admin peut reset. L’enfant n’ouvre pas une 2ᵉ liaison.

### F-ENF-001 — Enfant

Pas de filtres, pas de compte, pas d’admin. File = histoires cochées par le parent. Grandes cibles, mode jour/nuit.

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

Graphe git : uniquement `main`. Le message de commit porte l’ID de feature. `F-ACC-002` reporté au profit de `F-SEC-003`.

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

### F-PAY-001 — Stripe

Onglet parent **Obtenir des pièces AcoMytha**. Boutons **10, 20, 30, 40, 50 € → acm** (symbole de change). Checkout Stripe si `stripe_secret` (admin ou env). Webhook `POST /api/shop/stripe/webhook`. Sans clé : écran de paiement démo qui crédite le solde.

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
