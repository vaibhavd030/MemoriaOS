"""Google Cloud Text-to-Speech integration for MemoriaOS."""

import structlog
from google.cloud import texttospeech

log = structlog.get_logger(__name__)


async def synthesize_speech(ssml: str, voice_name: str, speaking_rate: float = 1.0) -> bytes:
    """Synthesizes speech from SSML using Google Cloud TTS.

    Args:
        ssml: Valid SSML string containing the text to speak.
        voice_name: The specific TTS voice ID (e.g., 'en-GB-Wavenet-B').
        speaking_rate: multiplier for the speed of speech (0.25 to 4.0).

    Returns:
        The raw MP3 audio bytes.
    """
    client = texttospeech.TextToSpeechAsyncClient()

    synthesis_input = texttospeech.SynthesisInput(ssml=ssml)

    # Extract language code from voice_name (e.g., en-GB-Wavenet-B -> en-GB)
    lang_code = "-".join(voice_name.split("-")[:2])

    voice = texttospeech.VoiceSelectionParams(language_code=lang_code, name=voice_name)

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3, speaking_rate=speaking_rate
    )

    response = await client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content
