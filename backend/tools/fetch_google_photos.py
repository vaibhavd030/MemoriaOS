"""ADK Tool for fetching and analyzing recent Google Photos using Gemini Vision."""

import structlog
from google.genai import Client
from google.genai import types
from backend.integrations.google_photos import GooglePhotosClient
from backend.models.extracted_data import PhotoAnalysis
from backend.config.settings import settings

log = structlog.get_logger(__name__)

async def fetch_and_analyze_recent_photos(access_token: str, limit: int = 3) -> list[PhotoAnalysis]:
    """
    Fetch recent photos from Google Photos and analyze them using Gemini Vision.
    Returns a list of structured PhotoAnalysis objects.
    """
    gp_client = GooglePhotosClient(access_token)
    genai_client = Client(api_key=settings.google_api_key)
    
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
            
            # Call Gemini Vision
            response = genai_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    prompt,
                    types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=PhotoAnalysis,
                ),
            )
            
            if response.parsed:
                analysis = response.parsed
                # Add timestamp from Google Photos metadata if available
                metadata = item.get("mediaMetadata", {})
                analysis.timestamp = metadata.get("creationTime", "Unknown")
                analyses.append(analysis)
                
        return analyses
        
    except Exception as e:
        log.error("error_analyzing_photos", error=str(e))
        return []
    finally:
        await gp_client.close()
