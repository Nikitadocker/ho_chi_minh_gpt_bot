resource "helm_release" "postgres" {
  name       = "postgres"
  repository = "https://charts.bitnami.com/bitnami"
  chart      = "postgresql"
  version    = "15.2.5"
  namespace = "postgres"
  create_namespace = true



  values = [
    templatefile("${path.module}/postgres_values.yaml", {})
  ]


}
