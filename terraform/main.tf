# Configure the Azure provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0.2"
    }
  }

  required_version = ">= 1.1.0"

  backend "azurerm" {
    resource_group_name  = "wordle-solver-dev"
    storage_account_name = "wordlesa"
    container_name       = "terraform"
    key                  = "wordle.tfstate"
    use_oidc             = true
  }
}

provider "azurerm" {
  features {}
}