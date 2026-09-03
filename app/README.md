# Application web Sentier

Forêt narrative audio : parent, enfant, admin. STRAT-005.

## Lancer

Depuis la racine du dépôt :

```bash
PYTHONPATH=app python -m uvicorn sentier.main:create_app --factory --host 127.0.0.1 --port 8787
```

Ouvrir http://127.0.0.1:8787

| Rôle | Adresse | Clé |
| --- | --- | --- |
| Parent | `parent@sentier.local` | `sentier-parent` |
| Admin | `admin@sentier.local` | `sentier-admin` |
| Enfant | depuis l’espace parent → Mode enfant | PIN `2468` |

Premier démarrage : import des xlsx `stories/arbres/` vers SQLite (`app/data/`, gitignoré).

## Tests

```bash
PYTHONPATH=app pytest -q app/tests
```

## Objets

- Python : `Settings`, `Database`, `CatalogImporter`, `StoryGraph`, `AudioVault`, `DeviceGuard`, `Bootstrap`
- JS : `Component`, `ApiClient`, `DeviceIdentity`, `CryptoPlayer`, `StoryEngine`, shells custom elements
- CSS : jetons + objets `.o-*` / `.c-*` / `.s-*`

Une clé d’accès ne peut lier **qu’un** `device_id`. Un deuxième appareil → alerte admin.
