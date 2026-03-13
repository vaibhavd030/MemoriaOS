#!/bin/bash
# deploy.sh — Simple deployment script for MemoriaOS

echo "🚀 Starting MemoriaOS Deployment..."

# 1. Build and push containers
echo "📦 Building containers..."
gcloud builds submit --config cloudbuild.yaml .

# 2. Apply infrastructure
echo "🏗️ Applying infrastructure with Terraform..."
cd infra
terraform init
terraform apply -auto-approve

echo "✅ Deployment Complete!"
