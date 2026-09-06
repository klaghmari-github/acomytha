# Dossier JSON généré (pas le manuscrit)

- **Contrat :** `../FORMAT_JSON_TTS.md` (F-NAR-024).
- **Source des histoires :** `../arbres/<story_id>.xlsx` (texte + prosodie).
- **Ici :** sortie du moteur, un fichier plat `<story_id>.json`, plus `voice_registry.json`. Pas de rapports (`conversion_report.json` → `poubelle/`).
- **Empreintes :** `../voices/` (chemins dans le registre).
- **Audio histoires :** `../audio/` (cible plate ; jobs d’atelier : `app/data/tts_jobs/`).
- **Éditeur :** `#/admin/editeur` liste ces JSON, convertit Excel → JSON, génère / enregistre les voix.
- **Échantillons ATOM** (schema 2.0) : `ATOM-AUT.AFF.*` et `ATOM-AUT.RAN.*`, plus `TREE-AUT-001.json`.
- **Pas utilisé :** le bundle `AkoMythaTTS-catalogue-tts.bundle`.
- On n’écrit pas les histoires ici. Qualité = Excel d’abord.
