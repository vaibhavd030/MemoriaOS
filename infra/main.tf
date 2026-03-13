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

  lifecycle_rule {
    condition {
      age = 90
    }
    action {
      type = "Delete"
    }
  }
}
