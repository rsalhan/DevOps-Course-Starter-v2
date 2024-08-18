terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = ">= 3.8"
    }
  }
  backend "azurerm" {
    resource_group_name  = "Cohort28_RajSal_ProjectExercise"
    storage_account_name = "rsm12st01"
    container_name       = "rsm12st01container"
    key                  = "terraform.tfstate"
    }
}

provider "azurerm" {
  features {}
}

data "azurerm_resource_group" "main" {
  name     = "Cohort28_RajSal_ProjectExercise"
}

# AppServicePlan
resource "azurerm_service_plan" "main" {
  name                = "terraformed-asp"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  os_type             = "Linux"
  sku_name            = "B1"
}

# AppService
resource "azurerm_linux_web_app" "main" {
  name                = "rs-m12-app"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  service_plan_id     = azurerm_service_plan.main.id

  site_config {
    application_stack {
      # docker_image     = "rsalhan/m8-todo-app"
      # docker_image_tag = "prod"
      docker_image_name = "rsalhan/m8-todo-app:prod"
      docker_registry_url = "https://index.docker.io"
    }
  }

  app_settings = {
    "DOCKER_REGISTRY_SERVER_URL" = "https://docker.io"
    "FLASK_APP" = "todo_app/app"
    "FLASK_DEBUG" = "true"
    "OAUTH_CLIENT_ID" = var.OAUTH_CLIENT_ID
    "OAUTH_CLIENT_SECRET" = var.OAUTH_CLIENT_SECRET
    "SECRET_KEY" = var.SECRET_KEY
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "false"
    "WEBSITES_PORT" = "8000"
    "MONGO_DB_CONNECTION_STRING" = azurerm_cosmosdb_account.main.primary_mongodb_connection_string
    "MONGO_DB_NAME" = "db01"
  }
}

# Cosmos DB Account
resource "azurerm_cosmosdb_account" "main" {
  name                = "terraformed-cosmos-db-m12"
  location            = data.azurerm_resource_group.main.location 
  resource_group_name = data.azurerm_resource_group.main.name
  offer_type          = "Standard"
  kind                = "MongoDB"

  enable_automatic_failover = false

  capabilities {
      name = "EnableServerless"
  }

  capabilities {
    name = "EnableAggregationPipeline"
  }

  capabilities {
    name = "mongoEnableDocLevelTTL"
  }

  capabilities {
    name = "MongoDBv3.4"
  }

  capabilities {
    name = "EnableMongo"
  }

  lifecycle { prevent_destroy = true }

  consistency_policy {
    consistency_level       = "BoundedStaleness"
    max_interval_in_seconds = 300
    max_staleness_prefix    = 100000
  }

  geo_location {
    location          = "uksouth"
    failover_priority = 0
  }
}

# Cosmos DB
resource "azurerm_cosmosdb_mongo_database" "main" {
  name                = "terraformed-cosmos-mongo-db-m12"
  resource_group_name = data.azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
}
