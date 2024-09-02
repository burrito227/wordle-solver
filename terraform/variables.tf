# =============================================================================
# General Variables
# =============================================================================
variable "rg" {
  description = "Resource group name."
  type        = string
}

variable "region" {
  description = "Region for all resources."
  type        = string
}

variable "tags" {
  description = "Resource tags"
  type        = map(string)
}

# =============================================================================
# Key Vault
# =============================================================================
variable "keyvault_name" {
  description = "Resource name of the key vault to store secrets."
  type        = string
}

variable "keyvault_rg" {
  description = "RG that stores the keyvault"
  type        = string
}

# =============================================================================
# SQL
# =============================================================================
variable "sqlserver_name" {
  description = "name of the SQL database"
  type        = string
}

variable "sqldb_name" {
  description = "name of the SQL database"
  type        = string
}

variable "admin_username" {
  description = "username for admin access to sql DB."
  type        = string
}

# =============================================================================
# Container Registry
# =============================================================================
variable "container_registry_name" {
  description = "name of the container registry resource"
  type        = string
}

# =============================================================================
# Web app
# =============================================================================
variable "app_service_name" {
  description = "The name of the web app"
  type        = string
}

variable "app_service_sku" {
  description = "The sku of the web app"
  type        = string
}