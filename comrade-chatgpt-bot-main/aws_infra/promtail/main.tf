terraform {
  required_version = ">= 1.4.7"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.53.0"
    }

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

  backend "s3" {
    profile        = "study"
    bucket         = "study-terraform-states"
    key            = "promtail.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
  }
}

provider "aws" {
  profile = "study"
  region  = "ap-southeast-1"
}


provider "kubectl" {
  config_path= "~/.kube/config"
  config_context = "arn:aws:eks:ap-southeast-1:632497825040:cluster/study-cluster"

}

provider "helm" {
  kubernetes {
    config_path= "~/.kube/config"
    config_context = "arn:aws:eks:ap-southeast-1:632497825040:cluster/study-cluster"

  }
}

provider "kubernetes" {
  config_path= "~/.kube/config"
  config_context = "arn:aws:eks:ap-southeast-1:632497825040:cluster/study-cluster"

}