# Define the Helm provider configuration to use the newly created AKS cluster
provider "helm" {
  kubernetes {
    host                   = azurerm_kubernetes_cluster.aks.kube_config.0.host
    client_certificate     = base64decode(azurerm_kubernetes_cluster.aks.kube_config.0.client_certificate)
    client_key             = base64decode(azurerm_kubernetes_cluster.aks.kube_config.0.client_key)
    cluster_ca_certificate = base64decode(azurerm_kubernetes_cluster.aks.kube_config.0.cluster_ca_certificate)
  }
}

# Deploy the local Helm chart to the AKS cluster
resource "helm_release" "practice_api" {
  name       = "practice-api-prod"
  chart      = "../helm/practice-api"  # Path to your local Helm chart
  namespace  = "default"

  # Pass the values-prod.yaml to simulate the production deployment
  values = [
    file("../helm/practice-api/values-prod.yaml")
  ]

  # Ensure the cluster exists before deploying the helm chart
  depends_on = [
    azurerm_kubernetes_cluster.aks
  ]
}
