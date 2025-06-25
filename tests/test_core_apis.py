"""Tests for core API endpoints."""

import os
from unittest.mock import Mock, patch

import pytest
import requests

from open_to_close import OpenToCloseAPI
from open_to_close.exceptions import AuthenticationError


@pytest.fixture
def client() -> OpenToCloseAPI:
    """Create a test client."""
    return OpenToCloseAPI(api_key="test_key")


@pytest.fixture
def mock_response() -> Mock:
    """Create a mock response."""
    response = Mock(spec=requests.Response)
    response.status_code = 200
    response.json.return_value = {"id": 1, "name": "Test"}
    response.headers = {}
    return response


class TestAgentsAPI:
    """Test AgentsAPI functionality."""

    def test_agents_initialization(self, client: OpenToCloseAPI) -> None:
        """Test that agents API can be initialized."""
        agents = client.agents
        assert agents is not None
        assert hasattr(agents, "list_agents")

    @patch("open_to_close.base_client.requests.Session.request")
    def test_list_agents(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_response: Mock
    ) -> None:
        """Test listing agents."""
        mock_request.return_value = mock_response
        mock_response.json.return_value = [{"id": 1, "name": "John Agent"}]

        agents = client.agents.list_agents()

        assert isinstance(agents, list)
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_create_agent(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_response: Mock
    ) -> None:
        """Test creating an agent."""
        mock_request.return_value = mock_response
        mock_response.json.return_value = {
            "id": 1,
            "name": "John Agent",
            "email": "john@example.com",
        }

        agent_data = {
            "name": "John Agent",
            "email": "john@example.com",
            "phone": "+1234567890",
        }
        agent = client.agents.create_agent(agent_data)

        assert isinstance(agent, dict)
        assert agent.get("id") == 1
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_retrieve_agent(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_response: Mock
    ) -> None:
        """Test retrieving an agent."""
        mock_request.return_value = mock_response
        mock_response.json.return_value = {"id": 1, "name": "John Agent"}

        agent = client.agents.retrieve_agent(1)

        assert isinstance(agent, dict)
        assert agent.get("id") == 1
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_update_agent(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_response: Mock
    ) -> None:
        """Test updating an agent."""
        mock_request.return_value = mock_response
        mock_response.json.return_value = {"id": 1, "name": "Jane Agent"}

        update_data = {"name": "Jane Agent"}
        agent = client.agents.update_agent(1, update_data)

        assert isinstance(agent, dict)
        assert agent.get("id") == 1
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_delete_agent(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_response: Mock
    ) -> None:
        """Test deleting an agent."""
        mock_request.return_value = mock_response
        mock_response.status_code = 204
        mock_response.json.return_value = {}

        result = client.agents.delete_agent(1)

        assert isinstance(result, dict)
        mock_request.assert_called_once()


class TestContactsAPI:
    """Test ContactsAPI functionality."""

    def test_contacts_initialization(self, client: OpenToCloseAPI) -> None:
        """Test that contacts API can be initialized."""
        contacts = client.contacts
        assert contacts is not None
        assert hasattr(contacts, "list_contacts")

    @patch("open_to_close.base_client.requests.Session.request")
    def test_list_contacts(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_response: Mock
    ) -> None:
        """Test listing contacts."""
        mock_request.return_value = mock_response
        mock_response.json.return_value = [{"id": 1, "name": "John Contact"}]

        contacts = client.contacts.list_contacts()

        assert isinstance(contacts, list)
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_create_contact(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_response: Mock
    ) -> None:
        """Test creating a contact."""
        mock_request.return_value = mock_response
        mock_response.json.return_value = {
            "id": 1,
            "name": "John Contact",
            "email": "john@example.com",
        }

        contact_data = {
            "first_name": "John",
            "last_name": "Contact",
            "email": "john@example.com",
            "phone": "+1234567890",
        }
        contact = client.contacts.create_contact(contact_data)

        assert isinstance(contact, dict)
        assert contact.get("id") == 1
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_retrieve_contact(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_response: Mock
    ) -> None:
        """Test retrieving a contact."""
        mock_request.return_value = mock_response
        mock_response.json.return_value = {"id": 1, "name": "John Contact"}

        contact = client.contacts.retrieve_contact(1)

        assert isinstance(contact, dict)
        assert contact.get("id") == 1
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_update_contact(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_response: Mock
    ) -> None:
        """Test updating a contact."""
        mock_request.return_value = mock_response
        mock_response.json.return_value = {"id": 1, "name": "Jane Contact"}

        update_data = {"first_name": "Jane", "last_name": "Contact"}
        contact = client.contacts.update_contact(1, update_data)

        assert isinstance(contact, dict)
        assert contact.get("id") == 1
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_delete_contact(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_response: Mock
    ) -> None:
        """Test deleting a contact."""
        mock_request.return_value = mock_response
        mock_response.status_code = 204
        mock_response.json.return_value = {}

        result = client.contacts.delete_contact(1)

        assert isinstance(result, dict)
        mock_request.assert_called_once()


