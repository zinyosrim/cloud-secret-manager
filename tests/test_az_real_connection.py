import unittest
from cloudsecretmanager.azure import AzureKeyVaultManager


class TestAzureKeyVaultManager(unittest.TestCase):
    def setUp(self):
        self.vault_url = "https://dc-testing-keyvault.vault.azure.net"
        self.secret_id = "test-secret"
        self.payload = "test-payload"

        # Initialize the AzureKeyVaultManager
        self.manager = AzureKeyVaultManager(self.vault_url)

    def test_create_and_get_secret(self):
        # Test create method
        self.manager.create(secret_id=self.secret_id, payload=self.payload)

        # Test get method
        result = self.manager.get(secret_id=self.secret_id)

        # Assert
        self.assertEqual(result, self.payload)


if __name__ == "__main__":
    unittest.main()
