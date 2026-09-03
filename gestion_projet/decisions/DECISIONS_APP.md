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
| D8 | Comptes démo | `admin@sentier.local` / `sentier-admin` · `parent@sentier.local` / `sentier-parent` · PIN `2468`. |
| D9 | F-APP-001 | Feature complexe : stories (socle, catalogue, auth, appareil, 3 UI, lecteur) sur **une** branche, commits par story. |
| D10 | F-AUD-006 | Plusieurs voix Piper par chunk (mix). Narrateur = Tom. Papa = Pierre. Maman = Siwis. Maîtresse = Jessica. Enfants = pitch ↑. Pas d’API TTS payante. F-AUD-003 (voix unique) abandonné. |
| D11 | F-AUD-007 | Immersion **générale** sur tout le corpus : chaque événement du récit a son bruit (assiette, parc, véhicule, chien… = exemples). Mix sous la voix au bake. Lexique extensible. |
