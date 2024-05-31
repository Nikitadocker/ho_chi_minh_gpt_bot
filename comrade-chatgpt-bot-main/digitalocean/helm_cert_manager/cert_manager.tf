resource "helm_release" "cert-manager" {
  name       = "cert-manager"
  repository = "https://charts.jetstack.io"
  chart      = "cert-manager"
  version    = "v1.14.5 "
  namespace = "cert-manager"


  values = [
    templatefile("${path.module}/values.yaml", {})
  ]


}