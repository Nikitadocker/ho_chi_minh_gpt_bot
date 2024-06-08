resource "digitalocean_spaces_bucket" "bucket_state" {
  name   = "bucketsave"
  region = "blr1"
}