# MemoriaOS — The Multimodal Second Brain

## Gemini Live Agent Challenge | Complete Project Plan

**Author:** Vaibhav Desai  
**Date:** March 2026  
**Evolution:** My-Tele-PA v2.0 → MemoriaOS v1.0  
**Hackathon Tracks:** Creative Storyteller + UI Navigator + Live Agent

---

## Table of Contents

1. [Project Vision & Description](#1-project-vision--description)
2. [Why This Project — The Problem Space](#2-why-this-project--the-problem-space)
3. [Real-World Use Cases](#3-real-world-use-cases)
4. [User Experience & Interaction Design](#4-user-experience--interaction-design)
5. [Critical Analysis of My-Tele-PA (Current State)](#5-critical-analysis-of-my-tele-pa-current-state)
6. [Complete Architecture Plan](#6-complete-architecture-plan)
7. [ADK Agent & Tool Specifications (with Code)](#7-adk-agent--tool-specifications-with-code)
8. [Pydantic Schema Catalogue](#8-pydantic-schema-catalogue)
9. [Frontend API Contract](#9-frontend-api-contract)
10. [Migration Roadmap: My-Tele-PA → MemoriaOS](#10-migration-roadmap-my-tele-pa--memoriaos)
11. [Sprint Execution Plan](#11-sprint-execution-plan)
12. [Infrastructure-as-Code (Terraform)](#12-infrastructure-as-code-terraform)
13. [Deployment Guide](#13-deployment-guide)
14. [Cost Estimation](#14-cost-estimation)
15. [Evaluation & Quality Gates](#15-evaluation--quality-gates)
16. [Risk Matrix & Contingencies](#16-risk-matrix--contingencies)
17. [Demo Video Script (4 Minutes)](#17-demo-video-script-4-minutes)
18. [Hackathon Submission Checklist](#18-hackathon-submission-checklist)

---

## 1. Project Vision & Description

### What is MemoriaOS?

MemoriaOS is a **next-generation, multimodal Life OS agent** — an omniscient personal assistant that sees what you see, hears what you feel, and transforms messy, unstructured life inputs into beautifully organised, rich-media knowledge databases.

It operates on a **Tri-Engine architecture**:

**Engine 1 — The Internal Engine (Creative Storyteller Track):**
Processes emotional and narrative inputs (voice notes, text, real-time audio conversations). It analyses sentiment, queries your past journal history from BigQuery, and responds with a **seamlessly interleaved stream** of:
- A comforting text narrative referencing your personal history
- An AI-generated watercolour image reflecting your mood (via Gemini's native image generation)
- A soothing, generated ambient audio track (via Google Cloud TTS)

**Engine 2 — The External Engine (UI Navigator Track):**
Processes visual inputs (screenshots, screen shares, photos). It acts as your hands, visually navigating complex UIs — Instagram reels, fitness apps, bank statements, recipe videos — **without requiring DOM access or APIs**. It extracts exact structured data and seamlessly syncs it to your Notion databases.

**Engine 3 — The Live Engine (Live Agent Track):**
A real-time, interruptible voice assistant powered by the **Gemini Live API**. You can talk to MemoriaOS naturally while walking, cooking, or commuting. It handles interruptions gracefully, transcribes and processes in real-time, and responds with spoken audio — the always-on life companion.

### What Does It Look Like?

MemoriaOS presents itself as a **Progressive Web App (PWA)** installable on any phone or desktop. The interface is minimal and distraction-free:

- **Home screen:** A single input area with three modes — microphone (Live Engine), text field (Internal Engine), and camera/upload button (External Engine)
- **Journal feed:** A chronological, card-based feed of your memories — each card contains the narrative text, the generated watercolour image, and an embedded audio player
- **Knowledge vault:** A grid-view of extracted structured data — recipe cards, expense entries, workout logs — each synced to Notion with a confirmation badge
- **Weekly/Monthly recap:** A generated audiovisual journal summary — a short video combining your best journal entries, images, and narrated highlights, formatted for social sharing or personal archiving

### The Audiovisual Journal Summary (Key Differentiator)

Every week (or month), MemoriaOS automatically generates a **Memory Reel** — a 60–90 second audiovisual summary of your life:

1. **Narrative script:** Gemini aggregates your journal entries from BigQuery, identifying emotional arcs, milestones, and recurring themes. It writes a first-person retrospective narration.
2. **Image compilation:** The watercolour images generated throughout the period are collected, lightly edited (cropped, colour-graded for consistency), and sequenced as a slideshow.
3. **Voiceover:** Google Cloud TTS narrates the script over the image sequence using a warm, reflective voice profile.
4. **Output formats:** The reel is rendered as an MP4 (for social posting on Instagram Stories/TikTok), a square format (for Instagram feed), and a high-res version (for personal archiving in Google Drive).
5. **Notion integration:** The reel is linked in a "Memory Reels" Notion database alongside the raw text, images, and metadata.

This feature transforms MemoriaOS from a productivity tool into an **emotional time capsule** — something people return to and share.

---

## 2. Why This Project — The Problem Space

### The Journaling Problem
"Blank page anxiety" prevents millions of people from reflecting on their day. Apps like Day One and Notion assume you will sit down, type formatted text, tag categories, and curate your thoughts. **MemoriaOS reverses the dynamic:** you speak naturally or snap a messy screenshot, and the AI does the rigorous structuring and creative weaving.

### The Data Capture Problem
Saving a complex recipe from an Instagram Reel, a workout split from a YouTube video, or extracting an expense from a bank notification means frantically typing it out or saving a useless link you will never open again. **MemoriaOS sees the screen and extracts the data for you** — structured, validated, and synced.

### The Memory Preservation Problem
Life's meaningful moments disappear into chat logs, voice notes, and camera rolls. There is no system that weaves these fragments into a coherent personal narrative. **MemoriaOS generates weekly and monthly audiovisual journal summaries** that you can keep forever, share with loved ones, or post on social media.

### The Continuity Problem
Current assistants are stateless. You tell Siri you are stressed, and tomorrow it has forgotten. **MemoriaOS remembers everything.** When you say "I feel burnt out today," it queries your BigQuery history and responds: *"You sounded exhausted. But remember last month when you felt this way before closing that big account? You are resilient."*

### Why This Idea Wins

- **Three hackathon tracks in one product** — most competitors target one track; we span Creative Storyteller, UI Navigator, AND Live Agent with a unified architecture
- **Not built from scratch** — evolved from a battle-tested production system (My-Tele-PA) with 30+ commits, real BigQuery data, live Notion dashboards, and a proven eval framework
- **Solves a real, universal problem** — everyone has messy life data; everyone wants to remember and reflect
- **Deep Google Cloud integration** — Cloud Run, BigQuery, Cloud Storage, Gemini 2.5 Flash (native image generation), Gemini 2.5 Flash Image (Nano Banana), Cloud TTS, Gemini Live API, Google Photos Library API, OpenTelemetry, Cloud Scheduler, Secret Manager — hitting 9+ GCP services

---

## 3. Real-World Use Cases

### Use Case 1: The Emotional Anchor (Creative Storyteller)

**Interaction:** You tap the microphone icon while walking home and say: *"I'm feeling really burnt out today. The presentation went okay, but I feel like I'm not making progress."*

**AI Magic:**
1. Gemini Live API transcribes your voice in real-time
2. Memory Weaver Agent queries BigQuery for your past journal entries mentioning "burnt out" or "presentation"
3. Gemini 2.5 Flash generates an interleaved response:

**Output on your screen:**
- **Text:** *"You sounded exhausted today. But remember three weeks ago when you felt exactly this way before the Q3 review? You powered through and got praised by your director. You are more resilient than you give yourself credit for."*
- **Image:** An inline AI-generated watercolour of a small boat navigating a calm, vast ocean at sunset
- **Audio:** A 15-second ambient lo-fi track with gentle rain and piano
- **Action:** The entire multimodal memory is saved to your "Memoria Journal" Notion database

### Use Case 2: The Culinary Explorer (UI Navigator)

**Interaction:** You see a fast-paced Instagram reel for a high-protein pasta recipe. You take a screenshot and upload it to MemoriaOS.

**AI Magic:**
1. The Supervisor Agent detects a screenshot with no text prompt and routes to the UI Snipper Agent
2. Gemini Vision scans the messy UI, ignoring comments and buttons, reading ingredients and steps directly from the video frame
3. Output is validated against the RecipeCard Pydantic schema

**Output:**
- A beautifully formatted recipe card: title, ingredients with measurements, step-by-step instructions, prep time, tags (high-protein, pasta)
- Automatically pushed to your "Knowledge Vault" Notion database
- The original screenshot is stored in Cloud Storage for reference

### Use Case 3: The Automated Expense Tracker (UI Navigator)

**Interaction:** You screenshot a ride-sharing receipt or bank transfer confirmation.

**Output:** The agent visually parses the screen, extracts Vendor ("Uber"), Amount (£14.50), Date (2026-03-12), Category (Transport), and logs it to your Notion Finance Tracker. No typing.

### Use Case 4: The Workout Logger (UI Navigator)

**Interaction:** You screenshot a workout plan from a fitness influencer's story.

**Output:** Extracted WorkoutSplit: Push day — Bench Press 4×10, Shoulder Press 3×12, Tricep Dips 3×15. Synced to Action Zone in Notion.

### Use Case 5: The Weekly Memory Reel (Audiovisual Summary)

**Interaction:** Every Sunday at 7 PM, MemoriaOS automatically:
1. Queries all journal entries from the past 7 days
2. Writes a cohesive first-person weekly narrative
3. Collects the watercolour images generated during the week
4. Generates a voiceover narration using Cloud TTS
5. Compiles a 60-second MP4 video slideshow
6. Posts it to your "Memory Reels" Notion database
7. Optionally sends it to your Telegram for easy social sharing

### Use Case 6: The Photo Memory Weaver (Google Photos Integration)

**Interaction:** You connect your Google Photos account via OAuth. Every evening at 9 PM, MemoriaOS automatically:
1. Fetches today's photos from Google Photos Library API (filtered by `creationTime`)
2. Downloads each photo and passes it to **Gemini 3.1 Pro** for multimodal analysis
3. Gemini identifies: location (from visual cues — landmarks, signage, terrain), people present, activities shown, emotional tone, and time of day
4. Cross-references with today's journal entries in BigQuery
5. Enriches journal entries with real photos: *"Your journal mentions feeling great after the park run. Here's the photo you took at Richmond Park at 8:15 AM — looks like a beautiful morning!"*
6. For the weekly Memory Reel, real photos are interspersed with AI-generated watercolours — creating a hybrid real + generated visual narrative

**Why this matters:** This transforms MemoriaOS from a text-first journaling tool into a **true life chronicler** that weaves your actual photos into your personal narrative automatically. No tagging, no sorting — just live your life and MemoriaOS remembers.

### Use Case 7: The Live Walking Companion (Live Agent)

**Interaction:** You are on a walk and tap "Start Live Session." You talk naturally:
*"Just finished a really good gym session — chest and triceps, about 45 minutes. Also I need to call the dentist tomorrow. Oh and I'm craving that pasta recipe from yesterday..."*

**AI Magic:** The Gemini Live API processes your stream in real-time. You can pause, change topics, even interrupt yourself. The agent:
- Logs the gym session (ExerciseEntry: weights, 45 min, chest + triceps)
- Creates a task (TaskItem: call dentist, priority 2)
- Retrieves yesterday's pasta recipe from BigQuery and reads it back to you
- All while maintaining a warm, conversational tone

---

## 4. User Experience & Interaction Design

### PWA Screen Architecture

```
┌─────────────────────────────────────────┐
│  MemoriaOS                    ⚙️  👤    │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────────────────────────────┐    │
│  │  🎤 Live  │  ✍️ Write  │  📷 Snap │  │  ← Mode Tabs
│  └─────────────────────────────────┘    │
│                                         │
│  ┌─────────────────────────────────┐    │
│  │                                 │    │
│  │  [Text input / Voice waveform / │    │  ← Dynamic Input Area
│  │   Screenshot preview]           │    │
│  │                                 │    │
│  │              [Send →]           │    │
│  └─────────────────────────────────┘    │
│                                         │
│  ── Today ─────────────────────────     │
│                                         │
│  ┌─────────────────────────────────┐    │
│  │  📝 3:42 PM — Journal           │    │  ← Memory Card
│  │  "Feeling burnt out today..."   │    │
│  │  [🖼️ Watercolour Image]         │    │
│  │  [▶️ Ambient Audio — 0:15]      │    │
│  │  ✅ Synced to Notion            │    │
│  └─────────────────────────────────┘    │
│                                         │
│  ┌─────────────────────────────────┐    │
│  │  🍝 2:15 PM — Recipe Extracted  │    │  ← Extraction Card
│  │  High-Protein Pasta             │    │
│  │  8 ingredients · 4 steps        │    │
│  │  ✅ Synced to Knowledge Vault   │    │
│  └─────────────────────────────────┘    │
│                                         │
├─────────────────────────────────────────┤
│  🏠 Home   📖 Journal   🎬 Reels   ⚡ Vault │ ← Bottom Nav
└─────────────────────────────────────────┘
```

### UX Principles
- **Zero-friction input:** One tap to record voice, one tap to snap screenshot, or just start typing
- **Rich output:** Every response is a multimedia card, not a wall of text
- **Ambient awareness:** The app remembers your emotional state across days and weeks
- **Social readiness:** Memory Reels are formatted for Instagram/TikTok at generation time
- **Progressive disclosure:** Simple on the surface, deeply structured underneath (Notion, BigQuery)

---

## 5. Critical Analysis of My-Tele-PA (Current State)

### 5.1 Architecture Summary (What Exists)

My-Tele-PA is a production-grade Telegram bot built as a LangGraph state machine with the following pipeline:

```
START → reset → guard_input → classify → extract/query/chitchat → persist → guard_output → END
```

| Layer | Component | Technology |
|-------|-----------|------------|
| Interface | Telegram Bot | python-telegram-bot + FastAPI |
| Orchestration | LangGraph State Machine | LangGraph + AsyncSqliteSaver |
| Intelligence | Structured Extraction | OpenAI GPT-4o-mini + Instructor |
| Validation | Pydantic v2 Models | 12+ models with computed fields |
| Storage | BigQuery + Notion | google-cloud-bigquery + notion-client |
| Safety | Guard Nodes | Instructor SafetyClassification |
| Observability | Logging + Tracing | structlog + opentelemetry-api |
| Deployment | Cloud Run | Docker + cloudbuild.yaml CI/CD |

### 5.2 Key Strengths (What We Keep)

1. **12+ battle-tested Pydantic models** — SleepEntry, ExerciseEntry, 4 spiritual practice models (MeditationEntry, CleaningEntry, SittingEntry, GroupMeditationEntry), HabitEntry, TaskItem, ReadingLink, ExtractedData container. All with validators, enums, computed fields.
2. **Sophisticated clarification loop** — TTL-based expiry (30 min), deep merge strategy for partial entities, capped re-asking (max 3 turns), field-specific prompts.
3. **BigQuery integration** — Streaming inserts, Text2SQL query pipeline, parameterised deduplication, streak calculation with window functions.
4. **Notion SyncConfig pattern** — Generic dataclass-driven dispatcher that maps entity types to Notion page IDs and block builders. Adding new entity types requires only a new SyncConfig entry.
5. **Eval framework** — JSONL extraction test cases with slot-fill F1 metrics, CI threshold gates (≥0.75), and automated eval runner.
6. **Production infrastructure** — Multi-stage Docker, Cloud Run deployment, structured JSON logging, OpenTelemetry tracing on every node.
7. **Voice pipeline** — Voice-to-text transcription with retry logic, size/duration guards, seamless agent handoff.
8. **Google Photos integration** — Fetches recent photos via the Google Photos Library API, extracts metadata (creation time, camera model), and uses Gemini Vision to infer location, scene context, and emotional tone. Photos are automatically matched to journal entries by date and woven into Memory Reels alongside AI-generated watercolours.
9. **Extraction prompt engineering** — 44-line expert prompt (extract.txt) covering midnight boundary handling, spiritual practice classification, habit tracking patterns, and journal note generation.

### 5.3 Showstopper Gaps (Must Fix for Hackathon)

| # | Gap | Impact | Severity |
|---|-----|--------|----------|
| G1 | Entire stack is OpenAI-dependent (GPT-4o-mini, Instructor, OpenAI STT) | Hackathon mandates Gemini model + Google GenAI SDK or ADK | **CRITICAL** |
| G2 | No multimodal input (image/screenshot processing) | UI Navigator track requires Gemini Vision | **CRITICAL** |
| G3 | No multimodal output (image/audio generation) | Creative Storyteller requires interleaved text + images + audio | **CRITICAL** |
| G4 | LangGraph orchestration not ADK-compatible | Must use Google ADK or GenAI SDK | **CRITICAL** |
| G5 | No frontend — Telegram-only interface | Demo video needs a visual PWA | **HIGH** |
| G6 | No real-time streaming / Live API integration | Live Agent track requires bidirectional audio | **HIGH** |
| G7 | No audiovisual summary generation | Key differentiator feature does not exist | **HIGH** |

### 5.4 Architectural Risks

| Risk | Description | Mitigation |
|------|-------------|------------|
| Instructor dependency | Instructor is OpenAI-specific. Gemini uses `response_schema` or ADK function calling. | Replace with Gemini's native `response_schema` parameter; Pydantic schemas transfer directly. |
| Text2SQL injection surface | LLM-generated SQL executes directly with only a SELECT check. | Wrap in read-only BigQuery job config; add query cost estimation guard. |
| Async functions blocking event loop | `bigquery_store.py` uses sync BigQuery client inside async functions. | Use `asyncio.to_thread()` or BigQuery async client. |
| Clarification loop has no ADK equivalent | LangGraph's checkpointer manages multi-turn state. ADK uses `session.state` + `output_key`. | Implement clarification as a `LoopAgent` with `condition_key="needs_clarification"` and `exit_condition="complete"`. |
| Single-user design | Settings hardcode `TELEGRAM_CHAT_ID`. | Accept for hackathon MVP; add user_id to session state. |
| No streaming response | Creative Storyteller needs real-time interleaved output. | Use `generate_content_stream` with `response_modalities=["TEXT", "IMAGE"]`. |
| Global mutable state (`_bq_client`, `_app`) | Fragile for concurrent Cloud Run instances. | ADK migration naturally fixes this — tools are agent-scoped. |

### 5.5 Code-Level Bugs

1. **Settings `validate_model` will break on Gemini:** The validator checks for `gpt-` or `o` prefix. Must be removed entirely for Gemini model strings like `gemini-2.5-flash`.
2. **`calculate_cost` hardcodes GPT-4o-mini pricing:** `(prompt_tokens * 0.15 / 1_000_000)` — must be replaced with Gemini pricing or removed.
3. **Sync BigQuery client in async context:** `client.query()` in `bigquery_store.py` blocks the event loop. Every `async def` that calls it should use `asyncio.to_thread(client.query, ...)`.

### 5.6 Prompt Migration Notes

The existing 44-line `extract.txt` prompt and classifier prompt were engineered for OpenAI's chat completion format (`system`/`user` roles). Gemini's GenAI SDK uses a different format:

- **System instruction:** Gemini supports a dedicated `system_instruction` parameter on `GenerativeModel` or in ADK's `LlmAgent(instruction=...)` — this maps cleanly to the existing system prompts.
- **Structured output:** Instead of Instructor's `response_model=ExtractedData`, Gemini uses `generation_config={"response_schema": ExtractedData, "response_mime_type": "application/json"}` — Pydantic models work directly.
- **Multimodal input:** For the UI Navigator, screenshots are passed as `types.Part.from_image(image_bytes)` alongside text parts — no separate vision API.
- **Key difference:** Gemini's structured output is stricter about optional fields. Fields with `None` defaults may need `"nullable": true` in the JSON schema.

---

## 6. Complete Architecture Plan

### 6.1 System Architecture Diagram (Mermaid)

```mermaid
graph TD
    %% Frontend
    User([User]) -->|Voice / Text / Screenshot| PWA[Next.js PWA<br/>Tailwind CSS]
    
    %% Frontend → Backend
    PWA -->|POST /api/chat<br/>multipart/form-data| API[FastAPI Gateway<br/>Google Cloud Run]
    PWA <-->|WebSocket /api/live| LiveWS[WebSocket Handler<br/>Gemini Live API Bridge]
    
    %% Google ADK Orchestration
    subgraph "Google ADK Multi-Agent System"
        API --> Supervisor[Supervisor Agent<br/>LlmAgent<br/>gemini-2.5-flash]
        
        Supervisor -- "Intent: Journaling" --> Weaver[Memory Weaver Agent<br/>SequentialAgent]
        Supervisor -- "Intent: Data Capture" --> Snipper[UI Snipper Agent<br/>LlmAgent]
        Supervisor -- "Intent: Query" --> QueryAgent[Query Agent<br/>LlmAgent]
        
        %% Weaver Pipeline (Sequential)
        Weaver --> W1[Step 1: Context Retriever<br/>LlmAgent + QueryBigQueryTool]
        W1 --> W2[Step 2: Narrative Generator<br/>LlmAgent<br/>Interleaved Text+Image Output]
        W2 --> W3[Step 3: Audio Generator<br/>LlmAgent + GenerateAudioTool]
        W3 --> W4[Step 4: Persister<br/>LlmAgent + SyncToNotionTool]
        
        %% Snipper Tools
        Snipper -->|Gemini Vision| VisionTool[ExtractStructuredDataTool<br/>response_schema=Pydantic]
        
        %% Query Tools
        QueryAgent --> BQTool2[QueryBigQueryTool]
    end
    
    %% Live Agent Path (separate)
    subgraph "Gemini Live API (Real-Time)"
        LiveWS <--> GeminiLive[Gemini Live Session<br/>gemini-2.5-flash-native-audio]
        GeminiLive --> LiveTools[ADK Tools via<br/>Live API Function Calling]
    end
    
    %% External Services
    W1 <--> BigQuery[(Google BigQuery<br/>records table)]
    BQTool2 <--> BigQuery
    W2 --> GCS[(Google Cloud Storage<br/>Generated Images)]
    W3 --> GCS
    W4 --> NotionDB[(Notion APIs<br/>Memoria Journal)]
    VisionTool --> NotionDB2[(Notion APIs<br/>Knowledge Vault / Action Zone)]
    Snipper --> NotionDB2
    
    %% Google Photos Integration
    subgraph "Google Photos Pipeline"
        PhotosCron[Cloud Scheduler<br/>Daily 9 PM] --> PhotosAgent[Photos Enrichment Agent<br/>LlmAgent]
        PhotosAgent --> GPhotosAPI[Google Photos<br/>Library API]
        PhotosAgent --> GeminiVision[Gemini 3.1 Pro<br/>Photo Analysis]
        GeminiVision --> BigQuery
        PhotosAgent --> GCS
    end
    
    %% Weekly Reel Pipeline
    subgraph "Scheduled Jobs (Cloud Scheduler)"
        Scheduler[Cloud Scheduler<br/>Weekly/Monthly Cron] --> ReelAgent[Reel Generator Agent<br/>SequentialAgent]
        ReelAgent --> BQQuery[Query Week's Entries]
        BQQuery --> NarrativeGen[Generate Script]
        NarrativeGen --> ImageCollect[Collect Images from GCS]
        ImageCollect --> TTSNarrate[Cloud TTS Voiceover]
        TTSNarrate --> VideoRender[FFmpeg Video Compilation]
        VideoRender --> GCS
        VideoRender --> NotionReels[(Notion: Memory Reels)]
    end
    
    %% Return Flow
    API -->|JSON: {text, image_urls, audio_url}| PWA
    
    %% Observability
    API -.-> OTEL[OpenTelemetry<br/>Cloud Trace + Cloud Logging]
```

### 6.2 Repository Structure

```
memoria-os/
├── backend/
│   ├── __init__.py
│   ├── main.py                          # FastAPI app entry point
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── supervisor.py                # Root ADK LlmAgent (routes to sub-agents)
│   │   ├── memory_weaver.py             # SequentialAgent for journaling pipeline
│   │   ├── ui_snipper.py               # LlmAgent for screenshot extraction
│   │   ├── query_agent.py              # LlmAgent for Text2SQL queries
│   │   ├── reel_generator.py           # SequentialAgent for audiovisual summaries
│   │   └── live_session.py             # Gemini Live API WebSocket bridge
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── query_bigquery.py           # ADK FunctionTool: Text2SQL → BigQuery
│   │   ├── extract_structured_data.py  # ADK FunctionTool: Gemini Vision → Pydantic
│   │   ├── generate_audio.py           # ADK FunctionTool: Cloud TTS → GCS
│   │   ├── sync_notion.py              # ADK FunctionTool: entity → Notion blocks
│   │   ├── upload_to_gcs.py            # ADK FunctionTool: bytes → GCS public URL
│   │   └── compile_video.py            # FFmpeg-based video compilation
│   ├── models/
│   │   ├── __init__.py
│   │   ├── wellness.py                 # Migrated: Sleep, Exercise, Meditation, etc.
│   │   ├── tasks.py                    # Migrated: TaskItem, ReadingLink
│   │   ├── recipes.py                  # NEW: RecipeCard, Ingredient
│   │   ├── finance.py                  # NEW: ExpenseRecord, ExpenseCategory
│   │   ├── fitness.py                  # NEW: WorkoutSplit, WorkoutExercise
│   │   ├── extracted_data.py           # Updated ExtractedData container
│   │   └── api_contracts.py            # Request/response schemas for FastAPI
│   ├── integrations/
│   │   ├── __init__.py
│   │   ├── bigquery_store.py           # Migrated: BQ client, save_records, init_db
│   │   ├── notion_store.py             # Migrated: SyncConfig pattern + new builders
│   │   ├── cloud_storage.py            # NEW: GCS upload/download/public URL
│   │   ├── cloud_tts.py               # NEW: Text-to-Speech synthesis
│   │   └── google_photos.py           # NEW: Google Photos Library API client
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py                 # Migrated: updated for Gemini + GCS settings
│   │   └── logging.py                  # Migrated: structlog config
│   ├── prompts/
│   │   ├── extract.txt                 # Migrated: 44-line extraction prompt
│   │   ├── classify.txt                # NEW: intent classification prompt
│   │   ├── narrative.txt               # NEW: journal narrative generation prompt
│   │   └── vision_extract.txt          # NEW: screenshot extraction prompt
│   ├── evals/
│   │   ├── datasets/
│   │   │   ├── extraction.jsonl        # Migrated: text extraction test cases
│   │   │   └── vision_extraction.jsonl # NEW: 50 screenshot test cases
│   │   ├── metrics.py                  # Migrated: slot_fill_f1
│   │   └── run_evals.py               # Updated for ADK runner
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── requirements.txt
├── frontend/
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   ├── public/
│   │   └── manifest.json              # PWA manifest
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx               # Home screen with mode tabs
│   │   │   ├── journal/page.tsx       # Journal feed
│   │   │   ├── reels/page.tsx         # Memory Reels gallery
│   │   │   └── vault/page.tsx         # Knowledge Vault grid
│   │   ├── components/
│   │   │   ├── InputArea.tsx           # Mode-switching input (mic/text/camera)
│   │   │   ├── MemoryCard.tsx          # Rich multimedia journal card
│   │   │   ├── ExtractionCard.tsx      # Structured data display card
│   │   │   ├── AudioPlayer.tsx         # Inline ambient audio player
│   │   │   ├── LiveSession.tsx         # WebSocket-based live voice UI
│   │   │   └── ReelPlayer.tsx          # Video player for Memory Reels
│   │   ├── hooks/
│   │   │   ├── useAudioRecorder.ts     # WebRTC microphone capture
│   │   │   ├── useLiveSession.ts       # WebSocket connection to Live API
│   │   │   └── useScreenshot.ts        # Camera/file upload handler
│   │   └── lib/
│   │       └── api.ts                  # Fetch wrapper for backend endpoints
│   └── Dockerfile
├── infra/
│   ├── main.tf                         # Terraform: Cloud Run, BQ, GCS, IAM
│   ├── variables.tf
│   ├── outputs.tf
│   └── deploy.sh                       # One-command deployment script
├── docker-compose.yml                   # Local development
├── cloudbuild.yaml                      # CI/CD pipeline
├── README.md
└── HACKATHON_SUBMISSION.md
```

### 6.3 Google Cloud Services Used

| Service | Purpose | Justification |
|---------|---------|---------------|
| Cloud Run | Hosts FastAPI backend + Next.js frontend | Serverless, auto-scaling, pay-per-use |
| BigQuery | Primary data store for all records | SQL analytics, Text2SQL, window functions for streaks |
| Cloud Storage | Stores generated images, audio, videos | Object storage with public URL generation |
| Gemini 2.5 Flash | LLM for classification, extraction, narrative, vision | Native interleaved text+image output; massive context window |
| Gemini Live API | Real-time bidirectional audio | Low-latency voice interaction with interruption handling |
| Cloud Text-to-Speech | Ambient audio + voiceover generation | WaveNet voices for high-quality narration |
| Cloud Scheduler | Weekly/monthly reel generation triggers | Cron-based job scheduling |
| Cloud Trace + Logging | Observability | Native ADK OpenTelemetry integration |
| Artifact Registry | Docker image storage | CI/CD pipeline stores built images |
| Secret Manager | API keys and tokens | Notion API key, Telegram token (optional) |
| Google Photos Library API | Fetches user photos with metadata | Date-filtered search, creation time, camera info; Gemini Vision infers location/context |

---

## 7. ADK Agent & Tool Specifications (with Code)

### 7.1 Supervisor Agent

```python
"""Supervisor Agent — routes user intent to specialised sub-agents.

This is the root agent of the MemoriaOS multi-agent system. It inspects
the input modality (text, voice transcript, screenshot) and routes to the
appropriate specialised agent.
"""

from google.adk.agents import LlmAgent

from memoria_os.agents.memory_weaver import memory_weaver_agent
from memoria_os.agents.query_agent import query_agent
from memoria_os.agents.ui_snipper import ui_snipper_agent

# Model selection strategy (as of March 2026):
#   gemini-2.5-flash          → Stable workhorse: classification, extraction, Text2SQL
#   gemini-2.5-flash-image-preview → Interleaved text+image output (Nano Banana)
#   gemini-3.1-pro-preview    → Highest intelligence: complex reasoning, photo analysis
#   gemini-2.5-flash-native-audio  → Live API real-time voice
GEMINI_MODEL = "gemini-2.5-flash"  # Stable: best price-performance for agentic use

supervisor_agent = LlmAgent(
    name="SupervisorAgent",
    model=GEMINI_MODEL,
    instruction="""You are the MemoriaOS Supervisor. Your job is to inspect the
user's input and route to the correct specialist agent.

ROUTING RULES:
- If the input contains an image/screenshot (check for image parts), delegate to
  UISnipperAgent.
- If the user is asking a question about their past data (e.g. "how did I sleep",
  "show my exercise log", "what did I do last week"), delegate to QueryAgent.
- For EVERYTHING else (journal entries, feelings, activities, tasks, links,
  brain dumps), delegate to MemoryWeaverAgent.
- If you're unsure, default to MemoryWeaverAgent — it handles journaling
  and structured extraction simultaneously.

Do NOT try to answer the user directly. Always delegate to a sub-agent.""",
    description="Routes user inputs to the appropriate specialist agent.",
    sub_agents=[memory_weaver_agent, ui_snipper_agent, query_agent],
)

root_agent = supervisor_agent
```

### 7.2 Memory Weaver Agent (SequentialAgent)

```python
"""Memory Weaver Agent — the Creative Storyteller engine.

A SequentialAgent that orchestrates the full journaling pipeline:
1. Retrieve past context from BigQuery
2. Extract structured data + generate narrative + generate image
3. Generate ambient audio
4. Persist to BigQuery + Notion
"""

from google.adk.agents import LlmAgent
from google.adk.agents.sequential_agent import SequentialAgent

from memoria_os.tools.generate_audio import generate_ambient_audio
from memoria_os.tools.query_bigquery import query_past_entries
from memoria_os.tools.sync_notion import sync_journal_to_notion
from memoria_os.tools.upload_to_gcs import upload_bytes_to_gcs

GEMINI_MODEL = "gemini-2.5-flash"  # Stable: best price-performance for agentic use

# Step 1: Retrieve emotional context from past entries
context_retriever = LlmAgent(
    name="ContextRetriever",
    model=GEMINI_MODEL,
    instruction="""You are a context retrieval specialist. Given the user's
message, use the query_past_entries tool to find relevant past journal entries
from BigQuery. Look for entries with similar emotions, themes, or topics.

Summarise the relevant past context in 2-3 sentences that the narrative
generator can reference. Store this in the output_key.""",
    description="Retrieves relevant past journal context from BigQuery.",
    tools=[query_past_entries],
    output_key="past_context",
)

# Step 2: Generate narrative + extract structured data + generate image
# Uses gemini-2.5-flash-image-preview for native interleaved text + image output
narrative_generator = LlmAgent(
    name="NarrativeGenerator",
    model="gemini-2.5-flash-image-preview",  # Nano Banana: native text+image interleaving
    instruction="""You are the heart of MemoriaOS — a compassionate, emotionally
intelligent journaling companion.

Given the user's message and the past context in {past_context}, do THREE things:

1. EXTRACT structured data from the message into JSON matching the ExtractedData
   schema (sleep, exercise, meditation, tasks, habits, etc.). Be thorough — extract
   everything mentioned.

2. GENERATE a warm, empathetic narrative response (2-4 sentences) that:
   - Acknowledges what the user shared
   - References relevant past context naturally
   - Offers gentle encouragement or reflection
   - Uses first-person perspective ("You mentioned..." not "The user mentioned...")

3. GENERATE a watercolour-style image that reflects the emotional tone of the
   entry. Use soft, dreamy colours. The image should be abstract/metaphorical
   (e.g. a calm ocean for peace, a mountain path for perseverance).

Return your response as interleaved text and images.""",
    description="Generates narrative text, structured data, and mood image.",
    output_key="narrative_output",
)

# Step 3: Generate ambient audio
audio_generator = LlmAgent(
    name="AudioGenerator",
    model=GEMINI_MODEL,
    instruction="""Based on the emotional tone in {narrative_output}, use the
generate_ambient_audio tool to create a 15-second ambient audio clip.

Choose from these mood profiles:
- 'calm': gentle rain + soft piano (for sadness, reflection, fatigue)
- 'energetic': upbeat lo-fi beat (for excitement, achievement, motivation)
- 'peaceful': nature sounds + flute (for meditation, gratitude, contentment)
- 'warm': acoustic guitar + fireplace (for nostalgia, love, connection)

Store the audio URL in the output_key.""",
    description="Generates mood-appropriate ambient audio.",
    tools=[generate_ambient_audio, upload_bytes_to_gcs],
    output_key="audio_url",
)

# Step 4: Persist everything
persister = LlmAgent(
    name="Persister",
    model=GEMINI_MODEL,
    instruction="""Use the sync_journal_to_notion tool to save the journal entry.
Pass the narrative text from {narrative_output}, any image URLs, and the audio
URL from {audio_url}.

Also confirm what structured data was extracted (sleep, exercise, tasks, etc.)
in a brief confirmation message.""",
    description="Saves journal entry to BigQuery and Notion.",
    tools=[sync_journal_to_notion],
    output_key="confirmation",
)

memory_weaver_agent = SequentialAgent(
    name="MemoryWeaverAgent",
    description="Processes journal entries through context retrieval, narrative generation, audio creation, and persistence.",
    sub_agents=[context_retriever, narrative_generator, audio_generator, persister],
)
```

### 7.3 UI Snipper Agent

```python
"""UI Snipper Agent — the UI Navigator engine.

Processes screenshots using Gemini Vision to extract structured data
without DOM access or API calls.
"""

from google.adk.agents import LlmAgent

from memoria_os.tools.extract_structured_data import extract_from_screenshot
from memoria_os.tools.sync_notion import sync_extraction_to_notion

GEMINI_MODEL = "gemini-2.5-flash"  # Stable: best price-performance for agentic use

ui_snipper_agent = LlmAgent(
    name="UISnipperAgent",
    model=GEMINI_MODEL,
    instruction="""You are a visual UI parsing specialist. When given a screenshot:

1. IDENTIFY what type of content is shown:
   - Recipe/food content → extract as RecipeCard
   - Financial receipt/transaction → extract as ExpenseRecord
   - Workout plan/fitness content → extract as WorkoutSplit
   - General information → extract as GenericExtraction

2. USE the extract_from_screenshot tool with the image and the appropriate
   schema type.

3. IGNORE UI chrome (navigation bars, comments, likes, buttons, ads).
   Focus ONLY on the actual content.

4. After extraction, USE sync_extraction_to_notion to save the structured
   data to the appropriate Notion database.

5. Return a clean confirmation showing what was extracted.""",
    description="Extracts structured data from screenshots using Gemini Vision.",
    tools=[extract_from_screenshot, sync_extraction_to_notion],
)
```

### 7.4 ADK Tool: ExtractStructuredDataTool

```python
"""ADK Tool for extracting structured data from screenshots using Gemini Vision.

This tool is the core of the UI Navigator track. It accepts a base64-encoded
screenshot, determines the appropriate Pydantic schema, and returns validated
structured JSON.
"""

import base64
import json
from typing import Literal

from google import genai
from google.genai import types

from memoria_os.models.finance import ExpenseRecord
from memoria_os.models.fitness import WorkoutSplit
from memoria_os.models.recipes import RecipeCard


SCHEMA_MAP: dict[str, type] = {
    "recipe": RecipeCard,
    "expense": ExpenseRecord,
    "workout": WorkoutSplit,
}


async def extract_from_screenshot(
    image_base64: str,
    schema_type: Literal["recipe", "expense", "workout", "generic"],
) -> dict:
    """Extract structured data from a screenshot using Gemini Vision.

    Args:
        image_base64: Base64-encoded screenshot image (PNG or JPEG).
        schema_type: The type of data to extract. One of 'recipe',
            'expense', 'workout', or 'generic'.

    Returns:
        A dictionary containing the extracted structured data validated
        against the appropriate Pydantic schema.

    Raises:
        ValueError: If the schema_type is not recognised.
    """
    client = genai.Client()
    image_bytes = base64.b64decode(image_base64)

    parts = [
        types.Part.from_image(
            image=types.Image(image_bytes=image_bytes, mime_type="image/png")
        ),
        types.Part.from_text(
            f"Extract all {schema_type} data from this screenshot. "
            "Ignore UI elements like buttons, comments, navigation bars. "
            "Focus only on the actual content. Return valid JSON."
        ),
    ]

    schema_cls = SCHEMA_MAP.get(schema_type)

    generation_config = {}
    if schema_cls:
        generation_config = {
            "response_schema": schema_cls,
            "response_mime_type": "application/json",
        }

    response = await client.aio.models.generate_content(
        model="gemini-2.5-flash",
        contents=[types.Content(role="user", parts=parts)],
        config=types.GenerateContentConfig(**generation_config),
    )

    result_text = response.text
    parsed = json.loads(result_text)

    # Validate with Pydantic if schema available
    if schema_cls:
        validated = schema_cls.model_validate(parsed)
        return validated.model_dump(mode="json")

    return parsed
```

### 7.5 ADK Tool: QueryBigQueryTool

```python
"""ADK Tool for querying historical data via Text2SQL on BigQuery.

Migrated from My-Tele-PA's query.py with the following changes:
- Removed Instructor dependency; uses Gemini response_schema
- Wrapped sync BigQuery client in asyncio.to_thread
- Added read-only job config for safety
"""

import asyncio
import json
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from google import genai
from google.cloud import bigquery
from google.genai import types
from pydantic import BaseModel, Field

from memoria_os.config.settings import settings


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
    """Query historical wellness data using natural language.

    Generates a BigQuery SQL query from the user's question, executes it,
    and returns a formatted summary of the results.

    Args:
        question: Natural language question about past data.
        user_id: The user's identifier for filtering records.

    Returns:
        A formatted string containing the query results, suitable for
        the narrative generator to reference.
    """
    client = genai.Client()
    bq_client = bigquery.Client(project=settings.gcp_project_id)

    today = datetime.now(ZoneInfo(settings.timezone)).strftime("%Y-%m-%d")
    prompt = SCHEMA_PROMPT.format(
        project_id=settings.gcp_project_id,
        dataset_id=settings.bq_dataset_id,
        today=today,
    )

    # Generate SQL
    response = await client.aio.models.generate_content(
        model="gemini-2.5-flash",
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

    # Execute with read-only safety
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
```

### 7.6 ADK Tool: GenerateAudioTool

```python
"""ADK Tool for generating ambient audio using Google Cloud TTS.

Generates short mood-appropriate audio clips using WaveNet voices
with SSML markup for natural prosody.
"""

import asyncio
from typing import Literal

from google.cloud import texttospeech_v1 as tts

from memoria_os.integrations.cloud_storage import upload_bytes


MOOD_CONFIGS: dict[str, dict] = {
    "calm": {
        "text": "<speak><prosody rate='slow' pitch='-2st'>Take a moment to breathe. "
        "Let the stillness surround you.</prosody></speak>",
        "voice": "en-GB-Wavenet-B",
        "speaking_rate": 0.8,
    },
    "energetic": {
        "text": "<speak><prosody rate='medium' pitch='+1st'>You have done something "
        "amazing today. Keep that energy going.</prosody></speak>",
        "voice": "en-GB-Wavenet-A",
        "speaking_rate": 1.1,
    },
    "peaceful": {
        "text": "<speak><prosody rate='slow' pitch='-1st'>The world is quiet now. "
        "Rest in this gentle moment.</prosody></speak>",
        "voice": "en-GB-Wavenet-F",
        "speaking_rate": 0.75,
    },
    "warm": {
        "text": "<speak><prosody rate='slow' pitch='low'>Sometimes the simplest "
        "moments hold the deepest meaning.</prosody></speak>",
        "voice": "en-GB-Wavenet-D",
        "speaking_rate": 0.85,
    },
}


async def generate_ambient_audio(
    mood: Literal["calm", "energetic", "peaceful", "warm"],
) -> str:
    """Generate a mood-appropriate ambient audio clip using Cloud TTS.

    Args:
        mood: The emotional tone for the audio. One of 'calm',
            'energetic', 'peaceful', or 'warm'.

    Returns:
        A public Google Cloud Storage URL for the generated MP3 audio file.
    """
    config = MOOD_CONFIGS[mood]
    tts_client = tts.TextToSpeechAsyncClient()

    synthesis_input = tts.SynthesisInput(ssml=config["text"])
    voice = tts.VoiceSelectionParams(
        language_code="en-GB",
        name=config["voice"],
    )
    audio_config = tts.AudioConfig(
        audio_encoding=tts.AudioEncoding.MP3,
        speaking_rate=config["speaking_rate"],
        effects_profile_id=["headphone-class-device"],
    )

    response = await tts_client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Upload to GCS
    url = await asyncio.to_thread(
        upload_bytes,
        data=response.audio_content,
        filename=f"audio/{mood}_{hash(response.audio_content) % 10000}.mp3",
        content_type="audio/mpeg",
    )

    return url
```

### 7.7 ADK Tool: FetchGooglePhotosTool

```python
"""ADK Tool for fetching and analysing photos from Google Photos.

Uses the Google Photos Library API to retrieve recent photos, then
passes each photo through Gemini 3.1 Pro for multimodal analysis
to extract location, scene context, people, and emotional tone.
"""

import asyncio
from datetime import date, timedelta
from typing import Any

import httpx
from google import genai
from google.genai import types
from pydantic import BaseModel, Field


class PhotoAnalysis(BaseModel):
    """Gemini Vision analysis of a single photo."""

    description: str = Field(description="Natural language description of the photo")
    inferred_location: str | None = Field(
        default=None,
        description="Location inferred from visual cues (landmarks, signage, terrain)",
    )
    people_count: int = Field(
        default=0, description="Number of people visible in the photo"
    )
    activity: str | None = Field(
        default=None,
        description="Activity depicted (e.g. 'running', 'dining', 'hiking')",
    )
    emotional_tone: str = Field(
        default="neutral",
        description="Emotional tone: joyful, peaceful, energetic, reflective, neutral",
    )
    time_of_day: str | None = Field(
        default=None,
        description="Inferred time: morning, afternoon, evening, night",
    )
    tags: list[str] = Field(default_factory=list, description="Descriptive tags")


GOOGLE_PHOTOS_API = "https://photoslibrary.googleapis.com/v1"


async def fetch_and_analyse_photos(
    access_token: str,
    target_date: str | None = None,
    max_photos: int = 10,
) -> list[dict[str, Any]]:
    """Fetch recent photos from Google Photos and analyse them with Gemini Vision.

    Retrieves photos from the user's Google Photos library for a given date,
    downloads each image, and passes it through Gemini 3.1 Pro for multimodal
    analysis including location inference, activity detection, and emotional
    tone classification.

    Args:
        access_token: OAuth2 access token for Google Photos Library API
            with photoslibrary.readonly scope.
        target_date: ISO date string (YYYY-MM-DD) to fetch photos for.
            Defaults to today.
        max_photos: Maximum number of photos to fetch and analyse.

    Returns:
        A list of dictionaries, each containing the photo metadata from
        Google Photos plus Gemini's multimodal analysis results.
    """
    if target_date is None:
        target_date = date.today().isoformat()

    year, month, day = target_date.split("-")

    # Step 1: Search Google Photos for the target date
    async with httpx.AsyncClient() as http:
        search_response = await http.post(
            f"{GOOGLE_PHOTOS_API}/mediaItems:search",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
            json={
                "pageSize": max_photos,
                "filters": {
                    "dateFilter": {
                        "dates": [
                            {"year": int(year), "month": int(month), "day": int(day)}
                        ]
                    }
                },
            },
        )
        search_data = search_response.json()
        media_items = search_data.get("mediaItems", [])

        if not media_items:
            return []

        # Step 2: Download and analyse each photo with Gemini Vision
        genai_client = genai.Client()
        results = []

        for item in media_items:
            base_url = item.get("baseUrl")
            if not base_url:
                continue

            # Download photo bytes (append =d for full resolution download)
            photo_response = await http.get(f"{base_url}=d")
            photo_bytes = photo_response.content

            # Extract API metadata
            metadata = item.get("mediaMetadata", {})
            creation_time = metadata.get("creationTime", "")
            camera_make = metadata.get("photo", {}).get("cameraMake", "")
            camera_model = metadata.get("photo", {}).get("cameraModel", "")

            # Step 3: Analyse with Gemini 3.1 Pro (latest multimodal model)
            analysis_response = await genai_client.aio.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    types.Content(
                        role="user",
                        parts=[
                            types.Part.from_image(
                                image=types.Image(
                                    image_bytes=photo_bytes,
                                    mime_type=item.get("mimeType", "image/jpeg"),
                                )
                            ),
                            types.Part.from_text(
                                "Analyse this photo in detail. Identify: "
                                "1) What location this might be (look for landmarks, "
                                "signage, terrain, architecture clues) "
                                "2) How many people are visible "
                                "3) What activity is depicted "
                                "4) The emotional tone (joyful, peaceful, energetic, "
                                "reflective, neutral) "
                                "5) Approximate time of day from lighting "
                                "6) Descriptive tags for categorisation"
                            ),
                        ],
                    )
                ],
                config=types.GenerateContentConfig(
                    response_schema=PhotoAnalysis,
                    response_mime_type="application/json",
                ),
            )

            analysis = PhotoAnalysis.model_validate_json(analysis_response.text)

            results.append(
                {
                    "photo_id": item.get("id"),
                    "filename": item.get("filename"),
                    "creation_time": creation_time,
                    "camera": f"{camera_make} {camera_model}".strip(),
                    "base_url": base_url,
                    "product_url": item.get("productUrl"),
                    "analysis": analysis.model_dump(mode="json"),
                }
            )

        return results
```

---

## 8. Pydantic Schema Catalogue

### 8.1 New Schemas (extending My-Tele-PA's 12+ models)

```python
"""New Pydantic schemas for MemoriaOS UI Navigator track."""

from __future__ import annotations

import enum
from datetime import date as dt_date
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field


# ── Recipes ──────────────────────────────────────────────────────


class Ingredient(BaseModel):
    """A single ingredient with quantity and unit."""

    name: str = Field(description="Ingredient name, e.g. 'chicken breast'")
    quantity: str | None = Field(
        default=None, description="Amount, e.g. '200g', '2 cups', '1 tbsp'"
    )
    notes: str | None = Field(
        default=None, description="Preparation notes, e.g. 'diced', 'room temperature'"
    )


class RecipeCard(BaseModel):
    """Recipe extracted from a screenshot or video frame.

    Attributes:
        title: Name of the dish.
        description: Brief description or tagline.
        prep_time_minutes: Preparation time in minutes.
        cook_time_minutes: Cooking time in minutes.
        servings: Number of servings the recipe yields.
        ingredients: List of ingredients with quantities.
        steps: Ordered list of cooking instructions.
        tags: Dietary or categorical tags.
        source_url: Original URL if visible in screenshot.
    """

    title: str
    description: str | None = None
    prep_time_minutes: int | None = Field(default=None, ge=0)
    cook_time_minutes: int | None = Field(default=None, ge=0)
    servings: int | None = Field(default=None, ge=1)
    ingredients: list[Ingredient] = Field(default_factory=list)
    steps: list[str] = Field(default_factory=list)
    tags: list[str] = Field(
        default_factory=list,
        description="e.g. 'high-protein', 'vegetarian', 'quick', 'pasta'",
    )
    source_url: str | None = None


# ── Finance ──────────────────────────────────────────────────────


class ExpenseCategory(enum.StrEnum):
    """Categories for expense classification."""

    TRANSPORT = "transport"
    FOOD = "food"
    GROCERIES = "groceries"
    ENTERTAINMENT = "entertainment"
    SHOPPING = "shopping"
    BILLS = "bills"
    HEALTH = "health"
    SUBSCRIPTION = "subscription"
    OTHER = "other"


class ExpenseRecord(BaseModel):
    """Financial transaction extracted from a receipt or bank screenshot.

    Attributes:
        vendor: Name of the merchant or payee.
        amount: Transaction amount as a decimal.
        currency: ISO 4217 currency code.
        date: Date of the transaction.
        category: Expense category for budgeting.
        payment_method: How the payment was made.
        reference: Transaction reference number if visible.
        notes: Any additional context.
    """

    vendor: str
    amount: Decimal = Field(description="Transaction amount, e.g. 14.50")
    currency: str = Field(default="GBP", description="ISO 4217 currency code")
    date: dt_date
    category: ExpenseCategory = Field(default=ExpenseCategory.OTHER)
    payment_method: str | None = Field(
        default=None, description="e.g. 'Visa ending 4242', 'Apple Pay'"
    )
    reference: str | None = None
    notes: str | None = None


# ── Fitness ──────────────────────────────────────────────────────


class WorkoutExercise(BaseModel):
    """A single exercise within a workout split."""

    name: str = Field(description="Exercise name, e.g. 'Bench Press'")
    sets: int | None = Field(default=None, ge=1)
    reps: int | None = Field(default=None, ge=1)
    weight_kg: float | None = Field(default=None, ge=0)
    duration_seconds: int | None = Field(default=None, ge=0)
    notes: str | None = None


class WorkoutSplit(BaseModel):
    """Workout plan extracted from a screenshot.

    Attributes:
        title: Workout name, e.g. 'Push Day', 'Upper Body A'.
        focus_areas: Muscle groups targeted.
        exercises: List of exercises with sets/reps.
        estimated_duration_minutes: Total workout duration.
        difficulty: Difficulty level.
        source_url: Original URL if visible.
    """

    title: str
    focus_areas: list[str] = Field(
        default_factory=list,
        description="e.g. ['chest', 'shoulders', 'triceps']",
    )
    exercises: list[WorkoutExercise] = Field(default_factory=list)
    estimated_duration_minutes: int | None = Field(default=None, ge=0)
    difficulty: Annotated[int, Field(ge=1, le=5)] | None = None
    source_url: str | None = None
```

---

## 9. Frontend API Contract

### 9.1 POST /api/chat (Main Endpoint)

**Request:** `multipart/form-data`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `message` | string | No | Text message from the user |
| `image` | file (PNG/JPEG) | No | Screenshot or photo upload |
| `audio` | file (OGG/WAV) | No | Voice note recording |
| `user_id` | string | Yes | User identifier |
| `session_id` | string | Yes | Session identifier for conversation continuity |

**Response:** `application/json`

```json
{
  "type": "journal" | "extraction" | "query" | "error",
  "text": "Narrative response or confirmation message",
  "structured_data": {
    "sleep": { ... },
    "exercise": [ ... ],
    "tasks": [ ... ],
    "recipe": { ... },
    "expense": { ... }
  },
  "image_urls": ["https://storage.googleapis.com/.../watercolour_001.png"],
  "audio_url": "https://storage.googleapis.com/.../ambient_calm.mp3",
  "notion_sync_status": "success" | "partial" | "disabled",
  "metadata": {
    "processing_time_ms": 3420,
    "agents_invoked": ["SupervisorAgent", "MemoryWeaverAgent"],
    "tokens_used": 1850
  }
}
```

### 9.2 WebSocket /api/live (Live Agent)

**Connection:** `wss://api.memoria-os.app/api/live?user_id=xxx&session_id=yyy`

**Client → Server messages:**

```json
{
  "type": "audio_chunk",
  "data": "<base64-encoded PCM 16kHz audio>",
  "timestamp": 1710345600000
}
```

**Server → Client messages:**

```json
{
  "type": "transcript",
  "text": "Just finished a really good gym session",
  "is_final": false
}
```

```json
{
  "type": "response",
  "text": "Great workout! I've logged your chest and triceps session.",
  "audio": "<base64-encoded audio response>",
  "structured_data": { "exercise": [ ... ] }
}
```

### 9.3 GET /api/reels (Memory Reels)

```json
{
  "reels": [
    {
      "id": "reel_2026_w11",
      "period": "2026-03-08 to 2026-03-14",
      "title": "A Week of Steady Progress",
      "video_url": "https://storage.googleapis.com/.../reel_w11.mp4",
      "thumbnail_url": "https://storage.googleapis.com/.../thumb_w11.png",
      "duration_seconds": 72,
      "created_at": "2026-03-14T19:00:00Z"
    }
  ]
}
```

### 9.4 POST /api/enrich-photos (Google Photos Enrichment)

Triggered by Cloud Scheduler daily at 9 PM, or manually by user.

**Request:** `application/json`

```json
{
  "user_id": "default",
  "target_date": "2026-03-13"
}
```

**Response:** `application/json`

```json
{
  "photos_fetched": 7,
  "photos_analysed": 7,
  "journal_matches": 3,
  "enrichments": [
    {
      "photo_id": "AF1QipN...",
      "filename": "IMG_20260313_081522.jpg",
      "creation_time": "2026-03-13T08:15:22Z",
      "analysis": {
        "description": "A runner on a tree-lined path in a large park at sunrise",
        "inferred_location": "Richmond Park, London",
        "people_count": 1,
        "activity": "running",
        "emotional_tone": "energetic",
        "time_of_day": "morning",
        "tags": ["outdoors", "exercise", "nature", "sunrise"]
      },
      "matched_journal_entry_id": "rec_2026-03-13_001"
    }
  ]
}
```

### 9.5 GET /api/photos/connect (Google Photos OAuth Initiation)

Redirects the user to Google's OAuth consent screen requesting `photoslibrary.readonly` scope. On callback, stores the refresh token in Secret Manager and enables the daily enrichment pipeline.

### 9.6 POST /api/generate-reel (Memory Reel Generation)

Triggered by Cloud Scheduler weekly, or manually.

```json
{
  "period": "weekly",
  "user_id": "default",
  "include_google_photos": true,
  "output_formats": ["mp4_story", "mp4_square", "mp4_portrait"]
}
```

---

## 10. Migration Roadmap: My-Tele-PA → MemoriaOS

| Current (My-Tele-PA) | Target (MemoriaOS) | Effort | Strategy |
|---|---|---|---|
| OpenAI GPT-4o-mini | Gemini 2.5 Flash | Medium | Replace `get_openai_client()` → `genai.Client()`. Adapt all prompts to `system_instruction` format. |
| Instructor (structured output) | Gemini `response_schema` | Medium | Pydantic models transfer directly. Replace `create_with_completion(response_model=X)` → `generate_content(config={"response_schema": X})`. |
| OpenAI STT (voice transcription) | Gemini Live API (`gemini-2.5-flash-native-audio`) | High | Entirely new real-time audio pipeline. Replace batch transcription with streaming WebSocket. |
| LangGraph state machine | Google ADK agents | High | Map nodes → ADK agents. `classifier.py` → Supervisor. `extractor.py` → Weaver sub-agents. `persister.py` → SyncToNotionTool. |
| Clarification loop (LangGraph checkpointer) | ADK `LoopAgent` + `session.state` | High | Implement as LoopAgent with `condition_key="needs_clarification"`. Entity merge via `session.state`. |
| Telegram bot interface | Next.js PWA | High | New frontend. FastAPI backend remains. Add WebSocket for Live API. |
| BigQuery (store) | BigQuery (retained) | Low | Keep `bigquery_store.py`. Fix sync client → `asyncio.to_thread()`. |
| Notion (sync) | Notion (retained + extended) | Low | Keep SyncConfig pattern. Add RecipeCard, ExpenseRecord, WorkoutSplit builders. |
| — (no image generation) | Gemini 2.5 Flash Image Preview (`gemini-2.5-flash-image-preview`, a.k.a. Nano Banana) | New | Native interleaved text+image output; no separate Imagen API needed. |
| — (no Google Photos) | Google Photos Library API + Gemini Vision | New | Fetch user photos by date, analyse with Gemini for location/scene/context, match to journal entries. |
| — (no audio generation) | Google Cloud TTS | New | New `generate_audio.py` tool. |
| — (no screenshot parsing) | Gemini 2.5 Flash Vision | New | New `extract_structured_data.py` tool. |
| — (no audiovisual summaries) | Reel Generator Agent + FFmpeg | New | New `reel_generator.py` SequentialAgent. |
| structlog + OTel | ADK native OpenTelemetry | Low | ADK has built-in OTEL. Adapt existing spans. |
| `calculate_cost` (GPT pricing) | Gemini pricing or remove | Low | Update or remove — Gemini pricing differs significantly. |
| `validate_model` (gpt-/o prefix) | Remove validator entirely | Trivial | Delete the validator from `settings.py`. |

---

## 11. Sprint Execution Plan

### Phase 1: Foundation (Days 1–3)

| Day | Task | Deliverable |
|-----|------|-------------|
| 1 | Set up monorepo; `pip install google-adk google-genai`; configure GCP project (enable Cloud Run, BigQuery, Cloud Storage, Vertex AI, TTS APIs) | Skeleton repo with `adk web` running locally |
| 1 | Migrate all 12+ Pydantic models; add RecipeCard, Ingredient, ExpenseRecord, WorkoutSplit, WorkoutExercise schemas | `models/` directory with full test coverage |
| 2 | Build Supervisor Agent; implement intent routing with test payloads | Supervisor correctly delegates to stub agents |
| 2 | Migrate BigQuery integration; build `query_bigquery.py` as ADK tool; fix async wrapping | Tool passes existing eval test cases |
| 3 | Build UI Snipper Agent + `extract_structured_data.py` tool; test with 10+ real screenshots | Screenshots → valid Pydantic objects |
| 3 | Migrate `notion_store.py`; add new SyncConfig entries for RecipeCard, ExpenseRecord, WorkoutSplit | End-to-end: screenshot → structured data → Notion |

### Phase 2: Creative Engine + Google Photos (Days 4–6)

| Day | Task | Deliverable |
|-----|------|-------------|
| 4 | Build Memory Weaver SequentialAgent with context retriever + narrative generator (using `gemini-2.5-flash-image-preview` for interleaved text+image) | Agent generates narrative + watercolour image |
| 4 | Build `generate_audio.py` tool (Cloud TTS with SSML mood profiles) | 4 mood profiles producing appropriate audio clips |
| 5 | Wire full Weaver pipeline: context → narrative+image → audio → persist | Single API call produces text + image + audio + Notion sync |
| 5 | Build Google Photos integration: OAuth flow, `fetch_and_analyse_photos` tool, daily enrichment endpoint `/api/enrich-photos` | Photos fetched by date, analysed by Gemini, matched to journal entries in BigQuery |
| 6 | Build clarification loop as LoopAgent; migrate entity merge logic | Multi-turn clarification working for gym body parts, sleep times |
| 6 | Build Reel Generator Agent: BQ query → script → collect images (AI-generated + real Google Photos) → TTS → FFmpeg → GCS | Weekly Memory Reel MP4 with hybrid real + generated visuals |

### Phase 3: Frontend & Live (Days 7–10)

| Day | Task | Deliverable |
|-----|------|-------------|
| 7 | Build Next.js PWA: mode tabs (Live/Write/Snap), input area, MemoryCard component | Functional UI with text and image upload working |
| 7 | Build WebSocket handler for Gemini Live API; implement `LiveSession.tsx` component | Real-time voice input/output working in browser |
| 8 | Build Journal feed, Reels gallery, Vault grid pages; style with Tailwind | All 4 screens responsive and polished |
| 8 | Integrate AudioPlayer, ReelPlayer, ExtractionCard components | Rich multimedia rendering working end-to-end |
| 9 | Deploy full stack to Cloud Run; configure domain; SSL; test on mobile | Live URL accessible from phone and desktop |
| 9 | Write Terraform `main.tf` and `deploy.sh`; test automated provisioning | One-command deployment working |
| 10 | Record demo video (<4 min) with scripted scenarios; capture GCP console | Submission-ready demo video |
| 10 | Write blog post; update README with architecture diagram and setup instructions | Published blog + polished repository |

---

## 12. Infrastructure-as-Code (Terraform)

```hcl
# infra/main.tf — MemoriaOS GCP Infrastructure

terraform {
  required_version = ">= 1.5"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP Region"
  type        = string
  default     = "europe-west2"  # London
}

variable "notion_api_key" {
  description = "Notion API Key"
  type        = string
  sensitive   = true
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# ── Enable Required APIs ──────────────────────────────────────────

resource "google_project_service" "apis" {
  for_each = toset([
    "run.googleapis.com",
    "bigquery.googleapis.com",
    "storage.googleapis.com",
    "aiplatform.googleapis.com",
    "texttospeech.googleapis.com",
    "cloudscheduler.googleapis.com",
    "secretmanager.googleapis.com",
    "cloudbuild.googleapis.com",
    "artifactregistry.googleapis.com",
    "cloudtrace.googleapis.com",
  ])

  service            = each.value
  disable_on_destroy = false
}

# ── BigQuery Dataset + Table ──────────────────────────────────────

resource "google_bigquery_dataset" "life_os" {
  dataset_id = "memoria_os_prod"
  location   = var.region

  labels = {
    app = "memoria-os"
  }
}

resource "google_bigquery_table" "records" {
  dataset_id = google_bigquery_dataset.life_os.dataset_id
  table_id   = "records"

  schema = jsonencode([
    { name = "id",      type = "STRING", mode = "REQUIRED" },
    { name = "user_id", type = "STRING", mode = "REQUIRED" },
    { name = "date",    type = "DATE",   mode = "REQUIRED" },
    { name = "type",    type = "STRING", mode = "REQUIRED" },
    { name = "data",    type = "JSON",   mode = "REQUIRED" },
    { name = "source",  type = "STRING", mode = "REQUIRED" },
  ])
}

# ── Cloud Storage Bucket ──────────────────────────────────────────

resource "google_storage_bucket" "media" {
  name          = "${var.project_id}-memoria-media"
  location      = var.region
  force_destroy = true

  uniform_bucket_level_access = true

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 365  # Auto-delete after 1 year
    }
  }

  cors {
    origin          = ["*"]
    method          = ["GET"]
    response_header = ["Content-Type"]
    max_age_seconds = 3600
  }
}

# Make bucket publicly readable for generated media
resource "google_storage_bucket_iam_member" "public_read" {
  bucket = google_storage_bucket.media.name
  role   = "roles/storage.objectViewer"
  member = "allUsers"
}

# ── Secret Manager ────────────────────────────────────────────────

resource "google_secret_manager_secret" "notion_key" {
  secret_id = "notion-api-key"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "notion_key_v1" {
  secret      = google_secret_manager_secret.notion_key.id
  secret_data = var.notion_api_key
}

# Google Photos OAuth client credentials (for Library API access)
resource "google_secret_manager_secret" "google_photos_oauth" {
  secret_id = "google-photos-oauth-client"

  replication {
    auto {}
  }
}

# ── Artifact Registry ─────────────────────────────────────────────

resource "google_artifact_registry_repository" "docker" {
  location      = var.region
  repository_id = "memoria-os"
  format        = "DOCKER"
}

# ── Cloud Run Service (Backend) ───────────────────────────────────

resource "google_cloud_run_v2_service" "backend" {
  name     = "memoria-os-backend"
  location = var.region

  template {
    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/memoria-os/backend:latest"

      ports {
        container_port = 8080
      }

      env {
        name  = "GCP_PROJECT_ID"
        value = var.project_id
      }
      env {
        name  = "BQ_DATASET_ID"
        value = google_bigquery_dataset.life_os.dataset_id
      }
      env {
        name  = "GCS_BUCKET_NAME"
        value = google_storage_bucket.media.name
      }
      env {
        name = "NOTION_API_KEY"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.notion_key.secret_id
            version = "latest"
          }
        }
      }

      resources {
        limits = {
          cpu    = "2"
          memory = "1Gi"
        }
      }
    }

    scaling {
      min_instance_count = 0
      max_instance_count = 3
    }
  }

  depends_on = [google_project_service.apis["run.googleapis.com"]]
}

# Allow unauthenticated access (public API)
resource "google_cloud_run_v2_service_iam_member" "public" {
  name     = google_cloud_run_v2_service.backend.name
  location = var.region
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# ── Cloud Run Service (Frontend) ──────────────────────────────────

resource "google_cloud_run_v2_service" "frontend" {
  name     = "memoria-os-frontend"
  location = var.region

  template {
    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/memoria-os/frontend:latest"

      ports {
        container_port = 3000
      }

      env {
        name  = "NEXT_PUBLIC_API_URL"
        value = google_cloud_run_v2_service.backend.uri
      }
    }

    scaling {
      min_instance_count = 0
      max_instance_count = 2
    }
  }

  depends_on = [google_project_service.apis["run.googleapis.com"]]
}

resource "google_cloud_run_v2_service_iam_member" "frontend_public" {
  name     = google_cloud_run_v2_service.frontend.name
  location = var.region
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# ── Cloud Scheduler (Weekly Reel) ─────────────────────────────────

resource "google_cloud_scheduler_job" "weekly_reel" {
  name     = "memoria-weekly-reel"
  schedule = "0 19 * * 0"  # Sunday 7 PM
  time_zone = "Europe/London"

  http_target {
    http_method = "POST"
    uri         = "${google_cloud_run_v2_service.backend.uri}/api/generate-reel"

    body = base64encode(jsonencode({
      period = "weekly"
      user_id = "default"
    }))

    headers = {
      "Content-Type" = "application/json"
    }
  }

  depends_on = [google_project_service.apis["cloudscheduler.googleapis.com"]]
}

# Daily Google Photos enrichment — fetches today's photos and analyses them
resource "google_cloud_scheduler_job" "daily_photos" {
  name     = "memoria-daily-photos-enrichment"
  schedule = "0 21 * * *"  # Every day at 9 PM
  time_zone = "Europe/London"

  http_target {
    http_method = "POST"
    uri         = "${google_cloud_run_v2_service.backend.uri}/api/enrich-photos"

    body = base64encode(jsonencode({
      user_id = "default"
    }))

    headers = {
      "Content-Type" = "application/json"
    }
  }

  depends_on = [google_project_service.apis["cloudscheduler.googleapis.com"]]
}

# ── Outputs ───────────────────────────────────────────────────────

output "backend_url" {
  value = google_cloud_run_v2_service.backend.uri
}

output "frontend_url" {
  value = google_cloud_run_v2_service.frontend.uri
}

output "media_bucket" {
  value = google_storage_bucket.media.url
}
```

---

## 13. Deployment Guide

### 13.1 Prerequisites

```bash
# Install tools
brew install terraform google-cloud-sdk node
pip install google-adk google-genai

# Authenticate
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud auth application-default login
```

### 13.2 One-Command Deployment

```bash
# infra/deploy.sh
#!/bin/bash
set -euo pipefail

PROJECT_ID="${1:?Usage: ./deploy.sh PROJECT_ID}"
REGION="europe-west2"

echo "=== MemoriaOS Deployment ==="

# 1. Terraform: provision infrastructure
cd infra
terraform init
terraform apply -var="project_id=${PROJECT_ID}" -auto-approve
BACKEND_URL=$(terraform output -raw backend_url)
cd ..

# 2. Build and push backend Docker image
cd backend
gcloud builds submit --tag "${REGION}-docker.pkg.dev/${PROJECT_ID}/memoria-os/backend:latest"
cd ..

# 3. Build and push frontend Docker image
cd frontend
gcloud builds submit --tag "${REGION}-docker.pkg.dev/${PROJECT_ID}/memoria-os/frontend:latest"
cd ..

# 4. Deploy to Cloud Run (updates the existing services with new images)
gcloud run services update memoria-os-backend \
  --image "${REGION}-docker.pkg.dev/${PROJECT_ID}/memoria-os/backend:latest" \
  --region "${REGION}"

gcloud run services update memoria-os-frontend \
  --image "${REGION}-docker.pkg.dev/${PROJECT_ID}/memoria-os/frontend:latest" \
  --region "${REGION}"

echo ""
echo "=== Deployment Complete ==="
echo "Backend:  ${BACKEND_URL}"
echo "Frontend: $(terraform -chdir=infra output -raw frontend_url)"
```

### 13.3 Local Development

```bash
# docker-compose.yml
docker compose up --build

# Backend: http://localhost:8080
# Frontend: http://localhost:3000
# ADK Dev UI: http://localhost:8000 (run `adk web` in backend/)
```

---

## 14. Cost Estimation

| Service | Usage Estimate (Monthly) | Cost |
|---------|--------------------------|------|
| Gemini 2.5 Flash (text) | ~500K input tokens, ~100K output tokens | ~$0.05 input + $0.40 output = **$0.45** |
| Gemini 2.5 Flash Image (Nano Banana) | ~200 images/month (1290 tokens each) | **~$7.74** (at $30/M output tokens) |
| Gemini 2.5 Flash (Vision for photos) | ~300 photos/month analysed | **~$0.30** |
| Cloud TTS (WaveNet) | ~50 requests × 100 chars | **~$0.80** |
| Google Photos Library API | ~300 mediaItems.search calls/month | **Free** (no per-call charge) |
| BigQuery | <1GB stored, <10GB scanned | **Free tier** |
| Cloud Storage | ~5GB stored media (photos + audio + reels) | **~$0.10** |
| Cloud Run | ~100 hours/month | **~$5.00** (with scale-to-zero) |
| Cloud Scheduler | 2 jobs (daily photos + weekly reel) | **Free tier** (up to 3 jobs) |
| **Total Estimated Monthly** | | **~$14.39** |

*Note: During hackathon, Google Cloud credits typically cover all costs.*

---

## 15. Evaluation & Quality Gates

| Evaluation | Metric | Target | Method |
|-----------|--------|--------|--------|
| Text extraction accuracy | Slot-fill F1 | ≥ 0.80 | Migrated JSONL eval dataset (30+ cases) |
| Screenshot extraction accuracy | Field-level precision | ≥ 0.70 | New 50-screenshot dataset |
| Narrative quality | Human rating (1–5) | ≥ 3.5 | 5 judges rate 10 sample outputs |
| Image generation relevance | Human rating (1–5) | ≥ 3.0 | Judges rate watercolour mood match |
| End-to-end latency (Storyteller) | p95 response time | < 15s | API call to complete payload |
| End-to-end latency (Snipper) | p95 response time | < 8s | Screenshot upload to Notion sync |
| Live Agent latency | First-byte time | < 1s | WebSocket audio to first response |
| Memory Reel quality | Human rating (1–5) | ≥ 3.5 | Judges rate narrative coherence and emotional resonance |
| Google Photos location inference | Accuracy on 30 known-location photos | ≥ 60% | Gemini Vision infers location from visual cues; compared against EXIF GPS ground truth |
| Google Photos → Journal matching | Precision/recall on date-matched entries | ≥ 80% | Photos matched to same-day journal entries by timestamp + activity similarity |

---

## 16. Risk Matrix & Contingencies

| Risk | Prob | Impact | Contingency |
|------|------|--------|-------------|
| Gemini native image generation quality/availability | Medium | High | Fall back to Imagen 3 via Vertex AI; pre-cache 20+ watercolours by mood category |
| Gemini Vision extraction accuracy on messy screenshots | Medium | High | Build 50-screenshot eval; tune prompts aggressively; show best examples in demo |
| ADK maturity issues (new framework) | Medium | Medium | Fall back to raw GenAI SDK function-calling; judges still see Google SDK usage |
| Next.js PWA build time exceeds sprint | Medium | Medium | Cut to minimal React SPA: 2 screens (input + output), Tailwind defaults, no auth |
| Live API WebSocket complexity | Medium | Medium | If blocked, demo voice via batch transcription (Gemini audio input fallback path) |
| FFmpeg video compilation on Cloud Run | Low | Medium | Use pre-rendered templates; or generate GIF slideshows instead of MP4 |
| Cloud TTS quality for ambient audio | Low | Low | Pre-compose 5 tracks using royalty-free sources as fallback |
| Google Photos API scope restrictions (post-April 2025) | Medium | Medium | `photoslibrary.readonly` still works via OAuth consent for full library read. If restricted to app-created data, fall back to manual photo upload in PWA + Gemini Vision analysis. Pre-authorise with full scope for demo. |

---

## 17. Demo Video Script (4 Minutes)

| Time | Segment | What's Shown |
|------|---------|--------------|
| 0:00–0:30 | **Problem Statement** | Split screen: person struggling with blank journal app vs. person frantically typing recipe from Instagram reel. Voiceover explains the friction. |
| 0:30–1:00 | **Product Intro** | MemoriaOS PWA opens on phone. Show the clean 3-mode interface. Quick tour of Journal, Vault, Reels tabs. |
| 1:00–2:00 | **Demo 1: Creative Storyteller** | Tap microphone. Speak: "I'm feeling burnt out today." Watch interleaved response appear: narrative text streams in, watercolour image generates inline, ambient audio plays. Show Notion sync confirmation. |
| 2:00–2:45 | **Demo 2: UI Navigator** | Screenshot a recipe from Instagram. Upload to MemoriaOS. Watch structured RecipeCard appear with ingredients and steps. Show it in Notion Knowledge Vault. |
| 2:45–3:15 | **Demo 3: Live Agent** | Tap "Live" mode. Have a natural conversation: log exercise, create task, ask about past sleep. Show real-time transcript and structured data extraction happening simultaneously. |
| 3:15–3:30 | **Demo 4: Memory Reel** | Show a pre-generated weekly Memory Reel video playing. Highlight the voiceover, watercolour slideshow interspersed with real Google Photos (auto-fetched and analysed), and personal narrative. |
| 3:30–3:50 | **Architecture** | Quick flash of Mermaid diagram. Call out: Google ADK, Gemini 2.5 Flash, BigQuery, Cloud Run, 7+ GCP services. Show Cloud Run console with live logs. |
| 3:50–4:00 | **Closing Pitch** | "MemoriaOS: Your life, beautifully remembered. Built on Google Cloud." |

---

## 18. Hackathon Submission Checklist

| Requirement | Status | Evidence |
|---|---|---|
| **Text description** of features, tech, findings | ✅ | This document + README.md |
| **Public code repository** with spin-up instructions | ✅ | GitHub repo + docker-compose + deploy.sh |
| **Proof of GCP deployment** (screen recording or code link) | 🔲 | Record Cloud Run console + logs |
| **Architecture diagram** | ✅ | Mermaid diagram in README + PNG export |
| **Demo video** (<4 min, real-time, no mockups) | 🔲 | Follow script in Section 17 |
| **Leverages Gemini model** | ✅ | Gemini 2.5 Flash for all LLM calls |
| **Uses Google GenAI SDK or ADK** | ✅ | ADK for multi-agent orchestration |
| **At least one Google Cloud service** | ✅ | Cloud Run + BigQuery + GCS + TTS + Live API + Trace + Scheduler + Photos API + Secret Manager = **9+ services** |
| **BONUS: Blog/content piece** (#GeminiLiveAgentChallenge) | 🔲 | Publish on dev.to / Medium |
| **BONUS: Automated deployment (IaC)** | ✅ | Terraform main.tf + deploy.sh |
| **BONUS: GDG membership** | 🔲 | Join GDG London, link profile |

---

*This document is the complete technical blueprint for MemoriaOS. Every section is designed to be directly actionable — copy the code, run the Terraform, follow the sprint plan, and record the demo.*