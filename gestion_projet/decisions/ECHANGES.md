# Traçabilité — demandes et exemples du fondateur

**Rôle.** Ce fichier n’est pas la spec. C’est le **fil des demandes** (3–4 septembre 2026 et suite) : ce qui a été dit, **surtout les exemples**.  
Les exemples sont des **manières**, pas des moules. Si un exemple contredit une règle (prénom hors troupe, adulte nommé Luca…), la **règle gagne** (D16, papa/maman). L’exemple reste pour le **ton**.

**Où ça vit ensuite.** Spec : `specification/AcoMytha_Specification.md`. Backlog : `backlog/Features.md`. Décisions courtes : `DECISIONS_APP.md`. Git : `consignes.txt`.

Les citations entre `>` sont le fondateur, orthographe d’origine.

---

## 1. Produit

Audio seulement, enfants **3–6 ans** (N1 / N2 / N3). Famille **papa–maman**. Formulation positive (POS-001) : dire quoi faire, ne jamais décrire le geste dangereux. Monde jardin. Absents : religion, politique, guerre, crime, discours de genre.

Le produit s’appelle **AcoMytha**. « Sentier » est retiré (D13).

Pas d’opinion demandée à l’agent : décider, noter D*.

---

## 2. Corpus et leçons

Générer les histoires **atomiques** (sans bifurcation) et **ramifiées** (≥ 3 choix, chaque branche ≥ 3, max 3 niveaux). Couvrir les domaines / sous-domaines. Valider contre les règles. Corpus 1445 xlsx (F-GEN-001).

Une leçon peut revenir dans **plusieurs** histoires, racontée **autrement**, dans un **autre contexte**.

> une leçon peut apparaitre dans différents histoires, par exemple respecter le feux rouge, on peut avoir plusieurs histoire avec des passage de traverser la route dans la leçon peut revenir dans différents histoires elle sera raconté de façon différentes dans un contexte différent.

Histoires dans **un seul dossier** (`stories/arbres/`), pas une forêt de sous-dossiers. Base **relationnelle** histoire ↔ leçon ↔ chunk (F-DAT-001, STRAT-003).

---

## 3. Audio, protection, moteur (demande longue)

### Format

> quel est le format le plus facile à générer wav ou mp3 ? car tous les smartphone iphone apple ou samsung android ou huwawai chinoix tous ont des lecteurs mp3.

Livraison : WAV 44100 **stéréo** + MP3 128k (le mono 22050 était inaudible sur téléphone). F-AUD-002.

### Chiffrement et RAM

> je dois réfléchir à une solution pour protéger les histoires. c'est à dire ne pas télécharger dans un format propre . mais une sorte de fichier chiffré. il n y a que l'application qui le déchiffre. le dechiffrement est rapide et ensuite la lecture se fait dans la RAM du smart phone

> on déchiffre un et pendant qu'on fait la lecture du premier on déchiffre le suivant, et ainsi de suite. […] on déchiffre et on charge en mémoire que chunk by chunk ca doit fonctionner rapidement sur les pc mais aussi rapidement sur les smartphone meme les plus pauvres.

F-AUD-004, D7. Prefetch N+1.

### Identifiants (exemple fondateur)

> identifiant de l'histoire : STO_00001 et identifiant du chunk : CHK_T_0001_P_0000 (chunk de transition 1. […] les chunk de passage ont un identifiant. CHK_T_0001_P_0001 ou CH_T_0001_P_0002 selon les options.

> la règle est que le tout premier passage de l'histoire il a l'identifiant CHK_T_0000_P_0000. et une fois qu'il est fini le suivant est forcement CHk_T_0001_P_0000 […] si on trouve pas le CHK_T_XXXX_P_0000 ça veut dire que l'histoire est finie.

Implémenté : `CHK_T0000_P0000` (sans underscores internes), F-NAR-007.

### Questions vs histoire

> des questions pour vérifier que l'enfant ecoutes bien, on lui demande le feu est rouge est ce qu'on peut traverser ? ca ne change pas le cours de l'histoire car dans tous les cas l'enfant ne va traverser que si le feu est vert.

Question d’écoute ≠ branchement narratif. F-INT-005 / F-PAR-002.

### Jour / nuit

> le mode jour il y a l'interaction, le mode nuit l'enfant doit dormir et ne fait que ecouter on lui pose pas de question. dans le mode nuit on peut desactiver aussi le branchement et laisser le moteur choisir les branchement qu'il veut.

F-PLY-001, STRAT-004.

### Délai 3 s

> au bout de 3 secondes sans réponse un choix est fait quand meme automatiquement. les 3 secondes sont parametrable. on peut meme dire une répétition de la question une fois avant de prendre une decision automatique.

F-PLY-005.

### Transitions (exemples)

> le chunk de type transition y en en fait deux type transition_question c'est à dire la question du genre "que va faire la maman ? ou que veut tu qque le chat fasse ensuite ?" puis les chunk de type transition_option "jouer" ou "sortir au parc" ou "aller à l'anniversaire d'un copin".

### Budget

> je ne veux pas payer meme pas un centime de plus autre que mon abonement deja reglé heavy

