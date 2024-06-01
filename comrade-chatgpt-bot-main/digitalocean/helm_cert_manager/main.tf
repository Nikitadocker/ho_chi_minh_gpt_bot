provider "kubectl" {
  config_path= "~/.kube/config_india"
}
provider "helm" {
  kubernetes {
    config_path= "~/.kube/config_india"
  }
}
provider "kubernetes" {
  config_path= "~/.kube/config_india"
}
terraform {
  required_providers {
    kubectl = {
      source  = "alekc/kubectl"
      version = ">= 2.0.2"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "2.5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "2.0.1"
    }
  }
}