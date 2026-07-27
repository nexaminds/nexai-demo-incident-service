job "nexai-demo-incident-service" {
  datacenters = ["dc1"]
  type        = "service"

  variable "image" {
    type    = string
    default = "nexai-demo-incident-service:latest"
  }

  group "api" {
    count = 1

    network {
      port "http" {
        to = 8000
      }
    }

    task "app" {
      driver = "docker"

      config {
        image = var.image
        ports = ["http"]
      }

      resources {
        cpu    = 200
        memory = 128
      }

      service {
        name = "nexai-demo-incident-service"
        port = "http"

        check {
          type     = "http"
          path     = "/healthz"
          interval = "10s"
          timeout  = "2s"
        }
      }
    }
  }
}
