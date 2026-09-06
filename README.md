# AcoMytha

Forêt narrative **audio seulement** pour enfants de 3 à 6 ans. Le parent choisit les leçons / histoires. L’enfant écoute. Rien n’est généré pendant la lecture.

## Application web

**Un seul serveur** (FastAPI, port **8787**) : accueil, parent, enfant, admin, **éditeur vocal**. Pas de second processus TTS.

```bash
./start.sh
```

Ouvre http://127.0.0.1:8787. Le script utilise `.venv/` s’il existe, charge `.env` s’il est là. Port : `ACOMYTHA_PORT` (défaut 8787).

| Mode | Hash | Qui |
| --- | --- | --- |
| Accueil | `#/` | public |
| Parent | `#/parent` | parent / admin |
| Enfant | `#/enfant` | enfant (PIN) |
| Admin | `#/admin` | admin |
| Éditeur | `#/admin/editeur` | admin — JSON, empreintes, Excel→JSON→audio |

Comptes locaux et lancement Kokoro : [`app/README.md`](app/README.md). Architecture : [`STRAT-005`](gestion_projet/strategies/STRAT-005-application-web.md). Chaîne vocale : [`stories/FORMAT_JSON_TTS.md`](stories/FORMAT_JSON_TTS.md).

Branche de fusion TTS : **`AkoMythaTTS`**.

## Corpus

Chiffres exacts : [`stories/CHIFFRES.md`](stories/CHIFFRES.md).

- **1449** histoires (685 atomiques + 764 ramifiées). **Toutes** ont une question.
- **85** leçons, **13** thèmes. Référentiel : `stories/referentiel/`
- Live : `stories/arbres/` (764 : 685 ATOM + 79 TREE). Archive ramifiée : `stories/archive/arbres/` (685).
- Audio témoin (stéréo 44100) : `stories/audio/ATOM-SAN.ALI.001-01/`, `TREE-SEC-001/`, `stories/TEST_SON.mp3`

## Projet

Cadrage dans [`gestion_projet/`](gestion_projet/). Git : une branche par feature, rebase, fast-forward `main`.
