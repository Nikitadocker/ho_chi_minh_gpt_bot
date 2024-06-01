resource "helm_release" "prometheus" {
  name       = "prometheus"
  repository = "https://prometheus-community.github.io/helm-charts"
  chart      = "kube-prometheus-stack"
  version    = "59.1.0"
  namespace = "monitoring"


  values = [
    templatefile("${path.module}/prometheus_stack_values.yaml", {})
  ]


}

