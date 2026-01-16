#!/bin/bash
# Deployment Script for Cyber Attack Visualization Platforms

# Variables
PROJECT_ID=$(gcloud config get-value project)
REGION="us-central1"
REPO="cyber-viz-repo"

echo "Deploying to Project: $PROJECT_ID in Region: $REGION"

# 1. Enable Services
echo "Enabling services..."
gcloud services enable artifactregistry.googleapis.com run.googleapis.com

# 2. Create Artifact Registry
echo "Creating Artifact Registry..."
gcloud artifacts repositories create $REPO --repository-format=docker --location=$REGION --description="Docker repository for Cyber Viz" || true

# 3. Build & Push Backend
echo "Building Backend..."
gcloud builds submit --tag $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/backend ./backend

# 4. Build & Push Frontend
echo "Building Frontend..."
gcloud builds submit --tag $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/frontend ./frontend

# 5. Deploy Backend
echo "Deploying Backend to Cloud Run..."
gcloud run deploy backend-service \
    --image $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/backend \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --port 8080

# Get Backend URL
BACKEND_URL=$(gcloud run services describe backend-service --platform managed --region $REGION --format 'value(status.url)')
echo "Backend deployed at: $BACKEND_URL"

# 6. Deploy Frontend
echo "Deploying Frontend to Cloud Run..."
# Pass VITE_API_URL as build arg or env var? 
# For static site in nginx, we need to bake it in or use a runtime config.
# For simplicity in this script, we'll just rebuild frontend with the env var if we were building locally, 
# but since we use Cloud Build, we might need a multistage approach or just use relative paths if on same domain (proxy).
# BUT, here backend and frontend are separate services.
# Let's set VITE_API_URL to the backend URL.

echo "Re-building Frontend with Backend URL..."
gcloud builds submit --tag $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/frontend ./frontend --substitutions=_VITE_API_URL=$BACKEND_URL

gcloud run deploy frontend-service \
    --image $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/frontend \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --port 80

FRONTEND_URL=$(gcloud run services describe frontend-service --platform managed --region $REGION --format 'value(status.url)')

echo "Deployment Complete!"
echo "Frontend: $FRONTEND_URL"
echo "Backend: $BACKEND_URL"
