data "azurerm_key_vault" "keyvault" {
  name                = var.keyvault_name
  resource_group_name = var.keyvault_rg

}

data "azurerm_key_vault_secret" "sql_admin_password" {
  name         = "sqladminpassword"
  key_vault_id = data.azurerm_key_vault.keyvault.id
}

data "azurerm_key_vault_secret" "sql_admin" {
  name         = "sqladmin"
  key_vault_id = data.azurerm_key_vault.keyvault.id
}

data "azurerm_key_vault_secret" "django_secret_key" {
  name         = "django-secret-key"
  key_vault_id = data.azurerm_key_vault.keyvault.id
}

data "azurerm_key_vault_secret" "azuread_username" {
  name         = "azureadusername"
  key_vault_id = data.azurerm_key_vault.keyvault.id
}

data "azurerm_key_vault_secret" "azuread_objectid" {
  name         = "azureadobjectid"
  key_vault_id = data.azurerm_key_vault.keyvault.id
}

data "azurerm_key_vault_secret" "azuread_tenantid" {
  name         = "azureadtenantid"
  key_vault_id = data.azurerm_key_vault.keyvault.id
}