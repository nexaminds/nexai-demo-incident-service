# GKE Namespace Bootstrap

A GCP/GKE administrator runs this once after creating the cluster and deployment service account.

```bash
kubectl apply -f k8s/namespace.yaml
kubectl -n nexai-demo create role deployment-manager \
  --verb=get,list,watch,create,update,patch,delete \
  --resource=deployments,replicasets,pods,services
kubectl -n nexai-demo create rolebinding github-deployer \
  --role=deployment-manager \
  --user=<GCP_SERVICE_ACCOUNT_EMAIL>
```

The GitHub Actions identity also needs GCP IAM roles `roles/artifactregistry.writer` and `roles/container.clusterViewer`. Workload Identity Federation grants it permission to impersonate the deployment service account. Do not create a service-account JSON key.
