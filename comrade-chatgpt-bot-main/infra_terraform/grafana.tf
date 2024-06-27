resource "helm_release" "grafana" {
  name       = "grafana"
  repository = "https://grafana.github.io/helm-charts"
  chart      = "grafana"
  version    = "7.3.9"
  namespace = "grafana"
  create_namespace = true



  values = [
    templatefile("${path.module}/grafana_values.yaml", {})
  ]


}

