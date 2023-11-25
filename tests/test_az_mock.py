import unittest
from unittest.mock import Mock, patch
from cloudsecretmanager.azure import AzureKeyVaultManager

VAULT_URL = "https://customer-clustering-kv.vault.azure.net"


class TestAzureKeyVaultManager(unittest.TestCase):
    def setUp(self):
        self.vault_url = "https://dc-testing-keyvault.vault.azure.net"
        self.secret_id = "test-secret"
        self.payload = "test-payload"
        # Initialize the AzureKeyVaultManager
        self.manager = AzureKeyVaultManager(self.vault_url)

    @patch("cloudsecretmanager.az.SecretClient")
    def test_create_secret(self, mock_secret_client):
        # Setup
        manager = AzureKeyVaultManager(self.vault_url)
        mock_client_instance = mock_secret_client.return_value

        # Test create method
        manager.create(secret_id=self.secret_id, payload=self.payload)

        # Assert
        mock_client_instance.set_secret.assert_called_once_with(
            self.secret_id, self.payload
        )

    @patch("cloudsecretmanager.az.SecretClient")
    def test_get_secret(self, mock_secret_client):
        # Setup

        manager = AzureKeyVaultManager(self.vault_url)
        mock_client_instance = mock_secret_client.return_value
        mock_client_instance.get_secret.return_value = Mock(value=self.payload)

        # Test get method
        result = manager.get(secret_id=self.secret_id)

        # Assert
        mock_client_instance.get_secret.assert_called_once_with(self.secret_id)
        self.assertEqual(result, self.payload)

    @patch("cloudsecretmanager.az.SecretClient")
    def test_get_secret_not_found(self, mock_secret_client):
        # Setup
        manager = AzureKeyVaultManager(self.vault_url)
        mock_client_instance = mock_secret_client.return_value
        mock_client_instance.get_secret.side_effect = Exception("Secret not found")

        # Test get method with exception
        secret_id = "nonexistent-secret"
        result = manager.get(secret_id=secret_id)

        # Assert
        mock_client_instance.get_secret.assert_called_once_with(secret_id)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
