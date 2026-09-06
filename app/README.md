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

Installer les dépendances :

```bash
python -m pip install -r app/requirements.txt
```

## Paiement Stripe en mode test (F-PAY-001, D40)

La recharge du portefeuille utilise **Stripe Checkout hébergé**. Aucune donnée de carte ne
transite par AcoMytha et le portefeuille n'est crédité que par un webhook Stripe signé.
Il n'existe volontairement aucun bouton de validation de paiement simulé dans l'application.

1. Copier `.env.example` vers `.env` sans committer ce dernier.
2. Renseigner une clé secrète de test `sk_test_...` depuis le Dashboard Stripe.
3. Dans un second terminal, transmettre les webhooks Stripe vers l'application :

```bash
stripe listen --forward-to http://127.0.0.1:8787/api/shop/stripe/webhook
```

4. Copier le secret `whsec_...` affiché par Stripe CLI dans `STRIPE_WEBHOOK_SECRET`.
5. Exporter les variables puis lancer l'application (`Settings` lit `os.environ`, pas le fichier `.env` tout seul) :

```bash
set -a
source .env
set +a
PYTHONPATH=app python -m uvicorn acomytha.main:create_app --factory --host 127.0.0.1 --port 8787
```

La carte Stripe `4242 4242 4242 4242`, une date future et un CVC quelconque permettent
un paiement réussi en test. Utiliser exclusivement des cartes de test dans cet environnement.

Événements traités : `checkout.session.completed`,
`checkout.session.async_payment_succeeded`, `checkout.session.async_payment_failed` et
`checkout.session.expired`.

### Passage en production

Créer un endpoint webhook de production pointant vers
`https://<domaine>/api/shop/stripe/webhook`, puis remplacer uniquement les variables par
`sk_live_...`, le nouveau `whsec_...` et l'URL HTTPS publique. Aucun secret Stripe ne doit
être enregistré dans l'interface admin ou dans Git.

## Tests

```bash
python -m pip install -r app/requirements-dev.txt
PYTHONPATH=app pytest -q app/tests
```

## Objets

- Python : `Settings`, `Database`, `CatalogImporter`, `StoryGraph`, `AudioVault`, `DeviceGuard`, `Bootstrap`
- JS : `Component`, `ApiClient`, `DeviceIdentity`, `CryptoPlayer`, `StoryEngine`, shells custom elements
- CSS : jetons + objets `.o-*` / `.c-*` / `.s-*`

Une clé d’accès ne peut lier **qu’un** `device_id`. Un deuxième appareil → alerte admin.
