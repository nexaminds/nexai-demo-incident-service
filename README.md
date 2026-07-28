# nexai-demo-incident-service

Small FastAPI service used to demonstrate a Managed Agents delivery flow.

## API

- `GET /healthz`
- `POST /orders/quote`
- `POST /orders/validate`

Example request:

```json
{
  "subtotal": 100,
  "discount_percent": 10,
  "tax_percent": 5
}
```

The quote endpoint applies the discount before percentage-based tax. The validation endpoint reports invalid subtotal, discount, and tax values without changing quote behavior.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

On Windows, activate with `.\.venv\Scripts\Activate.ps1`.

Run tests with:

```bash
pytest -q
```

## Deploy

A human-reviewed merge to `main` runs `.github/workflows/deploy-gke.yml`. The workflow tests the app, builds an immutable image tagged with the merged Git SHA, pushes it to Artifact Registry, deploys `k8s/` to GKE, waits for rollout, and verifies `/healthz` plus `/orders/validate`.

The GitHub repository requires these Actions variables:

- `GCP_PROJECT_ID`
- `GCP_REGION`
- `GAR_REPOSITORY`
- `GKE_CLUSTER`
- `GKE_LOCATION`
- `K8S_NAMESPACE` (`nexai-demo`)

It also requires `GCP_WORKLOAD_IDENTITY_PROVIDER` and `GCP_SERVICE_ACCOUNT` Actions secrets. Authentication is keyless through GCP Workload Identity Federation.
