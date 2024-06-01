resource "helm_release" "ingress-controller" {
  name       = "nginx-ingress"
  repository = "https://kubernetes.github.io/ingress-nginx"
  chart      = "ingress-nginx"
  version    = "4.10.1"
  namespace = "ingress-controller"


  values = [
    templatefile("${path.module}/ingress_controller_values.yaml", {})
  ]


}