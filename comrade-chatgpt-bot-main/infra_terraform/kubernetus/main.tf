terraform {
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }

  backend "s3" {
    endpoint                    = "projectbucket.blr1.digitaloceanspaces.com"
    key                         = "terraform.tfstate"
    bucket                      = "projectbucket"
    region                      = "nyc3"
    skip_credentials_validation = true
    skip_metadata_api_check     = true
   
  }


}



# Configure the DigitalOcean Provider
provider "digitalocean" {
  token = var.do_token
}



