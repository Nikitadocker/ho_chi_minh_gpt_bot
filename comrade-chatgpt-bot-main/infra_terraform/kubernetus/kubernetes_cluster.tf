resource "digitalocean_kubernetes_cluster" "cluster_for_bot" {
  name   = "cluster-bot"
  region = "blr1"
  # Grab the latest version slug from `doctl kubernetes options versions`
  version = "1.30.1-do.0"
  auto_upgrade = "false"

  node_pool {
    name       = "worker-pool"
    size       = "s-2vcpu-4gb"
    node_count = 1

  }
}

output "k8s_config" {
  value =  digitalocean_kubernetes_cluster.cluster_for_bot.kube_config.0.raw_config
  sensitive = true
}
# данный output предназначен для работы с value в cli
# выполнив  echo "$(terraform output k8s_config) вы увидите kubeconfig для кластера
# выполнив echo "$(terraform output k8s_config) >> kubeconfig.yaml вы создатите файл для кластера

