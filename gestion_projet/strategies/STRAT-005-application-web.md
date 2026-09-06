# STRAT-005 — Application web AcoMytha

**Référencé par :** `F-APP-001`, `F-ACC-001`, `F-SEC-002`, `F-SEC-003`, `F-ADM-004`, `F-PAR-001`, `F-ENF-001`, `F-AUD-004`, `F-PLY-001`, `F-PAY-001`.  
**Décisions datées :** 3 septembre 2026 (fondateur absent — prises et notées, pas de questionnaire).

## 1. Rôle du web

Le runtime **enfant cible** reste un téléphone hors-ligne (spec §9, STRAT-002).  
L’application web est le **premier client livrable** : catalogue, comptes, forêt parentale, lecture chiffrée, console admin. Android / iOS envelopperont les **mêmes classes JS** (WebView / Capacitor) plus tard. Pas de second front.

## 2. Pile (POO partout)

| Couche | Forme objet | Pourquoi |
| --- | --- | --- |
| HTML | *Custom Elements* (`HTMLElement`) | Chaque écran / carte / lecteur est une classe. Réutilisable dans une WebView native. |
| CSS | Jetons (`:root`) + objets BEM (`.o-*`, `.c-*`, `.s-*`) | Pas de framework CSS. Thèmes parent / admin / enfant = objets de jetons. |
| JS | ES modules + classes (`ApiClient`, `Router`, `StoryEngine`, `CryptoPlayer`, `DeviceIdentity`) | Zéro React/Vue : moins de dette pour l’APK. |
| Python | FastAPI + services / dépôts / modèles SQLAlchemy 2 | Un objet métier par concept (Compte, Appareil, Forêt, Graphe, CoffreAudio). |

## 3. Décisions produit

1. **Une clé d’accès = un appareil.** `F-ACC-002` (multi-appareils) est **reporté**. Un parent qui change de téléphone demande un *reset* admin. Motif : redistribution d’APK + même login.
2. **Enfant ≠ second appareil.** L’enfant est un *profil* sur l’appareil déjà lié au parent (PIN). Ça n’ouvre pas une deuxième liaison.
3. **Ping licence à chaque session.** Même si les `.chk` sont en cache, une session de lecture commence par `GET /api/me`. Pas de lecture anonyme.
4. **Déchiffrement en RAM seulement.** Web Crypto AES-GCM → `ArrayBuffer` → `Blob` révoqué après lecture. Jamais de MP3 en `localStorage` / IndexedDB.
5. **Catalogue SQL = source runtime.** Les xlsx restent l’atelier. Import au premier démarrage (`F-DAT-001`).
6. **Comptes de démo locaux** (changeables par env) : `admin@acomytha.local` / `acomytha-admin`, `parent@acomytha.local` / `acomytha-parent`, PIN enfant `2468`.
7. **Design parent, pas un décor.** Fond clair, accent bleu, pas de palette « arbre ». L’UI parent dit *histoires* / *sélection*, jamais forêt, arbre, clairière. Enfant : écran calme, cibles ≥ 64 px.
8. **Graphe joué côté client.** Le serveur envoie le graphe (sans texte enfant) + les blobs chiffrés. Le moteur JS applique jour / nuit / 3 s.

## 4. Anti-redistribution APK

```
login(email, secret, device_id)
  si pas de liaison     → bind(device_id)
  si device_id == lié   → session
  sinon                 → 409 + DeviceAlert (console admin)
```

`device_id` : UUID créé une fois (localStorage web, plus tard Keystore).  
Copier l’APK sans le compte ne sert à rien. Copier le compte sur un 2ᵉ téléphone : **alerte admin**, accès refusé.

Ce n’est pas une DRM studio. C’est le filet demandé (une clé, un appareil).

## 5. Routes UI

| Hash | Rôle | Contenu |
| --- | --- | --- |
| `#/entrer` | public | Connexion |
| `#/parent` | parent | Forêt, catalogue, filtres, préécoute |
| `#/enfant` | enfant | File d’histoires choisies, lecteur |
| `#/admin` | admin | Comptes, alertes appareil, corpus |

## 6. Fichiers

Code : `app/`. Données runtime gitignorées : `app/data/`. Stratégies audio / graphe inchangées (STRAT-002 à 004).

## 7. Paiement (F-PAY-001, D40)

Le parent n’achète pas en euros pièce par pièce : il **recharge des acm**, puis dépense le solde (F-PAY-002).

```
parent clique 10–50 €
  → POST /api/shop/recharge
  → Stripe Checkout Session (carte hors AcoMytha)
  → retour /#/parent?checkout=success|cancelled
  → Stripe POST /api/shop/stripe/webhook (signature)
  → crédit acm une fois (stripe_sessions.status = paid)
```

Sans `STRIPE_SECRET_KEY` **et** `STRIPE_WEBHOOK_SECRET` : pas de Checkout, pas de crédit. Live interdit si `ACOMYTHA_PUBLIC_URL` n’est pas `https://`. Les secrets ne sont plus des paramètres admin. Détail Features F-PAY-001 ; lancement : `app/README.md`.
