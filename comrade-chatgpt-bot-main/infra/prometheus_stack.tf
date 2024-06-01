resource "helm_release" "prometheus" {
  name       = "prometheus"
  repository = "https://prometheus-community.github.io/helm-charts"
  chart      = "kube-prometheus-stack"
  version    = "59.0.0"
  namespace = "monitoring"


  values = [
    templatefile("${path.module}/values.yaml", {})
  ]


}