TTS = Piper local. Pas d’API TTS payante. D10.

---

## 4. Application web

POO, HTML/CSS/JS + FastAPI, PWA, responsive. Trois shells : parent, enfant, admin. Une clé = un appareil (F-SEC-003) ; 2 appareils plus tard, pas au MVP. L’enfant ne voit que la sélection parentale. Marquer les features **développé** une fois sur `main`.

UI parent : **pas** de métaphore forêt/arbre (D14). Pas le mot « clé » face au parent.

Inscription : e-mail + mot de passe, libellé **E-mail**, pas de prénom (F-ACC-003).

PIN **4 chiffres**, le **même** pour entrer en mode enfant et en sortir (D18, F-ACC-004).

### Vitrine

Accueil **sans connexion**, même catalogue. Pas « gratuitement ». Pas pastille « Courte ». Pas l’âge sur les cartes. Pas de formulaire « Proposez une histoire » sur l’accueil.

Aperçus (D23) : visiteur **10 s**, parent non acheté **30 s**, acheté / enfant = entier.

Libellés (D19) : **Avec interaction** / **Avec ramifications vers d’autres histoires**.

### Accueil — lots (exemple 6)

> a la page d'accueil au lieu de charger d'une fois toutes les histoires faites plutot charger un nombre fixe parametrable dans l'interface admin. par exemple 6. les afficher, et faire en sorte que plus on scroll on charge 6 par 6. donner l'impression d'un infinite scroll plutot que tout afficher d'une fois. ajoute ça dans les features, puis fais le.

F-APP-003, D27. Paramètre admin `home_catalog_page_size` (défaut 6).

### Accueil — titre

Remplacer :

> Une multitude d’histoires.  
> Créer un compte. Les transmettre à votre enfant. Le laisser s’immerger.

par :

> Apprendre par l'histoire. Acomytha l'univers d'histoires ludiques et captivantes.

F-APP-004, D28. Affichage : **AcoMytha** (marque). Un seul bouton **Créer un compte** : en-tête, pas le hero.

Stats accueil : pas les chiffres bruts. *Plus d’un millier d’histoires*, *Une dizaine de thèmes*.

Section *AcoMytha, deux modes* (remplace « Jour : plus d’interaction. Nuit : plus calme ») :

> AcoMytha deux modes: modes jour : interactif questions/réponses et options d'histoires. mode nuit moins d'interaction, l'objectif est d'écouter jusqu'à dormir.

Pitch *AcoMytha, c’est quoi ?* (remplace « Votre enfant ne fait pas qu’écouter ») :

> AcoMytha c'est quoi ? l'enfant apprend par l'histoire de façon interactive uniquement par la voix, sans ecran sans bouton. les histoires sont ludiques et contiennent des leçons qui peuvent varier entre respect du feux rouge, partage des jouets, manger les légumes. etc.

### Boutique

Monnaie interne **acm** (affichage), code interne `A` / `balance_a`. Un **même dessin** pour le logo et le symbole de monnaie (F-PAY-003, D26). Prix = paramètres admin. Stripe Checkout ou démo carte 4242 (D24). Recharge 10–50 €.

---

## 5. Voix et immersion

Narrateur ≠ personnages. Interdit « maman dit » à la place de la voix de maman. Piper : Tom = narrateur, Pierre = papa, Siwis = maman, Jessica = maîtresse. Enfants = pitch ↑. D10.

Tom trop bas → RMS / présence (D22).

Le moteur joue **tous** les fichiers audio d’une histoire, dans l’ordre (D21). Pas s’arrêter après C0001.

### Immersion (F-AUD-007) — exemples, pas une liste fermée

Parc / rires, voiture ou ambulance, chien qui aboie, assiette qui tombe, robinet, porte. **Toute** histoire, **tout** événement raconté. Bruit **puis** récit au calme. Jamais parler dans le bruit. `sons` vide = silence.

---

## 6. Récit captivant (F-NAR-008)

Les histoires ne doivent pas ressembler à un **cours**. Un **fil rouge** dirige ; la leçon se **greffe**.

### Adultes parlent (D20) — exemples fondateur

> on peut pas dire à chaque fois "papa souris". le papa doit parler il doit dire bravo t'as fais du bon travail, ce n'est pas bien quand l'enfant fais une betise, le papa peut discuter et demander à l'enfant par exemple "as tu fini de ranger tes jouer?" ce sont juste des exemple il faut s'adapter à la situation.

Ce sont **des exemples**. S’adapter à la scène. POS-001 si bêtise : dire quoi faire / demander, sans décrire le geste interdit, sans humilier. Interdit de remplacer la voix par « papa sourit » / « maman est là ».

### Durée ≥ 3 min (D17)

Plusieurs passages. Certains portent une leçon, d’autres racontent. Atomique : plusieurs leçons possibles pour tenir 3 min. Allonger si le récit le demande.

### Troupe enfant fermée (D16)

Amir, Aniss, Sarah, Chouchou, Mila, Nino, Nina, Raphaël, Victorino, Victorina. **Pas d’autre prénom d’enfant.** Une histoire = 1 héros, au plus 1 autre enfant de la liste, papa et/ou maman.

