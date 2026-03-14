"""ADK Tool for querying historical data via Text2SQL on BigQuery."""

import asyncio
import json
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

import structlog
from google import genai
from google.cloud import bigquery
from google.genai import types
from pydantic import BaseModel, Field

from backend.config.settings import settings

log = structlog.get_logger(__name__)


class SQLQuery(BaseModel):
    """Generated SQL query with explanation."""

    query: str = Field(description="BigQuery Standard SQL SELECT query")
    explanation: str = Field(description="Brief explanation of what the query does")


SCHEMA_PROMPT = """
Table: `{project_id}.{dataset_id}.records`
Columns: id STRING, user_id STRING, date DATE, type STRING, data JSON, source STRING

Types and JSON fields:
- sleep: duration_hours, bedtime_hour, wake_hour, quality (1-10)
- exercise: exercise_type, duration_minutes, distance_km, intensity, body_parts
- meditation/cleaning/sitting/group_meditation: duration_minutes, datetime_logged
- habit: category, description
- tasks: task, priority (1-3)
- journal_note: note

Use JSON_EXTRACT_SCALAR(data, '$.field'). Cast before aggregation.
Filter test data: JSON_EXTRACT_SCALAR(data, '$.is_test') != 'true'
Today: {today}
"""


async def query_past_entries(question: str, user_id: str = "default") -> str:
    """Query historical wellness data using natural language."""
    client = genai.Client()
    bq_client = bigquery.Client(project=settings.gcp_project_id)

    today = datetime.now(ZoneInfo(settings.timezone)).strftime("%Y-%m-%d")
    prompt = SCHEMA_PROMPT.format(
        project_id=settings.gcp_project_id,
        dataset_id=settings.bq_dataset_id,
        today=today,
    )

    try:
        response = await client.aio.models.generate_content(
            model=settings.gemini_model,
            contents=[
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(
                            f"User ID: '{user_id}'. Generate BigQuery SQL for: {question}"
                        )
                    ],
                )
            ],
            config=types.GenerateContentConfig(
                system_instruction=prompt,
                response_schema=SQLQuery,
                response_mime_type="application/json",
            ),
        )

        sql_result = SQLQuery.model_validate_json(response.text)
        sql_query = sql_result.query

        if not sql_query.strip().upper().startswith("SELECT"):
            return "Error: Only SELECT queries are permitted."

        def _execute() -> list[dict[str, Any]]:
            job_config = bigquery.QueryJobConfig(
                maximum_bytes_billed=100 * 1024 * 1024  # 100MB safety limit
            )
            results = bq_client.query(sql_query, job_config=job_config).result()
            return [dict(row.items()) for row in results]

        rows = await asyncio.to_thread(_execute)
        if not rows:
            return "No matching records found."

        return json.dumps(rows[:20], indent=2, default=str)
    except Exception as e:
        log.error("query_bq_error", error=str(e))
        return f"Error querying past entries: {e}"
