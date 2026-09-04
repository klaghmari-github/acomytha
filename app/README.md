# Application web AcoMytha

Forêt narrative audio : parent, enfant, admin. STRAT-005.

## Lancer

Depuis la racine du dépôt :

```bash
PYTHONPATH=app python -m uvicorn acomytha.main:create_app --factory --host 127.0.0.1 --port 8787
```

Ouvrir http://127.0.0.1:8787

| Rôle | Adresse | Clé |
| --- | --- | --- |
| Parent | `parent@acomytha.local` | `acomytha-parent` |
| Admin | `admin@acomytha.local` | `acomytha-admin` |
| Enfant | depuis l’espace parent → Mode enfant | PIN `2468` |

Premier démarrage : import des xlsx `stories/arbres/` vers SQLite (`app/data/`, gitignoré).

Stripe (optionnel) : `pip install stripe`, clés `STRIPE_SECRET_KEY` / `STRIPE_PUBLISHABLE_KEY` ou paramètres admin.

## Tests

```bash
PYTHONPATH=app pytest -q app/tests
```

## Objets

- Python : `Settings`, `Database`, `CatalogImporter`, `StoryGraph`, `AudioVault`, `DeviceGuard`, `Bootstrap`
- JS : `Component`, `ApiClient`, `DeviceIdentity`, `CryptoPlayer`, `StoryEngine`, shells custom elements
- CSS : jetons + objets `.o-*` / `.c-*` / `.s-*`

Une clé d’accès ne peut lier **qu’un** `device_id`. Un deuxième appareil → alerte admin.
