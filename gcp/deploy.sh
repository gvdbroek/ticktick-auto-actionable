
region="europe-west1"
job_name="ticktick-auto-actionable"
echo Deploying job: $job_name
# Deploy with secrets
gcloud run jobs deploy ticktick-auto-actionable \
  --source . \
  --tasks 1 \
  --set-secrets "API_KEY=api-key:latest" \
  --region $region \
  --project=ticktick-actionable
