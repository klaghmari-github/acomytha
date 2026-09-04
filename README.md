# AcoMytha

Forêt narrative **audio seulement** pour enfants de 3 à 6 ans. Le parent choisit les leçons / histoires. L’enfant écoute. Rien n’est généré pendant la lecture.

## Application web

```bash
PYTHONPATH=app python -m uvicorn acomytha.main:create_app --factory --host 127.0.0.1 --port 8787
```

Comptes locaux : voir [`app/README.md`](app/README.md). Architecture : [`gestion_projet/strategies/STRAT-005-application-web.md`](gestion_projet/strategies/STRAT-005-application-web.md).

## Corpus

Chiffres exacts : [`stories/CHIFFRES.md`](stories/CHIFFRES.md).

- **1449** histoires (685 atomiques + 764 ramifiées). **Toutes** ont une question.
- **85** leçons, **13** thèmes. Référentiel : `stories/referentiel/`
- Live : `stories/arbres/` (764 : 685 ATOM + 79 TREE). Archive ramifiée : `stories/archive/arbres/` (685).
- Audio témoin (stéréo 44100) : `stories/audio/ATOM-SAN.ALI.001-01/`, `TREE-SEC-001/`, `stories/TEST_SON.mp3`

## Projet

Cadrage dans [`gestion_projet/`](gestion_projet/). Git : une branche par feature, rebase, fast-forward `main`.
