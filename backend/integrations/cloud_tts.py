"""Google Cloud Text-to-Speech integration for MemoriaOS."""

import structlog
from google.cloud import texttospeech
from backend.config.settings import settings

log = structlog.get_logger(__name__)

async def synthesize_speech(ssml: str, voice_name: str, speaking_rate: float = 1.0) -> bytes:
    """Synthesize speech using Cloud TTS WaveNet voices."""
    client = texttospeech.TextToSpeechAsyncClient()
    
    synthesis_input = texttospeech.SynthesisInput(ssml=ssml)
    
    # Extract language code from voice_name (e.g., en-GB-Wavenet-B -> en-GB)
    lang_code = "-".join(voice_name.split("-")[:2])
    
    voice = texttospeech.VoiceSelectionParams(
        language_code=lang_code,
        name=voice_name
    )
    
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=speaking_rate
    )
    
    response = await client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )
    
    return response.audio_content