Adultes racontés : **papa**, **maman** (pas Luca / Céline comme noms d’adultes dans le corpus).

---

## 7. Ouverture non brutale (F-NAR-009, D25)

### Demande (orthographe d’origine)

> l'entrée vers l'histoire est un peu brutal, par exemple j'ai vu une histoire quii commence par constentin joue au salon. je trouve que c'est brutal. il faut commencer par une introduction du genre "il etait une fois, dans un petit village, une petite famille heureuse, un enfant constentin, un papa luca, et une maman celine. un jour pluvieux constentin n'a paas pu sortir au paroc il est resté à la maison. en ce moment même, constentin joue au salon. voilà, il faut que l'histoire soit captivante et très descriptives les enfants adore ça adorent les detailles. ou bien commencer l'histoire par "ceci est l'histoire d'un enfant heureux qui s'appelait constentin, il vivait avec son papa lucas et sa maman celine dans une belle maison. la maison se trouvait dans un village très lointin. en ce moment dans ce village il pleut. constentin ne peut pas sortir au parc. il est au salon entrain de jouer avec des legos, ...." et voilà une autre façon de raconter l'histoire. il faut etre créatif, chaque histoire est racontée d'une manière différente, l'enfant ne s'ennuie pas. ajoute ça dans les features et précise qu'il s'agit d'exemple et qu'il faut être creatif et ne pas se limiter a ces exemples là. et il faut lancer des agents qui vont revoir le texte de toutes les histoires. on verra la conversion audio après

### Ce que ça fixe

| Non (brutal) | Oui |
| --- | --- |
| « Constantin joue au salon. » | Monde d’abord, puis « en ce moment » |
| « On va apprendre : … Voici le geste » | Le fil rouge porte la leçon |
| Recopier « il était une fois » partout | **Inventer** une amorce par histoire |

Les deux textes ci-dessus sont des **exemples de manières**. Prénoms Constantin / Luca / Céline = **illustration** ; le corpus utilise D16 + papa/maman.

**Audio plus tard.** Passe texte sur les 1445.

Autres amorces (encore des exemples) : gouttière, soupe dans l’escalier, rayon sur le tapis, chaussures qui sèchent, doudou dans le canapé, fenêtre embuée, marché au loin.

---

## 8. Git et un seul dossier local

Dossier projet : **`/media/laghmari/ssd-data/dev/akomytha`**. Pas de symlink. GitLab + GitHub = le **même** dossier.

D29 : uniquement **`main`**. Plus de `feat/…`. Message `feat(F-XXX):` / `fix(F-XXX):`.

`gitpush.sh` à la racine :

```bash
./gitpush.sh
./gitpush.sh -m "feat(F-XXX): …"
```

Fetch GitLab **et** GitHub, aligne `main`, add, commit, push les deux.

Deux `checkpoint` locaux sur `ATOM-FAM.SEC.002-05.xlsx` (Cédric, 151 mots) étaient une **régression** face à `main` (408 mots, ouverture monde). On a gardé `main`.

---

## 9. Serveur local

```
PYTHONPATH=app python -m uvicorn acomytha.main:create_app --factory --host 127.0.0.1 --port 8787
```

Depuis `/media/laghmari/ssd-data/dev/akomytha`. http://127.0.0.1:8787

---

## 10. Documents : pas mille fichiers

> je veux pas mille documents, je veux le bon nombre de documents et je veux surtout la completude et l'exactitude et la bonne qualité

| Fichier | Rôle |
| --- | --- |
| Spec unique | produit |
| Features | backlog `F-…` |
| STRAT-001…005 | architectures |
| DECISIONS_APP | D1… |
| **ECHANGES (ici)** | demandes + **exemples** |
| consignes.txt | git `main` |

Les features **pointent** les stratégies ; elles ne les recopient pas — sauf les **exemples fondateur**, qui restent ici et dans F-NAR-009 / F-AUD-007 / D20.

---

## Index demande → feature / décision

| Demande | ID |
| --- | --- |
| Corpus 1445 | F-GEN-001 |
| IDs chunks `CHK_T0000_P0000` | F-NAR-007 |
| SQLite histoire–leçon–chunk | F-DAT-001 |
| Chiffrement RAM, prefetch | F-AUD-004, D7 |
| Jour/nuit, délai 3 s | F-PLY-001, F-PLY-005 |
| Piper multi-voix | F-AUD-006, D10 |
| Immersion générale | F-AUD-007, D11 |
| Fil rouge | F-NAR-008, D12 |
| Adultes parlent (bravo / ranger les jouets) | D20 |
| Ouverture (Constantin / il était une fois / ceci est l’histoire) | F-NAR-009, D25 |
| Troupe fermée | D16 |
| ≥ 3 min | D17 |
| Marque AcoMytha | D13 |
| Vitrine, 10 s / 30 s | F-APP-002, F-PAR-003, D23 |
| Lots accueil, exemple 6 | F-APP-003, D27 |
| Titre accueil | F-APP-004, D28 |
| Symbole acm = logo | F-PAY-003, D26 |
| Git `main` + gitpush.sh | D29 |
