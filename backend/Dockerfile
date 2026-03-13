FROM python:3.11-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
# Note: we are currently in the backend/ directory context during docker build
RUN uv sync --frozen --no-dev --no-install-project

FROM python:3.11-slim AS runtime
RUN groupadd -r appuser && useradd -r -g appuser appuser
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
COPY . ./backend/
# The backend structure is expected to be under 'backend/' package
# We also need to add an __init__.py if it doesn't exist to make it a package
RUN touch backend/__init__.py
USER appuser
ENV PORT=8080
EXPOSE $PORT
CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
