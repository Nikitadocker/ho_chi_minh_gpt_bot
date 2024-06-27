provider "kubernetes" {
  config_path    = "~/.kube/config_india"
}



resource "kubernetes_namespace" "infra" {
  metadata {
    name = "infrastructure"
  }
}