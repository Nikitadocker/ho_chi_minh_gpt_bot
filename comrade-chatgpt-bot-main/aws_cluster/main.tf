terraform {
  required_version = ">= 1.4.7"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.31.0"
    }
  }

  backend "s3" {
    profile        = "study"
    bucket         = "study-terraform-states"
    key            = "study_cluster_nikita.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
  }
}

provider "aws" {
  profile = "study"
  region  = "us-east-1"


  default_tags {
    tags = {
      Name = "create-by-terraform-EKS-Demo-need-tag"
    }
  }
}