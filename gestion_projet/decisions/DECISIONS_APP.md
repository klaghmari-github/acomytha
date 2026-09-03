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
| D8 | Comptes démo | `admin@acomytha.local` / `acomytha-admin` · `parent@acomytha.local` / `acomytha-parent` · PIN `2468`. |
| D9 | F-APP-001 | Feature complexe : stories (socle, catalogue, auth, appareil, 3 UI, lecteur) sur **une** branche, commits par story. |
| D10 | F-AUD-006 | Plusieurs voix Piper par chunk (mix). Narrateur = Tom. Papa = Pierre. Maman = Siwis. Maîtresse = Jessica. Enfants = pitch ↑. Pas d’API TTS payante. F-AUD-003 (voix unique) abandonné. |
| D11 | F-AUD-007 | Immersion **générale**. Colonne `sons` (vide = silence). Ordre : bruit seul, puis récit au calme. Jamais parler dans le bruit, jamais nappe sur tout le passage. |
| D12 | F-NAR-008 | Reconstruire les textes autour d’un fil rouge. L’xlsx n’est touché qu’après fusion d’agents. Passe 2 : fusion **éditoriale** (un moment par chunk, 3–6 ans, leçon vécue en fin). Le merge « plus long gagne » recolle un cours : on ne s’en sert pas comme vérité. |
| D13 | Marque | Le produit s’appelle **AcoMytha**. « Sentier » est retiré de l’UI, du code, des docs et des comptes démo. |
| D14 | UI parent | Pas de métaphore forêt/arbre dans l’UI. Histoires, sélection, interaction, ramifications. Palette claire, accent bleu. |
| D15 | Vitrine + A | Accueil public, inscription e-mail/mdp, aperçu 10 s (non affiché). Pas « gratuitement », pas pastille Courte, pas âge sur les cartes. |
| D16 | Troupe enfant | Amir, Aniss, Sarah, Chouchou, Mila, Nino, Nina, Raphaël, Victorino, Victorina. Pas d’autre prénom d’enfant. Une histoire = 1 héros, au plus 1 autre enfant, papa/maman. |
| D17 | Durée | Histoire ≥ 3 min. Plusieurs passages ; certains portent une leçon. Atomique : plusieurs leçons possibles pour tenir 3 min. Allonger si le récit le demande. |
| D18 | PIN | 4 chiffres, modifiable par le parent. Même code pour entrer en mode enfant et en sortir. |
| D19 | Libellés | Interaction = questions. Ramifications = lance d’autres histoires (liens + pop-up vitrine). |
