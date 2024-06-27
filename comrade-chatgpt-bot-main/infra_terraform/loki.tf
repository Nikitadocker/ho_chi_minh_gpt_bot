resource "helm_release" "loki" {
  name       = "loki"
  repository = "https://grafana.github.io/helm-charts"
  chart      = "loki"
  version    = "5.47.2"
  namespace = "loki"
  create_namespace = true



  values = [
    templatefile("${path.module}/loki_values.yaml", {})
  ]


}