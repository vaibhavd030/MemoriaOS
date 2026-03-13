"""Google Cloud Storage integration for MemoriaOS."""

import structlog
from google.cloud import storage
from backend.config.settings import settings

log = structlog.get_logger(__name__)

async def upload_bytes(data: bytes, filename: str, content_type: str = "application/octet-stream") -> str:
    """Upload bytes to GCS and return the public URL."""
    if not settings.gcs_bucket_name:
        log.warning("gcs_bucket_not_configured")
        return ""
    
    client = storage.Client(project=settings.gcp_project_id)
    bucket = client.bucket(settings.gcs_bucket_name)
    blob = bucket.blob(filename)
    
    blob.upload_from_string(data, content_type=content_type)
    
    # Return the public URL
    # Note: In production, you might want sign_url or a CDN
    url = f"https://storage.googleapis.com/{settings.gcs_bucket_name}/{filename}"
    log.info("file_uploaded_to_gcs", url=url)
    return url
