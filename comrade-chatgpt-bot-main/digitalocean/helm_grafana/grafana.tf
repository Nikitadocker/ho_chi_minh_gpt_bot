resource "helm_release" "grafana" {
  name       = "grafana"
  repository = "https://grafana.github.io/helm-charts"
  chart      = "grafana"
  version    = "7.3.9"
  namespace = "grafana"

  values = [
    templatefile("${path.module}/values.yaml", {})
  ]

}