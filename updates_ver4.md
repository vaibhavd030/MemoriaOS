# MemoriaOS: Final Audit + Operational Guide

**Repository:** github.com/vaibhavd030/MemoriaOS  
**Latest Commit:** `12b3bf6` (7 commits total)  
**Audit Date:** 14 March 2026

---

## 1. Final Readiness Score

| Dimension | Score | Notes |
|-----------|-------|-------|
| Backend Architecture | **87%** | 5-step SequentialAgent, Extractor wired with `extract.txt`, all bugs from previous audit resolved |
| Frontend | **74%** | SSE streaming, AudioPlayer, WaveformVisualizer, live data on all pages. 1 bug remaining. |
| Infrastructure | **85%** | Terraform complete with IAM, CORS, outputs, Scheduler. Deploy script passes vars. |
| Hackathon Rubric | **72%** | Only GCP deployment proof + demo video remain |
| Innovation | **68%** | Cinematic SSE + waveform + AudioPlayer all live |
| **Overall** | **78%** | **+5 points from last audit. 2 small bugs left, then deploy + record.** |

---

## 2. Remaining Issues (2 Items)

### ISSUE 1: `reels/page.tsx` Missing `"use client"` Directive

The Reels page uses `useState`, `useEffect`, and `motion` but does not have `"use client"` as its first line. Next.js will throw a server component error.

**Fix:** Add `"use client";` as the very first line of `frontend/src/app/reels/page.tsx`.

### ISSUE 2: GCS Bucket Has CORS but No Public Read IAM

The Terraform adds CORS to the GCS bucket (good), but generated images, audio, and reels served from GCS will return 403 because there is no public read permission. The bucket uses `uniform_bucket_level_access = true` so object ACLs do not apply.

**Fix:** Add to `infra/main.tf`:
```hcl
resource "google_storage_bucket_iam_member" "public_read" {
  bucket = google_storage_bucket.media.name
  role   = "roles/storage.objectViewer"
  member = "allUsers"
}
```

### ADVISORY: Live API Model String

The WebSocket endpoint uses `gemini-2.0-flash-exp` which is deprecated (shutdown June 2026). For the hackathon demo this will still work. For production, upgrade to `gemini-2.5-flash-native-audio`. Not blocking submission.

---

## 3. How to Run the Project Locally

### 3.1 Prerequisites

```bash
# Python 3.11+
python3 --version  # Must be 3.11 or higher

# Node.js 18+
node --version  # Must be 18 or higher

# uv (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Google Cloud CLI
gcloud --version  # Install from https://cloud.google.com/sdk/docs/install

# Google API Key
# Get one from https://aistudio.google.com/apikey
```

### 3.2 Clone and Configure

```bash
git clone https://github.com/vaibhavd030/MemoriaOS.git
cd MemoriaOS

# Create environment file
cp .env.example .env
```

Edit `.env` with your actual values:
```env
GCP_PROJECT_ID=your-gcp-project-id
GOOGLE_API_KEY=your-gemini-api-key
BQ_DATASET_ID=memoria_os_prod
GCS_BUCKET_NAME=your-project-id-memoria-media
ENABLE_NOTION=false
NOTION_API_KEY=
NOTION_WELLNESS_PAGE_ID=
TIMEZONE=Europe/London
LOG_FORMAT=console
NEXT_PUBLIC_API_URL=http://localhost:8080
```

### 3.3 Start the Backend

```bash
cd backend

# Install dependencies
uv sync

# Authenticate with GCP (needed for BigQuery, GCS, TTS)
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID

# Start the API server
uv run uvicorn backend.main:app --host 0.0.0.0 --port 8080 --reload
```

Verify it works:
```bash
curl http://localhost:8080/health
# Expected: {"status":"healthy"}
```

### 3.4 Start the Frontend

Open a new terminal:
```bash
cd frontend

# Install dependencies
npm install

# Start the dev server
npm run dev
```

Open **http://localhost:3000** in your browser. You should see the MemoriaOS PWA with the animated mic orb.

### 3.5 Using the Application

**Storyteller Mode (Write tab):**
1. Type a message in the input field, e.g. "I'm feeling burnt out today. The presentation went okay but I feel like I'm not making progress."
2. Press Enter or tap the Send button
3. Watch the cinematic SSE reveal: text streams in, then a watercolour image fades in, then ambient audio starts playing

**UI Navigator Mode (Snap):**
1. Tap the camera icon next to the input field
2. Select a screenshot of a recipe, receipt, or workout plan
3. The UISnipperAgent will extract structured data and display it as cards

