# =============================================================================
# General Variables
# =============================================================================
rg     = "wordle-solver-dev"
region = "westus2"
tags = {
  provisioning_mode = "terraform",
  project           = "wordle-solver",
  environment_owner = "Gabriel Saenz"
}

# =============================================================================
# Key Vault
# =============================================================================
keyvault_name = "wordlesolverkv"
keyvault_rg   = "wordle-solver-dev"

# =============================================================================
# SQL
# =============================================================================
sqlserver_name = "wordlesql-server"
sqldb_name     = "wordle-database"
admin_username = "vaderalligator"

# =============================================================================
# Container Registry
# =============================================================================
container_registry_name = "wordlesolvercr"

# =============================================================================
# Web app
# =============================================================================
app_service_name = "wordle-solver-ejedfvcrd3f9dmd8"
app_service_sku  = "B1"