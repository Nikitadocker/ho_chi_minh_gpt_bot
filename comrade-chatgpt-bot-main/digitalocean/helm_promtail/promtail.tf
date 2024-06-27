resource "helm_release" "promtail" {
  name       = "promtail"
  repository = "https://grafana.github.io/helm-charts"
  chart      = "promtail"
  version    = "6.15.5"
  namespace = "promtail"


  values = [
    templatefile("${path.module}/values.yaml", {})
  ]


}
