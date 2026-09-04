# Décisions — application web (3 septembre 2026)

Fondateur pas devant le PC : décisions prises, pas de questionnaire.

| # | Sujet | Décision |
| --- | --- | --- |
| D1 | VLC snap | Conservé techniquement (sudo requis pour `snap remove --purge vlc`). Masqué du menu. Lecteur réel = `~/.local/bin/vlc` (paquets Ubuntu extraits). |
| D2 | Merge `main` | Le corpus `F-GEN-001` est mergé en fast-forward sur `main` (`837d436`) : consigne du jour, graphe linéaire. |
| D3 | Multi-appareils | Interdit au MVP. Une clé → un `device_id`. Reset = admin. |
| D4 | Enfant | Profil + PIN sur l’appareil parent, pas une licence séparée. |
| D5 | Front | Web Components + CSS objets, pas React. |
| D6 | Back | FastAPI + SQLite + classes service. |
| D7 | Chiffrement | AES-256-GCM, clé d’histoire dérivée (HKDF) du master local, lazy `.chk`. |
| D8 | Comptes démo | `admin@acomytha.local` / `acomytha-admin` · `parent@acomytha.local` / `acomytha-parent` · PIN `2468`. |
| D9 | F-APP-001 | Feature complexe : stories (socle, catalogue, auth, appareil, 3 UI, lecteur) en commits sur `main`. |
| D10 | F-AUD-006 | Plusieurs voix Piper par chunk (mix). Narrateur = Tom. Papa = Pierre. Maman = Siwis. Maîtresse = Jessica. Enfants = pitch ↑. Pas d’API TTS payante. F-AUD-003 (voix unique) abandonné. |
| D11 | F-AUD-007 | Immersion **générale**. Colonne `sons` (vide = silence). Ordre : bruit seul, puis récit au calme. Jamais parler dans le bruit, jamais nappe sur tout le passage. |
| D12 | F-NAR-008 | Reconstruire les textes autour d’un fil rouge. L’xlsx n’est touché qu’après fusion d’agents. Passe 2 : fusion **éditoriale** (un moment par chunk, 3–6 ans, leçon vécue en fin). Le merge « plus long gagne » recolle un cours : on ne s’en sert pas comme vérité. |
| D13 | Marque | Le produit s’appelle **AcoMytha**. « Sentier » est retiré de l’UI, du code, des docs et des comptes démo. |
| D14 | UI parent | Pas de métaphore forêt/arbre dans l’UI. Histoires, sélection, interaction, ramifications. Palette : **D36**. |
| D15 | Vitrine + A | Accueil public, inscription e-mail/mdp, aperçu 10 s (non affiché). Pas « gratuitement », pas pastille Courte, pas âge sur les cartes. |
| D16 | Troupe enfant | Amir, Aniss, Sarah, Chouchou, Mila, Nino, Nina, Raphaël, Victorino, Victorina. Pas d’autre prénom d’enfant. Une histoire = 1 héros, au plus 1 autre enfant, papa/maman. |
| D17 | Durée | Histoire ≥ 3 min. Plusieurs passages ; certains portent une leçon. Atomique : plusieurs leçons possibles pour tenir 3 min. Allonger si le récit le demande. |
| D18 | PIN | 4 chiffres, modifiable par le parent. Même code pour entrer en mode enfant et en sortir. |
| D19 | Libellés | Interaction = questions. Ramifications = lance d’autres histoires (liens + pop-up vitrine). |
| D20 | Adultes parlent | Papa et maman ont des répliques. Exemples fondateur (pas un moule) : « bravo t'as fais du bon travail » ; bêtise → discuter, « as tu fini de ranger tes jouer? ». Interdit « papa sourit » / « maman est là » à la place d’une réplique. POS-001. Détail : `ECHANGES.md` §6. |
| D21 | Ordre des passages | Le moteur enchaîne **tous** les fichiers audio d’une histoire, quel que soit leur nombre. Atomique = ordre des IDs. Ramifiée = défaut / option, sans sauter vers une branche sœur. |
| D22 | Narrateur | Voix Tom trop basse dans le mix. RMS aligné par réplique, volume et présence relevés, cuisson relancée. |
| D23 | Aperçus | Parent non acheté : 30 s. Parent acheté / enfant : histoire entière. Visiteur vitrine : **D34**. Clip serveur. |
| D24 | Stripe | Recharge 10–50 € via Checkout si clés admin. Sans clé : paiement démo (carte 4242) qui crédite le solde, pour valider l’UI. |
| D25 | Ouverture | Pas d’entrée brutale (« constentin joue au salon »). Monde d’abord, puis « en ce moment ». Deux **exemples** fondateur (conte / présentation, Constantin) : `ECHANGES.md` §7 — **pas un moule**, inventer. Audio plus tard. |
| D26 | acm | Monnaie affichée **acm** (glyphe organique = logo). Code interne inchangé (`A`, `balance_a`). Plus de A barré. |
| D27 | Accueil lots | Vitrine : lots de `home_catalog_page_size` (défaut 6), chargement au scroll. Pas les 1445 d’un coup. |
| D28 | Accueil titre | Hero : *Apprendre par l’histoire.* / *AcoMytha l’univers d’histoires ludiques et captivantes.* |
| D29 | Git | Uniquement `main`. Plus de branche `feat/…`. Message `feat(F-XXX):` / `fix(F-XXX):`. |
| D30 | Récit f_04 | Désir ≠ leçon ; arc et vraie fin ; question en chaîne ; chemins cohérents. Source `feedback_chatgpt/f_04.txt`. F-NAR-010…015. |
| D31 | Pilote ramifié | Priorité : TREE-AUT-001 (actif) et TREE-COL-001 (archive). Un seul ramifié dans `stories/arbres/` ; 763 autres en `stories/archive/arbres/`. |
| D32 | Veille ChatGPT | Watchdog inotify worktree **et** clone SSD. Nouveau fichier → signal. |
| D33 | N1 ramifié | Un arbre ramifié garde **3 options** par nœud (contrainte d’arbre). La règle N1 « 2 options max » vaut pour les atomiques. |
| D34 | Vitrine écoute | Invité : 30 s de **chaque** histoire, puis pop-up connexion / inscription. Pas de prix acm ni de solde avant connexion. F-APP-006. |
| D35 | Veille sans conflit | Le watchdog **prévient** seulement. Le traitement éditorial est fait par l’agent principal, jamais en parallèle du watchdog. F-NAR-017. |
| D36 | Identité hors vitrine | Connexion, inscription, parent, admin, enfant : mêmes jetons que la vitrine (nuit, or, crème, Fraunces). Solde et prix acm après connexion. F-APP-007. |
| D37 | POO | Encapsulation réelle : champs privés, propriétés pour les invariants. Pas un getter/setter vide par variable. Une classe = un rôle. Routeurs FastAPI inchangés. F-APP-008. |
| D38 | Catalogue entier | Les consignes récit (monde, désir, imprévu, résolution, fin heureuse, leçon greffée) s’appliquent à **toutes** les histoires (685 ATOM + ramifiés). Plus seulement AUT-001 / COL-001. Texte d’abord, audio ensuite. Voix : lent, non robot, non monotone. |
| D39 | Vitrine chiffres | Accueil : **> 1400** histoires, **> 10** thèmes, **> 80** leçons. Totaux exacts dans `stories/CHIFFRES.md` seulement. |
