resource "azurerm_service_plan" "wordle_appplan" {
  name                = "${var.app_service_name}_plan"
  location            = var.region
  resource_group_name = azurerm_resource_group.rg.name
  sku_name            = var.app_service_sku
  os_type             = "Linux"
}


resource "azurerm_app_service" "wordle_appservice" {
  name                = var.app_service_name
  location            = var.region
  resource_group_name = azurerm_resource_group.rg.name
  app_service_plan_id = azurerm_service_plan.wordle_appplan.id

  site_config {
    linux_fx_version = "DOCKER|${azurerm_container_registry.containerregistry.login_server}/wordlesolver:latest"
  }

  app_settings = {
    "DOCKER_REGISTRY_SERVER_URL"      = "https://${azurerm_container_registry.containerregistry.login_server}"
    "DOCKER_REGISTRY_SERVER_USERNAME" = azurerm_container_registry.containerregistry.admin_username
    "DOCKER_REGISTRY_SERVER_PASSWORD" = azurerm_container_registry.containerregistry.admin_password
  }
}