class TestPropertiesAPI:
    """Test PropertiesAPI functionality."""

    def test_properties_initialization(self, client: OpenToCloseAPI) -> None:
        """Test that properties API can be initialized."""
        properties = client.properties
        assert properties is not None
        assert hasattr(properties, "list_properties")

    @patch("open_to_close.base_client.requests.Session.request")
    def test_list_properties(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_response: Mock
    ) -> None:
        """Test listing properties."""
        mock_request.return_value = mock_response
        mock_response.json.return_value = [{"id": 1, "address": "123 Main St"}]

        properties = client.properties.list_properties()

        assert isinstance(properties, list)
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_create_property(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_response: Mock
    ) -> None:
        """Test creating a property."""
        # Mock field mappings request
        field_mappings_response = Mock(spec=requests.Response)
        field_mappings_response.status_code = 200
        field_mappings_response.json.return_value = [
            {
                "group": {
                    "title": "Property Details",
                    "sections": [
                        {
                            "section": {
                                "title": "Basic Info",
                                "fields": [
                                    {
                                        "id": 926565,
                                        "key": "contract_title",
                                        "title": "Contract Title",
                                        "type": "text",
                                    },
                                    {
                                        "id": 926553,
                                        "key": "contract_client_type",
                                        "title": "Contract Client Type",
                                        "type": "choice",
                                        "options": [
                                            {"id": 797212, "title": "buyer"},
                                            {"id": 797213, "title": "seller"},
                                            {"id": 797214, "title": "dual"},
                                        ],
                                    },
                                    {
                                        "id": 926552,
                                        "key": "contract_status",
                                        "title": "Contract Status",
                                        "type": "choice",
                                        "options": [
                                            {"id": 797206, "title": "listing- active"},
                                            {"id": 797207, "title": "under contract"},
                                            {"id": 797210, "title": "closed"},
                                        ],
                                    },
                                ],
                            }
                        }
                    ],
                }
            }
        ]
        field_mappings_response.headers = {}

        # Mock teams request (for team member auto-detection)
        teams_response = Mock(spec=requests.Response)
        teams_response.status_code = 200
        teams_response.json.return_value = [
            {"team_members": [{"id": 26392, "name": "Test Member"}]}
        ]
        teams_response.headers = {}

        # Mock property creation request
        property_response = Mock(spec=requests.Response)
        property_response.status_code = 201
        property_response.json.return_value = {
            "id": 1,
            "address": "123 Main St",
            "price": 500000,
        }
        property_response.headers = {}

        # Configure mock to return different responses for different URLs
        mock_request.side_effect = [
            field_mappings_response,
            teams_response,
            property_response,
        ]

        property_data = {
            "contract_title": "Test Property Contract",
            "address": "123 Main St, City, ST 12345",
            "price": 500000,
            "bedrooms": 3,
            "bathrooms": 2,
        }
        property = client.properties.create_property(property_data)

        assert isinstance(property, dict)
        assert property.get("id") == 1
        # Expect 3 calls: 1 for field mappings, 1 for teams (auto-detection) and 1 for property creation
        assert mock_request.call_count == 3

    @patch("open_to_close.base_client.requests.Session.request")
    def test_retrieve_property(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_response: Mock
    ) -> None:
        """Test retrieving a property."""
        mock_request.return_value = mock_response
        mock_response.json.return_value = {"id": 1, "address": "123 Main St"}

        property = client.properties.retrieve_property(1)

        assert isinstance(property, dict)
        assert property.get("id") == 1
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_update_property(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_response: Mock
    ) -> None:
        """Test updating a property."""
        mock_request.return_value = mock_response
        mock_response.json.return_value = {"id": 1, "price": 550000, "status": "sold"}

        update_data = {"price": 550000, "status": "sold"}
        property = client.properties.update_property(1, update_data)

        assert isinstance(property, dict)
        assert property.get("id") == 1
        mock_request.assert_called_once()

    @patch("open_to_close.base_client.requests.Session.request")
    def test_delete_property(
        self, mock_request: Mock, client: OpenToCloseAPI, mock_response: Mock
    ) -> None:
        """Test deleting a property."""
        mock_request.return_value = mock_response
        mock_response.status_code = 204
        mock_response.json.return_value = {}

        result = client.properties.delete_property(1)

        assert isinstance(result, dict)
        mock_request.assert_called_once()


class TestClientIntegration:
    """Integration tests for the main client."""

    def test_client_initialization_with_api_key(self) -> None:
        """Test client initialization with API key."""
        client = OpenToCloseAPI(api_key="test_key")
        assert client._api_key == "test_key"

    @patch.dict("os.environ", {}, clear=True)
    def test_client_initialization_without_api_key_raises_error(self) -> None:
        """Test that client raises error without API key when accessing resources."""
        client = OpenToCloseAPI(api_key=None)
        # The error should be raised when trying to access a resource that initializes BaseClient
        with pytest.raises(AuthenticationError, match="API key is required"):
            client.agents.list_agents()

    def test_all_api_properties_accessible(self, client: OpenToCloseAPI) -> None:
        """Test that all API properties are accessible."""
        assert client.agents is not None
        assert client.contacts is not None
        assert client.properties is not None
        assert client.property_contacts is not None
        assert client.property_documents is not None
        assert client.property_emails is not None
        assert client.property_notes is not None
        assert client.property_tasks is not None
        assert client.tags is not None
        assert client.teams is not None
        assert client.users is not None

    def test_lazy_initialization(self, client: OpenToCloseAPI) -> None:
        """Test that API clients are lazily initialized."""
        # Initially, the private attributes should be None
        assert client._agents is None
        assert client._contacts is None

        # After accessing the property, they should be initialized
        agents = client.agents
        contacts = client.contacts

        assert client._agents is not None
        assert client._contacts is not None
        assert agents is client._agents
        assert contacts is client._contacts

    def test_base_client_inheritance(self, client: OpenToCloseAPI) -> None:
        """Test that all API clients inherit from BaseClient."""
        from open_to_close.base_client import BaseClient

        assert isinstance(client.agents, BaseClient)
        assert isinstance(client.contacts, BaseClient)
        assert isinstance(client.properties, BaseClient)
        assert isinstance(client.property_contacts, BaseClient)
        assert isinstance(client.property_documents, BaseClient)
        assert isinstance(client.property_emails, BaseClient)
        assert isinstance(client.property_notes, BaseClient)
        assert isinstance(client.property_tasks, BaseClient)
