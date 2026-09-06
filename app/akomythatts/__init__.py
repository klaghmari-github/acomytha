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
TtsApp               façade unique (éditeur AcoMytha, même processus FastAPI)
WebApp               ancien adaptateur Flask du studio autonome (ne plus lancer)
"""

from .app import TtsApp
from .settings import Settings
from .utils import Utils

__all__ = ["Settings", "TtsApp", "Utils"]
