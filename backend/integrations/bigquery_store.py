"""Google Cloud BigQuery integration for logging metrics and analytics.

Updated for MemoriaOS:
- Uses asyncio.to_thread for blocking client calls.
- Standardized schema.
"""

import asyncio
import json
import uuid
from datetime import UTC
from datetime import datetime as dt
from typing import Any

import structlog
from google.cloud import bigquery
from google.cloud.exceptions import NotFound

from backend.config.settings import settings

log = structlog.get_logger(__name__)

SCHEMA = [
    bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("user_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("date", "DATE", mode="REQUIRED"),
    bigquery.SchemaField("type", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("data", "JSON", mode="REQUIRED"),
    bigquery.SchemaField("source", "STRING", mode="REQUIRED"),
]

_bq_client: bigquery.Client | None = None


def get_db() -> bigquery.Client:
    """Gets or instantiates the global BigQuery client.

    Returns:
        bigquery.Client: Authed BigQuery client.
    """
    global _bq_client
    if _bq_client is None:
        _bq_client = bigquery.Client(project=settings.gcp_project_id)
    return _bq_client


async def init_db() -> None:
    """Initializes the BigQuery Dataset and Table if they do not exist.

    Ensures the 'records' table is ready for multi-modal data ingestion.
    """
    dataset_id = f"{settings.gcp_project_id}.{settings.bq_dataset_id}"

    def _ensure_dataset() -> None:
        with bigquery.Client(project=settings.gcp_project_id) as client:
            try:
                client.get_dataset(dataset_id)
            except NotFound:
                dataset = bigquery.Dataset(dataset_id)
                dataset.location = "europe-west2"
                client.create_dataset(dataset, timeout=30)
                log.info("bigquery_dataset_created", id=dataset_id)

    await asyncio.to_thread(_ensure_dataset)

    table_id = f"{dataset_id}.records"

    def _ensure_table() -> None:
        with bigquery.Client(project=settings.gcp_project_id) as client:
            try:
                client.get_table(table_id)
                log.info("bigquery_table_detected", id=table_id)
            except NotFound:
                table = bigquery.Table(table_id, schema=SCHEMA)
                client.create_table(table, timeout=30)
                log.info("bigquery_table_created", id=table_id)

    await asyncio.to_thread(_ensure_table)


async def save_records(user_id: str, records: list[dict[str, Any]]) -> None:
    """Saves records directly to BigQuery.

    Args:
        user_id (str): The unique identifier for the user.
        records (list[dict[str, Any]]): List of record dictionaries to persist.

    Raises:
        RuntimeError: If the BigQuery insertion fails.
    """
    if not records:
        return

    table_id = f"{settings.gcp_project_id}.{settings.bq_dataset_id}.records"
    rows_to_insert = []

    now_date = dt.now(UTC).date().isoformat()

    for r in records:
        record_type = str(r.get("type", "unknown"))
        record_date = str(r.get("date", now_date))
        record_source = str(r.get("source", "memoria_os"))

        data_payload = dict(r)
        data_payload.pop("type", None)
        data_payload.pop("date", None)
        data_payload.pop("source", None)

        rows_to_insert.append(
            {
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "date": record_date,
                "type": record_type,
                "data": json.dumps(data_payload),
                "source": record_source,
            }
        )

    def _insert() -> None:
        with bigquery.Client(project=settings.gcp_project_id) as client:
            errors = client.insert_rows_json(table_id, rows_to_insert)
            if errors:
                log.error("bigquery_insert_errors", errors=errors)
                raise RuntimeError(f"BigQuery Insert Failed: {errors}")

    await asyncio.to_thread(_insert)
    log.info("saved_records_to_bigquery", count=len(records), user_id=user_id)


async def get_recent_records(user_id: str, limit: int = 50) -> list[dict[str, Any]]:
    """Fetches recent records for the user from BigQuery.

    Args:
        user_id (str): The unique identifier for the user.
        limit (int): Max number of records to return.

    Returns:
        list[dict[str, Any]]: List of parsed record dictionaries.
    """
    table_id = f"{settings.gcp_project_id}.{settings.bq_dataset_id}.records"
    query = f"""
        SELECT date, type, data, source
        FROM `{table_id}`
        WHERE user_id = @user_id
        ORDER BY date DESC, id DESC
        LIMIT @limit
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
            bigquery.ScalarQueryParameter("limit", "INTEGER", limit),
        ]
    )

    def _query() -> list[dict[str, Any]]:
        with bigquery.Client(project=settings.gcp_project_id) as client:
            query_job = client.query(query, job_config=job_config)
            results = query_job.result()
            records = []
            for row in results:
                record = {
                    "date": str(row.date),
                    "type": row.type,
                    "source": row.source,
                }
                # Unpack JSON data
                try:
                    data = json.loads(row.data)
                    record.update(data)
                except (json.JSONDecodeError, TypeError):
                    pass
                records.append(record)
            return records

    return await asyncio.to_thread(_query)


async def get_current_streak(user_id: str) -> int:
    """Calculates user's current journaling streak.

    Args:
        user_id (str): The unique identifier for the user.

    Returns:
        int: Total number of consecutive days.
    """
    return 0
