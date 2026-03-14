"""ADK Tool for generating ambient audio using Google Cloud TTS."""

from typing import Any, Literal

import structlog

from backend.integrations.cloud_storage import upload_bytes
from backend.integrations.cloud_tts import synthesize_speech

log = structlog.get_logger(__name__)

MOOD_CONFIGS: dict[str, dict[str, Any]] = {
    "calm": {
        "text": (
            "<speak><prosody rate='slow' pitch='-2st'>"
            "Take a moment to breathe. Let the stillness surround you."
            "</prosody></speak>"
        ),
        "voice": "en-GB-Wavenet-B",
        "speaking_rate": 0.8,
    },
    "energetic": {
        "text": (
            "<speak><prosody rate='medium' pitch='+1st'>"
            "You have done something amazing today. Keep that energy going."
            "</prosody></speak>"
        ),
        "voice": "en-GB-Wavenet-A",
        "speaking_rate": 1.1,
    },
    "peaceful": {
        "text": (
            "<speak><prosody rate='slow' pitch='-1st'>"
            "The world is quiet now. Rest in this gentle moment."
            "</prosody></speak>"
        ),
        "voice": "en-GB-Wavenet-F",
        "speaking_rate": 0.75,
    },
    "warm": {
        "text": (
            "<speak><prosody rate='slow' pitch='low'>"
            "Sometimes the simplest moments hold the deepest meaning."
            "</prosody></speak>"
        ),
        "voice": "en-GB-Wavenet-D",
        "speaking_rate": 0.85,
    },
}


async def generate_audio_summary(
    mood: Literal["calm", "energetic", "peaceful", "warm"],
) -> str:
    """Generates a mood-appropriate ambient audio clip using Cloud TTS.

    Synthesizes speech from SSML templates and uploads the resulting MP3 to GCS.

    Args:
        mood: The emotional tone to use for the synthesized speech.

    Returns:
        The public GCS URL of the generated audio file.
    """
    config = MOOD_CONFIGS.get(mood, MOOD_CONFIGS["calm"])

    try:
        audio_content = await synthesize_speech(
            ssml=config["text"], voice_name=config["voice"], speaking_rate=config["speaking_rate"]
        )

        # Upload to GCS
        filename = f"audio/{mood}_{hash(audio_content) % 10000}.mp3"
        url = await upload_bytes(data=audio_content, filename=filename, content_type="audio/mpeg")

        return url
    except Exception as e:
        log.error("generate_audio_error", mood=mood, error=str(e))
        return f"Error generating audio: {e}"
