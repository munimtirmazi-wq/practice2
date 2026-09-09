resource "azurerm_resource_group" "rg" {
  name     = "rg-practice-api"
  location = "East US"
}

resource "azurerm_kubernetes_cluster" "aks" {
  name                = "aks-practice-api"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = "practice-api"

  oidc_issuer_enabled       = true
  workload_identity_enabled = true

  default_node_pool {
    name       = "default"
    node_count = 1
    vm_size    = "Standard_D2as_v7" # Picked from allowed SKUs for this subscription
  }

  identity {
    type = "SystemAssigned"
  }

  tags = {
    Environment = "Production"
  }
}