**Live Agent Mode (Mic):**
1. Tap the animated mic orb at the centre of the home screen
2. Grant microphone permission when prompted
3. The waveform visualiser activates and reacts to your voice
4. Speak naturally. The Live API processes your audio in real-time.

**Journal Page:**
- Navigate to the Journal tab to see your logged memories fetched from BigQuery

**Reels Page:**
- Navigate to Reels to see generated weekly memory reel videos from GCS

**Vault Page:**
- Navigate to Vault to see counts of media, structured data, and narrative logs from GCS

### 3.6 Running with Docker Compose (Alternative)

```bash
# From the repo root
cp .env.example .env
# Fill in .env values

docker compose up --build

# Backend: http://localhost:8080
# Frontend: http://localhost:3000
```

---

## 4. How to Deploy to Google Cloud

### 4.1 One-Time GCP Setup

```bash
# Set your project
export GCP_PROJECT_ID=your-project-id
gcloud config set project $GCP_PROJECT_ID

# Enable required APIs
gcloud services enable \
  run.googleapis.com \
  bigquery.googleapis.com \
  storage.googleapis.com \
  aiplatform.googleapis.com \
  texttospeech.googleapis.com \
  cloudscheduler.googleapis.com \
  secretmanager.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  cloudtrace.googleapis.com

# Grant Cloud Build permission to deploy to Cloud Run
gcloud projects add-iam-policy-binding $GCP_PROJECT_ID \
  --member="serviceAccount:$(gcloud projects describe $GCP_PROJECT_ID --format='value(projectNumber)')@cloudbuild.gserviceaccount.com" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding $GCP_PROJECT_ID \
  --member="serviceAccount:$(gcloud projects describe $GCP_PROJECT_ID --format='value(projectNumber)')@cloudbuild.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"
```

### 4.2 Deploy with Terraform (Infrastructure)

```bash
cd infra

# Initialize Terraform
terraform init

# Preview what will be created
terraform plan \
  -var="project_id=$GCP_PROJECT_ID" \
  -var="google_api_key=YOUR_GEMINI_API_KEY" \
  -var="notion_api_key=YOUR_NOTION_KEY"

# Apply infrastructure
terraform apply \
  -var="project_id=$GCP_PROJECT_ID" \
  -var="google_api_key=YOUR_GEMINI_API_KEY" \
  -var="notion_api_key=YOUR_NOTION_KEY"

# Note the outputs:
# backend_url  = "https://memoria-os-backend-xxxxx-nw.a.run.app"
# frontend_url = "https://memoria-os-frontend-xxxxx-nw.a.run.app"
# memory_bucket_name = "your-project-id-memoria-media"
```

### 4.3 Deploy with Cloud Build (Application Code)

```bash
# From the repo root
cd ..

# Build and deploy both backend and frontend
gcloud builds submit --config cloudbuild.yaml .

# This will:
# 1. Build backend Docker image and push to Artifact Registry
# 2. Build frontend Docker image and push to Artifact Registry
# 3. Deploy backend to Cloud Run
# 4. Deploy frontend to Cloud Run
```

### 4.4 Or Use the One-Command Script

```bash
# Set environment variables first
export GCP_PROJECT_ID=your-project-id
export GOOGLE_API_KEY=your-gemini-api-key
export NOTION_API_KEY=your-notion-key

# Run the deployment
chmod +x deploy.sh
./deploy.sh
```

### 4.5 Verify Deployment

```bash
# Get the backend URL from Terraform output
cd infra && terraform output backend_url

# Test health check
curl https://memoria-os-backend-xxxxx-nw.a.run.app/health
# Expected: {"status":"healthy"}

# Test chat endpoint
curl -X POST https://memoria-os-backend-xxxxx-nw.a.run.app/api/chat \
  -F "message=Hello, how are you?" \
  -F "user_id=demo"
# Expected: {"response":[{"type":"text","content":"..."}],"status":"success"}

# Open the frontend
open $(cd infra && terraform output -raw frontend_url)
```

---

## 5. How to Record GCP Deployment Proof

The hackathon requires a screen recording proving the backend runs on Google Cloud. Here is exactly what to capture:

### 5.1 Cloud Run Console Recording (30 seconds)

1. Open **https://console.cloud.google.com/run** in your browser
2. Start screen recording (QuickTime on Mac, OBS on Windows/Linux)
3. Click on `memoria-os-backend` service
4. Show the **Service Details** page (URL, region, container image, revision)
5. Click on the **Logs** tab
6. In another browser tab, send a chat message via the frontend
7. Switch back to Cloud Run console and show the live log entries appearing:
   ```
   chat_request_received message="I'm feeling burnt out" user_id="demo"
   ```
