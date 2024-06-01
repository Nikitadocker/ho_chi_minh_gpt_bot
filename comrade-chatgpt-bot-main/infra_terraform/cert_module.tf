module "cert_manager" {
  source  = "terraform-iaac/cert-manager/kubernetes"
  version = "2.6.3"
  cluster_issuer_email                   = "neketa51993@gmail.com"
  cluster_issuer_name                    = "letsencrypt-prod"
  cluster_issuer_private_key_secret_name = "cert-manager-private-key"
  namespace_name = "cert-manager"
  create_namespace	= "true"
}