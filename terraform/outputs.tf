output "cr_admin_username" {
  value = azurerm_container_registry.containerregistry.admin_username
}

output "cr_admin_password" {
  value     = azurerm_container_registry.containerregistry.admin_password
  sensitive = true
}

output "acr_login_server" {
  value       = azurerm_container_registry.containerregistry.login_server
  description = "The login server of the Azure Container Registry"
}

output "db_admin_password" {
  value     = data.azurerm_key_vault_secret.sql_admin_password.value
  sensitive = true
}

output "django_secret_key" {
  value     = data.azurerm_key_vault_secret.django_secret_key.value
  sensitive = true
}

output "rg" {
  value = var.rg
}

# output "webapp_name" {
#   value = var.app_service_name
# }