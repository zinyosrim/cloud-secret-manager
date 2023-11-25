import unittest
from unittest.mock import patch, Mock
from cloudsecretmanager.gcp import GCPSecretManager
from google.api_core.exceptions import NotFound


class TestGCPSecretManager(unittest.TestCase):
    def setUp(self):
        self.project_id = "test-project"
        self.secret_id = "test-secret"
        self.payload = "test-payload"

        # Initialize the GCPSecretManager
        self.manager = GCPSecretManager(self.project_id)

    @patch("cloudsecretmanager.gcp.secretmanager.SecretManagerServiceClient")
    def test_create_secret(self, mock_client):
        # Setup mock
        mock_client_instance = mock_client.return_value
        mock_client_instance.get_secret.side_effect = NotFound("not found")

        # Test create method
        self.manager.create(secret_id=self.secret_id, payload=self.payload)

        # Assert
        mock_client_instance.create_secret.assert_called()
        mock_client_instance.add_secret_version.assert_called_with(
            request={
                "parent": f"projects/{self.project_id}/secrets/{self.secret_id}",
                "payload": {"data": self.payload.encode("UTF-8")},
            }
        )

    @patch("cloudsecretmanager.gcp.secretmanager.SecretManagerServiceClient")
    def test_get_secret(self, mock_client):
        # Setup mock
        mock_client_instance = mock_client.return_value
        mock_response = Mock()
        mock_response.payload.data = self.payload.encode("UTF-8")
        mock_client_instance.access_secret_version.return_value = mock_response

        # Test get method
        result = self.manager.get(secret_id=self.secret_id)

        # Assert
        self.assertEqual(result, self.payload)


if __name__ == "__main__":
    unittest.main()
