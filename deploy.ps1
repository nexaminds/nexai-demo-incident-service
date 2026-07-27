param(
    [string]$ImageName = "nexai-demo-incident-service:latest"
)

docker build -t $ImageName .
nomad job run -var="image=$ImageName" .\nomad\job.nomad
