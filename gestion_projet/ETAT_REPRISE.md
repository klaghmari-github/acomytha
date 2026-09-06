# Reprise — AcoMytha

**Lire ce fichier en premier** dans une session neuve. Ne pas « reprendre la dernière conversation ». Le contexte utile est ici et dans les docs qu’il pointe.

Date de gel : **5 septembre 2026**. HEAD : **`4fa95621`**. Worktree, SSD, GitLab `origin` et GitHub `github` = ce commit.

Produit : **AcoMytha** (jamais Sentier). Forêt narrative **audio seulement**, enfants 3–6 ans (N1 / N2 / N3), famille papa-maman. POS-001. Pas religion / politique / guerre / crime / discours de genre.

Le fondateur **interdit de demander son avis**. Décider, noter D*, avancer.

---

## 1. Où est le code

| | |
| --- | --- |
| Clone canonique SSD | `/media/laghmari/ssd-data/dev/akomytha` |
| Worktree Grok | `/home/laghmari/.grok/worktrees/dev-akomytha/2026-09-03-696fa471` |
| Branche | **`main` uniquement (D29)** |
| GitLab | `origin` → `gitlab.com:klaghmari-group/akomytha.git` |
| GitHub | `github` → `github.com:klaghmari-github/acomytha.git` |

Chaque commit : `feat(F-XXX):` / `fix(F-XXX):` / `docs:`. **Les deux remotes** : `git push origin main && git push github main`. Puis fast-forward SSD (`git checkout --` des copies sales d’abord, jamais `gitpush.sh` sur un arbre sale).

Live : uvicorn **SSD** port **8787**, audio du worktree.

```bash
cd /media/laghmari/ssd-data/dev/akomytha
ACOMYTHA_AUDIO=/home/laghmari/.grok/worktrees/dev-akomytha/2026-09-03-696fa471/stories/audio \
PYTHONPATH=app python -m uvicorn acomytha.main:create_app --factory --host 127.0.0.1 --port 8787
```

Démo : `admin@acomytha.local` / `acomytha-admin` · `parent@acomytha.local` / `acomytha-parent` · PIN `2468`.  
`device_id` parent démo : `b150c5bf-0509-4746-a3e6-65da72cc5d5d`.

SQLite live : `/media/laghmari/ssd-data/dev/akomytha/app/data/acomytha.sqlite`.

Après promotion d’xlsx : importer.

```bash
cd /media/laghmari/ssd-data/dev/akomytha
PYTHONPATH=app python3 -c "
from acomytha.settings import Settings
from acomytha.db import Database
from acomytha.catalog import CatalogImporter
s=Settings(); db=Database(s)
with db.SessionLocal() as session:
    print(CatalogImporter(s).import_all(session))
"
```

`import_all` **supprime** les histoires dont l’xlsx n’est plus dans `stories/arbres/` (`_drop_missing_stories`). Live = ATOM + TREE promus seulement.

---

## 2. Chiffres (stables vs live)

Détail canonique : [`stories/CHIFFRES.md`](../stories/CHIFFRES.md).

**Corpus xlsx (stable)** : **1449** histoires = **685 ATOM** + **764 TREE**. **85** leçons, **13** thèmes, **44** sous-domaines. **1449 / 1449** ont une question. Âges : N1 404, N2 567, N3 478.

**Live `stories/arbres/` au gel** : **764** (685 ATOM + **79 TREE**). Archive : **685 TREE**. SQLite : 764 stories, 79 TREE, 10221 chunks, 85 leçons.

Live TREE : **AUT 44** + **COL 35** (famille COL entière). AUT-041–044 n’ont jamais existé.

Archive restante : DIF 73, EMO 115, FAM 39, JEU 37, LAN 21, REL 88, SAN 79, SEC 93, SOC 55, TMP 46, VIV 39.

**Vitrine** (D39, `HomeApp.js`) : **> 1400** histoires, **> 10** thèmes, **> 80** leçons. Pas les totaux exacts. Les exacts restent dans `CHIFFRES.md`.

Atomique : ~5 chunks, **1** `passage_question` parlée. Ramifiée : **86** chunks (1 début, 13 `transition_question`, 42 passage, 3 `passage_question`, 27 fins). 16 nœuds question, 13 à 3 options.

---

## 3. Décisions à ne pas réouvrir

Table : [`decisions/DECISIONS_APP.md`](decisions/DECISIONS_APP.md). Les plus utilisées :

