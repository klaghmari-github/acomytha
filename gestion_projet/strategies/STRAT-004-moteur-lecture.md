# STRAT-004 — Moteur de lecture (jour, nuit, enchaînement, RAM)

**Référencé par :** `F-NAR-002`, `F-PLY-001` à `F-PLY-005`, `F-INT-001`, `F-NAR-005`.  
**IDs :** `STRAT-003`. **Blobs :** `STRAT-002`.

## 1. Boucle

```
cursor = CHK_T0000_P0000
prefetch(successeur_probable)
tant que cursor existe :
    decrypt_RAM(cursor)          # 1 chunk
    play(MP3)
    wipe(buffer)
    cursor = next(cursor, mode, réponse | timeout)
    prefetch(successeur_probable)
fin
```

Un seul chunk déchiffré **en lecture** + un seul **en préchargement**. Pas toute l’histoire en RAM.

`successeur_probable` : jour = on ne connaît pas encore la réponse → précharger la question suivante **et** l’option 1 (défaut). Nuit = on connaît le défaut → précharger ce passage.

## 2. Calcul du suivant

Voir règles `STRAT-003` §2. Si `chunk_link` existe pour `(chunk, intent)`, elle **gagne** sur la convention (questions d’écoute).

Timeout jour : `intent = timeout` → `default_option` (souvent 1).

Fichier / id absent ⇒ **fin propre** (pas d’exception enfant). Journal : `END_MISSING_NEXT` pour le parent.

## 3. Mode jour

`night_policy=auto_default` **ne s’applique pas** le jour : l’enfant choisit. (Bug corrigé : le JS traitait `auto_default` comme un skip de choix même en journée.)

1. Jouer `transition_question`.
2. Jouer `transition_option` 1..n avec pause **moteur** 400–600 ms (pas dans le MP3).
3. Ouvrir le micro / l’attente : **3 secondes** par défaut, réglable par le parent (1–8 s).
4. Option : **une** répétition de la question (`retry_prompt` ou le même TQ), puis encore 3 s.
5. Match → `P000k`. Wrong sur `listen_question` → `FKO` puis **même** suite (on ne traverse pas au rouge). Wrong sur un choix narratif : ne devrait pas arriver (toutes les options sont sûres) ; si reco foire → timeout / défaut.
6. Silence → défaut. L’histoire **n’attend jamais** indéfiniment.

## 4. Mode nuit

- `listen_question` + feedbacks : `night_policy=skip`.
- `transition_question` + options : `skip` ; le moteur enchaîne `P000{default_option}` **sans** poser la question.
- Voix : on a déjà baké **une** piste ; la baisse de volume / vitesse est un gain lecteur (–2 à –4 dB, speed 0,90–0,95), pas un second MP3.
- Pas de son brusque, pas de relance.

Le parent peut laisser le branchement **actif** la nuit (rare) : alors on pose la question une fois, délai court, défaut. Réglage profil : `night_skip_branch` (défaut : oui).

## 5. Reprise (`F-NAR-005`)

On stocke `story_id`, `chunk_id`, `position_ms` dans le MP3 **déjà déchiffré uniquement en session**. Au redémarrage : on re-déchiffre le chunk, on seek, courte remise en contexte si on était au milieu d’un `passage`. Jamais reprendre au milieu d’une `transition_question`.

## 6. Hors connexion

Catalogue SQLite + `chunks/*.chk` + clés dans le Keystore. Zéro réseau. `STRAT-002` §5.

## 7. Téléphones pauvres

Cible : 1 Go RAM, décodeur MP3 matériel. Budget : &lt; 2 Mo RAM audio, I/O séquentielle. Interdit : décoder toute l’histoire, unzip géant, SSTable mmap de WAV.