8. Stop recording

### 5.2 Alternative: Code-Based Proof

If you prefer a code link instead of a recording, point judges to these files:
- `cloudbuild.yaml` (lines showing `gcloud run deploy memoria-os-backend`)
- `infra/main.tf` (lines showing `google_cloud_run_v2_service`)
- `backend/Dockerfile` (container definition)
- `infra/outputs.tf` (Cloud Run URLs as Terraform outputs)

---

## 6. How to Use the Deployed Project

Once deployed, share the frontend URL with anyone:

```
https://memoria-os-frontend-xxxxx-nw.a.run.app
```

### User Journey

1. **Open the PWA** on mobile or desktop. On mobile, tap "Add to Home Screen" for the installable PWA experience.

2. **Write a memory:** Type "Had an amazing gym session today. Chest and triceps for 45 minutes. Feeling energised but also craving pizza."
   - The cinematic SSE stream shows: narrative text, then a watercolour image, then ambient audio plays
   - Behind the scenes: the Extractor agent pulls out ExerciseEntry (weights, 45 min, chest + triceps) and HabitEntry (junk_food craving)
   - Data is persisted to BigQuery and synced to Notion

3. **Snap a screenshot:** Upload a photo of a recipe from Instagram
   - The UISnipperAgent uses Gemini Vision to parse the pixels
   - A structured RecipeCard appears with title, ingredients, steps, and tags
   - Synced to the Knowledge Vault in Notion

4. **Start a live session:** Tap the mic orb and speak freely
   - The waveform visualiser reacts to your voice in real-time
   - Gemini Live API processes your stream and responds with audio

5. **Check your journal:** Navigate to the Journal tab to see all logged entries from BigQuery

6. **Watch your reel:** Navigate to Reels to see weekly video summaries (hover to preview)

7. **Browse the vault:** Navigate to Vault to see counts of all your stored media and data

---

## 7. Architecture Summary for Judges

| Component | Technology | Purpose |
|-----------|------------|---------|
| Frontend | Next.js 16 + Tailwind CSS + Framer Motion | PWA with glassmorphism UI, SSE streaming, WebSocket live voice |
| Backend API | FastAPI + Google ADK | Multi-agent orchestration with 6 specialised agents |
| LLM | Gemini 2.5 Flash + Flash Image Preview | Text, vision, and native image generation |
| Live Voice | Gemini Live API (WebSocket) | Real-time bidirectional audio |
| Storage | Google BigQuery | Structured life data with Text2SQL queries |
| Media | Google Cloud Storage | Images, audio, video reels |
| Sync | Notion API | Human-readable dashboards for all entity types |
| Audio | Google Cloud TTS (WaveNet) | 4 mood profiles with SSML |
| Video | FFmpeg (async subprocess) | Weekly Memory Reel compilation |
| Photos | Google Photos Library API + Gemini Vision | Automatic photo analysis and journal enrichment |
| IaC | Terraform | Cloud Run, BigQuery, GCS, Secret Manager, Scheduler, IAM |
| CI/CD | Cloud Build | Docker build, push, deploy pipeline |
| Observability | structlog + OpenTelemetry | JSON structured logging, distributed tracing |

**Agent Architecture:**
- **SupervisorAgent** (LlmAgent) routes to 5 sub-agents
- **MemoryWeaverAgent** (SequentialAgent) chains 5 steps: Context Retriever → Narrative Generator → Extractor → Audio Generator → Persister
- **UISnipperAgent** (LlmAgent) with Gemini Vision + Notion sync tools
- **QueryAgent** (LlmAgent) with Text2SQL BigQuery tool
- **LoopAgent** (LoopAgent) with Clarifier + Validator, max 3 iterations
- **ReelGeneratorAgent** (LlmAgent) with BigQuery + FFmpeg tools

**Data Models:** 15+ Pydantic v2 models covering sleep, exercise, 4 spiritual practices, habits, recipes, expenses, workouts, tasks, reading links, photo analysis, and journal notes.

---

## 8. What Remains (2.5 hours to complete submission)

| Task | Time | Priority |
|------|------|----------|
| Fix `reels/page.tsx`: add `"use client"` as first line | 2 min | Must fix |
| Add GCS public read IAM to `infra/main.tf` | 5 min | Must fix for media display |
| Deploy to Cloud Run | 1.5 hrs | Mandatory |
| Record GCP deployment proof (30s screen recording) | 15 min | Mandatory |
| Record 4-min demo video | 45 min | Mandatory |
| **Total** | **~2.5 hrs** | |

After these 2.5 hours, the submission is complete.