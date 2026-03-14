"""Google Cloud Storage integration for MemoriaOS."""

import asyncio

import structlog
from google.cloud import storage

from backend.config.settings import settings

log = structlog.get_logger(__name__)


async def upload_bytes(
    data: bytes, filename: str, content_type: str = "application/octet-stream"
) -> str:
    """Uploads arbitrary bytes to Google Cloud Storage.

    Args:
        data: The raw byte content to upload.
        filename: The destination path/name in the bucket.
        content_type: The MIME type for the uploaded object.

    Returns:
        The public URL of the uploaded object, or an empty string on failure.
    """
    if not settings.gcs_bucket_name:
        log.warning("gcs_bucket_not_configured")
        return ""

    client = storage.Client(project=settings.gcp_project_id)
    bucket = client.bucket(settings.gcs_bucket_name)
    blob = bucket.blob(filename)

    await asyncio.to_thread(blob.upload_from_string, data, content_type=content_type)

    # Return the public URL
    # Note: In production, you might want sign_url or a CDN
    url = f"https://storage.googleapis.com/{settings.gcs_bucket_name}/{filename}"
    log.info("file_uploaded_to_gcs", url=url)
    return url


async def list_files(prefix: str = "") -> list[dict[str, Any]]:
    """Lists files in the GCS bucket with a specific prefix.

    Args:
        prefix: The folder/prefix to filter by.

    Returns:
        List of dictionaries with name, url, and metadata.
    """
    if not settings.gcs_bucket_name:
        log.warning("gcs_bucket_not_configured")
        return []

    client = storage.Client(project=settings.gcp_project_id)
    bucket = client.bucket(settings.gcs_bucket_name)

    def _list() -> list[dict[str, Any]]:
        blobs = bucket.list_blobs(prefix=prefix)
        files = []
        for blob in blobs:
            files.append(
                {
                    "name": blob.name,
                    "url": f"https://storage.googleapis.com/{settings.gcs_bucket_name}/{blob.name}",
                    "size": blob.size,
                    "updated": str(blob.updated),
                }
            )
        return files

    return await asyncio.to_thread(_list)
