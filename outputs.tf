output "webapp_url" {
  value = "https://${azurerm_linux_web_app.main.default_hostname}"
}

output "cosmosdb_connection_string" {
  value = azurerm_cosmosdb_account.main.primary_mongodb_connection_string
  sensitive = true
}

output "webhook_url" {
  value = "https://${azurerm_linux_web_app.main.site_credential[0].name}:${azurerm_linux_web_app.main.site_credential[0].password}@${azurerm_linux_web_app.main.name}.scm.azurewebsites.net/docker/hook"
  sensitive = true
}