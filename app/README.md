# Application web AcoMytha

Forêt narrative audio : parent, enfant, admin, **éditeur vocal**. STRAT-005. Un processus, un port.

## Lancer

Depuis la racine du dépôt :

```bash
./start.sh
```

Équivalent : `PYTHONPATH=app python -m uvicorn acomytha.main:create_app --factory --host 127.0.0.1 --port 8787`

Ouvrir http://127.0.0.1:8787

**Un seul serveur** sert tous les modes : accueil, parent, enfant, admin, éditeur vocal (TTS). Plus de processus Flask séparé sur le port 8765.

| Rôle | Adresse | Clé | Espace |
| --- | --- | --- | --- |
| Parent | `parent@acomytha.local` | `acomytha-parent` | `#/parent` → `#/enfant` |
| Admin | `admin@acomytha.local` | `acomytha-admin` | `#/admin` → `#/admin/editeur` |
| Enfant | depuis l’espace parent → Mode enfant | PIN `2468` | `#/enfant` |

Pour la synthèse (Kokoro / OpenVoice), lancer avec le venv AkoMythaTTS :

```bash
TTS_PY=/media/laghmari/ssd-data/dev/AkoMythaTTS/.venv/bin/python
$TTS_PY -m pip install -r app/requirements.txt
PYTHONPATH=app $TTS_PY -m uvicorn acomytha.main:create_app --factory --host 127.0.0.1 --port 8787
```

## Éditeur vocal (branche `AkoMythaTTS`)

Même processus que le parent et l’enfant. Admin → **Éditeur** (`#/admin/editeur`).

| Action | Où |
| --- | --- |
| Vues personnages / histoires | troupe, API `GET /api/editor/roster` |
| Choisir un JSON | `stories/json/`, `GET /api/editor/stories`, `POST /api/editor/parse` |
| Excel → JSON | bouton *Excel → JSON*, `POST /api/editor/excel` (`stories/arbres/` → `stories/json/`) |
| Empreinte générer / enregistrer | modal Kokoro ou micro, `POST /api/editor/voices/generate` ou `…/record` |
| JSON → audio + répliques | *Convertir en audio*, `POST /api/editor/convert`, édition `GET /api/editor/jobs/{id}/edit` |

Façade Python (sans Flask) : `from akomythatts import TtsApp`. Registre : `stories/json/voice_registry.json`. WAV d’empreinte : `stories/voices/`. Jobs : `app/data/tts_jobs/` (gitignoré).

Objets TTS : `TtsApp`, `Utils`, `CharacterCatalogue`, `StoryParser`, `CharacterDetector`, `Roster`, `VoiceStudio`, `ReplicaBook`, `ConversionQueue`, `CatalogueConverter`. JS : `EditorApp`, `EditorApi`, `TroupeBoard`, `DropZone`, `CastBoard`, `VoicePanel`, `ConvertPanel`, `ReplicaStudio`, `MicRecorder`.

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

- Python : `Settings`, `Database`, `CatalogImporter`, `StoryGraph`, `AudioVault`, `DeviceGuard`, `Bootstrap`, `TtsApp`
- JS : `Component`, `ApiClient`, `DeviceIdentity`, `CryptoPlayer`, `StoryEngine`, `EditorApp`, shells custom elements
- CSS : jetons + objets `.o-*` / `.c-*` / `.s-*` (+ `editor.css` pour l’atelier vocal)

Une clé d’accès ne peut lier **qu’un** `device_id`. Un deuxième appareil → alerte admin.