| | |
| --- | --- |
| D16 | Troupe : Amir, Aniss, Sarah, Chouchou, Mila, Nino, Nina, Raphaël, Victorino, Victorina. 1 héros, au plus 1 autre enfant, papa/maman. |
| D17 | ≥ 3 min. |
| D18 | PIN 4 chiffres, les deux sens. |
| D19 | Interaction = questions. Ramification = un choix **change** la suite. N1 ramifié : **3 options** (D33). |
| D20 | Papa et maman parlent. Pas « papa sourit ». |
| D21 | Jouer **tous** les audio dans l’ordre. |
| D23 / D34 | Invité : 30 s puis popup. Parent non acheté : 30 s. Possédé / enfant : entier. Prix acm **après** login. |
| D25 | Monde d’abord, puis l’action. « Il était une fois » = exemple, pas un moule. |
| D26 | Monnaie **acm**, glyphe = logo. |
| D27 | `home_catalog_page_size` défaut 6. |
| D28 | h1 *Apprendre par l’histoire.* Kicker *AcoMytha : univers d’histoires ludiques et captivantes.* |
| D29 | `main` only. |
| D36 | Nuit / or hors vitrine aussi. |
| D37 | Vraie encapsulation OOP (`#private`). |
| D38 | Consignes récit = **tout** le catalogue. Pas seulement deux arbres. Texte d’abord, audio ensuite. |
| D39 | Vitrine en seuils (> 1400 / > 10 / > 80). |

Watchdog feedback : **éteint** (D32/D35). Scheduler `01a06d02db267852b90eec7fa4d9fa2e` annulé. Ne pas le relancer sauf demande explicite. Ingest manuel : skill `ingest-feedback-chatgpt`.

---

## 4. Qualité récit (ce qui compte vraiment)

Règles : [`stories/REWRITE.md`](../stories/REWRITE.md), F-NAR-008…018, `feedback_chatgpt/NOTES.md`, `f_04.txt`, `avis2.txt`.

**Interdit** : « on va apprendre », puces d’objets, « l’histoire est finie », « bravo / bon travail » en refrain, « j’ai dit le besoin », morale énoncée, leçon collée en récap, prénoms hors D16.

**Obligatoire** : situation + contexte → désir du héros (≠ la leçon) → petit imprévu → l’enfant agit → résolution → fin heureuse qui **tient la promesse du début**. Leçon **implicite**. Adultes parlent. `script` = `role|phrase` une phrase par ligne.

**Étalon (F-NAR-018, avis2)** : TREE-AUT-001 *Le bateau d’Amir et la rivière du jardin*. Reprendre la **logique**, pas les phrases (pas « capitaine / plic / volet jaune » partout). Un ramifié n’a pas 27 histoires distinctes si T1 ne change que l’accessoire.

Outil : `python3 stories/outils/rewrite_story.py dump|apply <ID>`. `apply` **promouvoit** archive → `stories/arbres/` (move). Helpers : `stories/rewrites/_lib.py` (`check`, `FORBIDDEN`, limites N1=10 / N2=15 / N3=16 mots/phrase).

Voix enfant : Amir Aniss Nino Raphaël Victorino → `enfant-m` ; Sarah Chouchou Mila Nina Victorina → `enfant-f`.

Piper CAST (`xlsx_to_audio.py`) : narrateur length 1.34 pitch 0.15 ; maman 1.28 ; papa 1.26 ; enfant-f siwis 1.40 pitch 1.0 ; enfant-m tom 1.40 pitch 1.15. Enfant pitch **≤ ~1.2** (sinon robot/chipmunk — *La gouttière de Raphaël*). `--sentence_silence` 0.38. Piper : `/home/laghmari/.local/bin/piper`. **Tuer un bake par PID, jamais `pkill -f xlsx_to_audio`.**

Audio **gitignoré** sauf `TREE-SEC-001/` et `ATOM-SAN.ALI.001-01/`.

---

## 5. Fait (dans git, au gel)

### Produit / app
- PWA FastAPI + front OOP (tokens / objects / components / shells).
- Catalogue paginé, aperçu 30 s, shop acm, PIN, jour/nuit.
- Icônes SVG soleil / lune (commit `f2230ed0`).
- Vitrine seuils `e4f34904`.
- Parent homepage sans login ; prix après login.

### Textes ATOM
- 685/685 réécrits une première fois (arcs, plus puces).
- Passe leçon **implicite** RAN / REG / EMO / FAM / REL / SEC / COL.
- `import_all` ne laisse plus les 764 TREE archive dans sqlite.

