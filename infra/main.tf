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

  cors {
    origin          = ["*"]
    method          = ["GET", "HEAD", "PUT", "POST", "DELETE"]
    response_header = ["*"]
    max_age_seconds = 3600
  }

  lifecycle_rule {
    condition {
      age = 90
    }
    action {
      type = "Delete"
    }
  }
}

# ── Artifact Registry ─────────────────────────────────────────────

resource "google_artifact_registry_repository" "memoria_os" {
  location      = var.region
  repository_id = "memoria-os"
  format        = "DOCKER"
}

# ── Secrets Manager ───────────────────────────────────────────────

resource "google_secret_manager_secret" "google_api_key" {
  secret_id = "GOOGLE_API_KEY"
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "google_api_key_v1" {
  secret      = google_secret_manager_secret.google_api_key.id
  secret_data = var.google_api_key
}

# ── Cloud Run Backend ─────────────────────────────────────────────

resource "google_cloud_run_v2_service" "backend" {
  name     = "memoria-os-backend"
  location = var.region

  template {
    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/memoria-os/backend:latest"
      env {
        name  = "GCP_PROJECT_ID"
        value = var.project_id
      }
      env {
        name = "GOOGLE_API_KEY"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.google_api_key.secret_id
            version = "latest"
          }
        }
      }
    }
  }
}

# ── Storage Public Access ─────────────────────────────────────────

resource "google_storage_bucket_iam_member" "public_viewer" {
  bucket = google_storage_bucket.media.name
  role   = "roles/storage.objectViewer"
  member = "allUsers"
}

# ── Cloud Run Frontend ────────────────────────────────────────────

resource "google_cloud_run_v2_service" "frontend" {
  name     = "memoria-os-frontend"
  location = var.region

  template {
    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/memoria-os/frontend:latest"
      env {
        name  = "NEXT_PUBLIC_API_URL"
        value = google_cloud_run_v2_service.backend.uri
      }
    }
  }
}

# ── Cloud Scheduler ───────────────────────────────────────────────

resource "google_cloud_scheduler_job" "photo_enrichment" {
  name             = "photo-enrichment-job"
  description      = "Triggers Google Photos enrichment pipeline every night"
  schedule         = "0 2 * * *"
  time_zone        = "UTC"
  attempt_deadline = "320s"

  http_target {
    http_method = "POST"
    uri         = "${google_cloud_run_v2_service.backend.uri}/api/enrich-photos"
    body        = base64encode("{}")
  }
}

# ── IAM Public Access ─────────────────────────────────────────────

resource "google_cloud_run_v2_service_iam_member" "backend_public" {
  name     = google_cloud_run_v2_service.backend.name
  location = google_cloud_run_v2_service.backend.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

resource "google_cloud_run_v2_service_iam_member" "frontend_public" {
  name     = google_cloud_run_v2_service.frontend.name
  location = google_cloud_run_v2_service.frontend.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}
