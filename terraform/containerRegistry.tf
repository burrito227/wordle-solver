resource "azurerm_container_registry" "containerregistry" {
  name                = var.container_registry_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = var.region
  sku                 = "Basic"
  admin_enabled       = true
}