### Textes TREE live (79)
- AUT-001 **étalon** (avis1 + avis2 + example1) : *Le bateau d’Amir et la rivière du jardin*. T1 = préparer d’abord un objet, les trois partent ; 9 résolutions. Source `feedback_chatgpt/examples/example1/`. Audio local cuit (86 wav/mp3, gitignoré).
- AUT-002–040, 045–048 promus (qualité variable, pas tous au niveau avis2).
- COL-001 **réécrit avis2** : pomme qui s’échappe ; T3 = on ramasse / on attend / on invente ; plus « L’histoire est finie » (`b979be8a`).
- COL-002–006 : récits 86 nœuds, D16, leçon implicite.
- COL-007–035 : **promus** (`681223cb`). Refrains Bravo / bon travail / « l’histoire est finie » retirés. **Pas** encore une passe avis2 (obstacle + 9 aventures). Qualité inférieure à COL-001.

### ATOM cités par avis2 (texte, `b979be8a`)
- `ATOM-EMO.LEX.001-05` *Sarah et le dessin du soleil* — crayon cassé, attente de maman, une seule « je suis contente ».
- `ATOM-FAM.AID.001-01` *La boîte trop haute* — Chouchou **enfant-f**, va vers papa, le bateau **se termine** (voile). Plus de « j’ai dit le besoin ».

### Feedback ChatGPT
Tous les fichiers du dossier sont `done` dans `processed.json` (audit, exemple, f_04, avis1, avis2, html 24 Mo).

---

## 6. Pas fait (reprendre ici)

Ordre recommandé pour la session neuve :

1. **Lire** ce fichier + `stories/REWRITE.md` + `CHIFFRES.md` + `feedback_chatgpt/NOTES.md` + F-NAR-018.
2. **Ne pas** cuire l’audio des TREE archive avant le texte.
3. **Famille DIF** (73) : dumps `source.json` déjà extraits dans `stories/rewrites/TREE-DIF-*/`. 13 `merged.json` existent, **non appliqués**, qualité non validée avis2. Réécrire comme COL-001 (désir, obstacle, T3 qui change la suite), `apply`, importer, commit, dual-push, FF SSD.
4. Ensuite EMO (115), REL (88), SEC (93), SAN (79), SOC, TMP, FAM, VIV, JEU, LAN.
5. **Passe avis2 sur COL-007–035** et sur les AUT live hors 001 (gabarit encore possible).
6. **Passe ATOM gabarit** : avis2 a mesuré ~666 « En ce moment », ~550 « bravo ». Seuls 2 ATOM ont eu la passe auteur. Le catalogue ATOM reste majoritairement « leçon habillée ».
7. **Audio** : bake ATOM `--force` **arrêté** le 5 sept. Dernière ligne log `/tmp/akomytha-bake/all.log` : **`[27/686] ATOM-AUT.RAN.001-03`**. Relance **sans** `--force` pour sauter l’existant, **après** décision (les textes avis2 de Sarah / Chouchou / AUT-001 / COL-001 devront être recuits). Ne pas baker les TREE promus tant que l’ATOM n’est pas fini, sauf demande. Témoins git : `ATOM-SAN.ALI.001-01`, `TREE-SEC-001`.
8. **Commerce / ASR / hors-ligne / Stripe réel / FX F-AUD-007** : « pas maintenant » (`NOTES.md`).

ChatGPT proposait d’arrêter de produire et de ne garder que 20 titres. **Non** : D38, tout le catalogue. On hausse la barre, on ne réduit pas.

---

## 7. Fichiers de travail au gel

- Dumps `stories/rewrites/<ID>/source.json` : **1449** (tout le corpus). Les TREE encore en archive y sont, pour ne pas redumper.
- `merged.json` : ~780 (ATOM + TREE déjà réécrits). DIF : 13 merged **brouillons**.
- `stories/rewrites/REMAINING_TREE.txt` : liste d’IDs (périmée en tête : COL-033–035 sont **live**).
- Scripts `_write_tree_*.py`, `_gen_*.py`, `_lib.py` : atelier. `_lib.check` refuse les refrains et les prénoms hors troupe (**limites de mots** : matcher `\b` pour ne pas coincer sur « graines » / « fines »).
- `stories/arbres/TREE-AUT-010.xlsx` et `011` : des copies sales d’agents ont été **restaurées** sur HEAD avant gel. Les `merged.json` correspondants peuvent encore diverger : **ne pas apply** sans relecture.

---

## 8. Recette session neuve

```text
1. git fetch origin && git log -1 --oneline   # doit matcher origin et github
2. Lire gestion_projet/ETAT_REPRISE.md (ce fichier)
3. Lire stories/REWRITE.md, stories/CHIFFRES.md, gestion_projet/feedback_chatgpt/NOTES.md
4. Lire gestion_projet/decisions/DECISIONS_APP.md (D16, D29, D34, D38, D39)
5. Continuer au §6 point 3 (TREE-DIF), texte seulement
```

