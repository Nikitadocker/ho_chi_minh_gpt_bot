resource "helm_release" "postgres" {
  name       = "postgres"
  repository = "https://charts.bitnami.com/bitnami"
  chart      = "postgresql"
  version    = "15.2.5"
  namespace = "postgres"


  values = [
    templatefile("${path.module}/values.yaml", {})
  ]


}
