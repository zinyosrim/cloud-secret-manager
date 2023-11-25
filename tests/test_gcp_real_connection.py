import unittest
from cloudsecretmanager.gcp import GCPSecretManager


class TestGCPSecretManagerRealConnection(unittest.TestCase):
    def setUp(self):
        # You should replace 'your-gcp-project-id' with your actual GCP project ID
        self.project_id = "your-gcp-project-id"
        self.secret_id = "test-secret"
        self.payload = "test-payload"

        # Initialize the GCPSecretManager
        self.manager = GCPSecretManager(self.project_id)

    def test_create_and_get_secret(self):
        # Test create method
        self.manager.create(secret_id=self.secret_id, payload=self.payload)

        # Test get method
        result = self.manager.get(secret_id=self.secret_id)

        # Assert
        self.assertEqual(result, self.payload)


if __name__ == "__main__":
    unittest.main()