Commandes utiles :

```bash
python3 stories/outils/rewrite_story.py dump TREE-DIF-001
python3 stories/rewrites/_lib.py   # pas un CLI ; importer check depuis un _write_*.py
python3 stories/outils/watch_feedback_chatgpt.py scan
```

Frontend changé : copier JS/CSS/HTML vers le SSD **avant** de juger le live, puis commit worktree, dual-push, FF SSD.

---

## 9. Processus arrêtés au gel

| Processus | État |
| --- | --- |
| `xlsx_to_audio.py --force` PID 2467955 | **tué** (~27/686 ATOM-AUT.RAN.001-03) |
| uvicorn 8787 SSD PID 1376204 | laissé (démo), pas un chantier |
| Watchdog feedback / scheduler 30 min | **off** |
| Agents réécriture COL/DIF | arrêtés ; ne pas relancer de bake ni de vague sans relire §6 |

---

## 10. Où sont tes consignes et exemples (ne pas les chercher dans le chat)

On ne recopie pas tout ici. Une session neuve lit **ces fichiers** :

| Ce que tu as donné | Où c’est sauvé |
| --- | --- |
| Décisions D1–D39 (sans questionnaire) | `gestion_projet/decisions/DECISIONS_APP.md` |
| Citations fondateur (Constantin / Luca / Céline, « il était une fois », bravo, PIN, acm…) | `gestion_projet/decisions/ECHANGES.md` |
| Spec produit | `gestion_projet/specification/AcoMytha_Specification.md` |
| Git `main` only, `feat(F-XXX):` | `gestion_projet/consignes.txt` |
| Grille récit + étalon avis2 | `stories/REWRITE.md` |
| Chiffres exacts | `stories/CHIFFRES.md` |
| Backlog F-* développé / en cours / à faire | `gestion_projet/backlog/Features.md` |
| Audits ChatGPT + NOTES | `gestion_projet/feedback_chatgpt/` (`exemple.txt`, `exemple2.txt`, `f_04.txt`, `avis1.txt`, `avis2.txt`, `NOTES.md`) |
| Ce gel (fait / reste / commandes) | **ce fichier** |

## 11. Features : développé vs reste

**Développé (app, sur `main`)** : F-APP-001…008, F-ACC-001/003/004, F-SEC-002/003, F-PAR-001/002/003, F-ENF-001, F-ADM-004, F-PLY-001/002, F-PAY-001/002/003, F-AUD-002/004/006, F-DAT-001, F-TAX-001/002, F-NAR-002/007, F-NAR-017 (veille, actuellement **éteinte**).

**En cours (texte)** : F-NAR-008…016 et **F-NAR-018**. Règles posées. Appliqué à fond : TREE-AUT-001, TREE-COL-001, 2 ATOM cités par avis2. ATOM 685 : première réécriture + leçon implicite, **pas** encore tous au niveau étalon. TREE live 79 (AUT+COL) ; archive 685 à reprendre (prochain = DIF).

**À faire** : F-AUD-007 (SFX partout). F-AUD-005 partiel (bake ATOM arrêté à ~27/686). F-ACC-002 reporté (contredit 1 appareil).

**Pas maintenant** (NOTES) : clés Stripe **live** + HTTPS public (le Checkout **test** est dans `main`, F-PAY-001 / D40), ASR, hors-ligne, vente sans audio validé.

## 12. Hors git (volontaire)

| | |
| --- | --- |
| `stories/audio/**` | gitignoré sauf `TREE-SEC-001/` et `ATOM-SAN.ALI.001-01/`. Le bake local n’est **pas** sur GitLab/GitHub. |
| `app/data/acomytha.sqlite` | base live SSD, pas dans git. Réimportable depuis les xlsx. |
| 13 `TREE-DIF-00x/original.xlsx` | copies locales de l’archive déjà versionnée. Inutiles. |

## 13. Commits récents (repères)

| Hash | Quoi |
| --- | --- |
| `4fa95621` | Gel + dumps TREE archive + ce fichier |
| `e4f34904` | Vitrine > 1400 / > 10 / > 80 |
| `b979be8a` | avis2 : AUT-001, COL-001, 2 ATOM, F-NAR-018 |
| `681223cb` | TREE-COL-007 à 035 au catalogue |
| `40b0ac54` | `stories/CHIFFRES.md` totaux exacts |
| `f2230ed0` | Soleil / lune Jour-Nuit |
