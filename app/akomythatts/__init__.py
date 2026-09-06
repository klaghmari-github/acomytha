"""Moteur vocal AcoMythaTTS.

Classes qui collaborent
-----------------------
Settings             chemins et constantes
Utils                helpers globaux (slug, JSON, WAV, ffmpeg)
CharacterCatalogue   registre des empreintes
StoryParser          Excel / JSON → ParsedStory
CharacterDetector    locuteurs → CastMember + profil
Roster               index personnages × histoires
VoiceStudio          générer / enregistrer une empreinte
ReplicaBook          une WAV par réplique, réassemblage
ConversionQueue      JSON → WAV (travaux asynchrones)
CatalogueConverter   Excel atelier → JSON schema 2.0
TtsApp               façade pour l'éditeur AcoMytha (sans Flask)
WebApp               adaptateur HTTP du studio local
"""

from .app import TtsApp
from .settings import Settings
from .utils import Utils

__all__ = ["Settings", "TtsApp", "Utils"]
