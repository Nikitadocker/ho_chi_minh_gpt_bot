terraform {
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }

  # backend "s3" {
  #   endpoint                    = "https://bucketsave.blr1.digitaloceanspaces.com"
  #   key                         = "terraform.tfstate"
  #   bucket                      = "bucketsave"
  #   # region                      = "blr1"
  #   skip_credentials_validation = true
  #   skip_metadata_api_check     = true
   
  # }


}



# Configure the DigitalOcean Provider
provider "digitalocean" {
  token = var.do_token
  spaces_access_id  = var.access_id
  spaces_secret_key = var.secret_key
}



