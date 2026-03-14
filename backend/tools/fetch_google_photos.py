"""ADK Tool for fetching and analyzing recent Google Photos using Gemini Vision."""

import structlog
from google.genai import Client, types

from backend.config.settings import settings
from backend.integrations.google_photos import GooglePhotosClient
from backend.models.extracted_data import PhotoAnalysis

log = structlog.get_logger(__name__)


async def fetch_and_analyze_recent_photos(access_token: str, limit: int = 3) -> list[PhotoAnalysis]:
    """Fetches recent photos from Google Photos and analyzes them using Gemini Vision.

    Connects to the Google Photos API, downloads media, and performs visual
    analysis to extract structured context and metadata.

    Args:
        access_token: Valid OAuth2 access token with GPhotos scopes.
        limit: Maximum number of recent photos to process.

    Returns:
        A list of analyzed photo records.
    """
    gp_client = GooglePhotosClient(access_token)
    genai_client = Client(api_key=settings.google_api_key.get_secret_value())

    try:
        log.info("fetching_recent_photos", limit=limit)
        items = await gp_client.list_media_items(page_size=limit)

        if not items:
            log.info("no_photos_found")
            return []

        analyses = []
        for item in items:
            base_url = item.get("baseUrl")
            if not base_url:
                continue

            log.info("analyzing_photo", id=item.get("id"))

            # Download the photo bytes
            image_bytes = await gp_client.download_media(base_url)

            # Prepare the Vision prompt
            prompt = """Analyze this photo and provide structured details.
            Identify the location, activity, objects, mood, and any inferred context.
            Return the result as a structured PhotoAnalysis object."""

            # Call Gemini Vision asynchronously
            response = await genai_client.aio.models.generate_content(
                model="gemini-2.5-flash",
                contents=[prompt, types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=PhotoAnalysis,
                ),
            )

            if response.parsed:
                # Merge parsed data with timestamp from Google Photos metadata
                p_metadata = item.get("mediaMetadata", {})
                analysis_dict = response.parsed.model_dump()
                analysis_dict["timestamp"] = p_metadata.get("creationTime", "Unknown")

                analyses.append(PhotoAnalysis.model_validate(analysis_dict))

        return analyses

    except Exception as e:
        log.error("error_analyzing_photos", error=str(e))
        return []
    finally:
        await gp_client.close()
