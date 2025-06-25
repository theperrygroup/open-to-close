from typing import Any, Dict, List, Optional, Tuple

from .agents import AgentsAPI
from .base_client import DEFAULT_BASE_URL
from .contacts import ContactsAPI
from .properties import PropertiesAPI
from .property_contacts import PropertyContactsAPI
from .property_documents import PropertyDocumentsAPI
from .property_emails import PropertyEmailsAPI
from .property_notes import PropertyNotesAPI
from .property_tasks import PropertyTasksAPI
from .tags import TagsAPI
from .teams import TeamsAPI
from .users import UsersAPI


class OpenToCloseAPI:
    """Main client for Open To Close API.

    This client provides access to all Open To Close API endpoints through
    service-specific clients using a composition pattern with lazy initialization.

    Example:
        ```python
        from open_to_close_api import OpenToCloseAPI

        # Initialize with API key from environment variable
        client = OpenToCloseAPI()

        # Or provide API key directly
        client = OpenToCloseAPI(api_key="your_api_key_here")

        # Use service endpoints
        agents = client.agents.list_agents()
        agent = client.agents.retrieve_agent(1)

        # Create a new contact
        contact = client.contacts.create_contact({
            "name": "John Doe",
            "email": "john@example.com"
        })
        ```
    """

    def __init__(
        self, api_key: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Initialize the client.

        Args:
            api_key: API key for authentication. If not provided, it will
                     attempt to load it from the OPEN_TO_CLOSE_API_KEY environment
                     variable.
            base_url: Base URL for the Open To Close API. Defaults to
                      https://api.opentoclose.com/v1

        Raises:
            AuthenticationError: If API key is not provided and not found in environment
        """
        self._api_key = api_key
        self._base_url = base_url or DEFAULT_BASE_URL

        # Lazy initialization of service clients
        self._agents: Optional[AgentsAPI] = None
        self._contacts: Optional[ContactsAPI] = None
        self._properties: Optional[PropertiesAPI] = None
        self._property_contacts: Optional[PropertyContactsAPI] = None
        self._property_documents: Optional[PropertyDocumentsAPI] = None
        self._property_emails: Optional[PropertyEmailsAPI] = None
        self._property_notes: Optional[PropertyNotesAPI] = None
        self._property_tasks: Optional[PropertyTasksAPI] = None
        self._tags: Optional[TagsAPI] = None
        self._teams: Optional[TeamsAPI] = None
        self._users: Optional[UsersAPI] = None

    @property
    def agents(self) -> AgentsAPI:
        """Access to agents endpoints.

        Returns:
            AgentsAPI instance for managing agents
        """
        if self._agents is None:
            self._agents = AgentsAPI(api_key=self._api_key, base_url=self._base_url)
        return self._agents

    @property
    def contacts(self) -> ContactsAPI:
        """Access to contacts endpoints.

        Returns:
            ContactsAPI instance for managing contacts
        """
        if self._contacts is None:
            self._contacts = ContactsAPI(api_key=self._api_key, base_url=self._base_url)
        return self._contacts

    @property
    def properties(self) -> PropertiesAPI:
        """Access to properties endpoints.

        Returns:
            PropertiesAPI instance for managing properties
        """
        if self._properties is None:
            self._properties = PropertiesAPI(
                api_key=self._api_key, base_url=self._base_url
            )
        return self._properties

    @property
    def property_contacts(self) -> PropertyContactsAPI:
        """Access to property contacts endpoints.

        Returns:
            PropertyContactsAPI instance for managing property contacts
        """
        if self._property_contacts is None:
            self._property_contacts = PropertyContactsAPI(
                api_key=self._api_key, base_url=self._base_url
            )
        return self._property_contacts

    @property
    def property_documents(self) -> PropertyDocumentsAPI:
        """Access to property documents endpoints.

        Returns:
            PropertyDocumentsAPI instance for managing property documents
        """
        if self._property_documents is None:
            self._property_documents = PropertyDocumentsAPI(
                api_key=self._api_key, base_url=self._base_url
            )
        return self._property_documents

    @property
    def property_emails(self) -> PropertyEmailsAPI:
        """Access to property emails endpoints.

        Returns:
            PropertyEmailsAPI instance for managing property emails
        """
        if self._property_emails is None:
            self._property_emails = PropertyEmailsAPI(
                api_key=self._api_key, base_url=self._base_url
            )
        return self._property_emails

    @property
    def property_notes(self) -> PropertyNotesAPI:
        """Access to property notes endpoints.

        Returns:
            PropertyNotesAPI instance for managing property notes
        """
        if self._property_notes is None:
            self._property_notes = PropertyNotesAPI(
                api_key=self._api_key, base_url=self._base_url
            )
        return self._property_notes

    @property
    def property_tasks(self) -> PropertyTasksAPI:
        """Access to property tasks endpoints.

        Returns:
            PropertyTasksAPI instance for managing property tasks
        """
        if self._property_tasks is None:
            self._property_tasks = PropertyTasksAPI(
                api_key=self._api_key, base_url=self._base_url
            )
        return self._property_tasks

    @property
    def tags(self) -> TagsAPI:
        """Access to tags endpoints.

        Returns:
            TagsAPI instance for managing tags
        """
        if self._tags is None:
            self._tags = TagsAPI(api_key=self._api_key, base_url=self._base_url)
        return self._tags

    @property
    def teams(self) -> TeamsAPI:
        """Access to teams endpoints.

        Returns:
            TeamsAPI instance for managing teams
        """
        if self._teams is None:
            self._teams = TeamsAPI(api_key=self._api_key, base_url=self._base_url)
        return self._teams

    @property
    def users(self) -> UsersAPI:
        """Access to users endpoints.

        Returns:
            UsersAPI instance for managing users
        """
        if self._users is None:
            self._users = UsersAPI(api_key=self._api_key, base_url=self._base_url)
        return self._users

    def get_property_fields(self) -> List[Dict[str, Any]]:
        """Convenience method to retrieve property field definitions.

        This is a convenience method that delegates to the properties API
        to fetch property field definitions. It's equivalent to calling
        client.properties.get_property_fields().

        Returns:
            A list of dictionaries containing property field definitions.
            Each field group contains sections with individual field definitions
            including field name, type, options (for choice fields), and other metadata.

        Raises:
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            # Get property field definitions directly from main client
            client = OpenToCloseAPI()
            fields = client.get_property_fields()

            # This is equivalent to:
            # fields = client.properties.get_property_fields()

            # Analyze field groups
            for group in fields:
                if 'group' in group:
                    print(f"Group: {group['group']['title']}")
            ```
        """
        return self.properties.get_property_fields()

    def list_available_fields(self) -> List[Dict[str, Any]]:
        """List all available property fields with their IDs and metadata.

        Returns:
            List of field information dictionaries containing:
            - name: Field key/name
            - id: Field ID
            - type: Field type (text, choice, date, etc.)
            - title: Human-readable field title
            - required: Whether field is required
            - options: For choice fields, available options

        Example:
            ```python
            client = OpenToCloseAPI()
            fields = client.list_available_fields()

            for field in fields[:5]:  # Show first 5 fields
                print(f"{field['name']} ({field['type']}): {field['title']}")
                if field.get('required'):
                    print("  *REQUIRED*")
                if field.get('options'):
                    print(f"  Options: {', '.join(field['options'])}")
            ```
        """
        mappings = self.properties.get_field_mappings()
        required_fields = ["contract_title", "contract_client_type", "contract_status"]

        fields = []
        for field_key, mapping in mappings.items():
            field_info = {
                "name": field_key,
                "id": mapping["id"],
                "type": mapping["type"],
                "title": mapping.get("title", field_key),
                "required": field_key in required_fields,
            }

            # For choice fields, extract option names
            if "options" in mapping:
                # Get unique option names (excluding variations with hyphens)
                option_names = [
                    k
                    for k in mapping["options"].keys()
                    if "-" not in k or k.startswith("listing")
                ]
                field_info["options"] = sorted(set(option_names))

            fields.append(field_info)

        # Sort by required first, then by name
        return sorted(fields, key=lambda x: (not x["required"], x["name"]))

    def validate_property_data(
        self, property_data: Dict[str, Any]
    ) -> Tuple[bool, List[str]]:
        """Validate property data before submission.

        Args:
            property_data: Property data dictionary to validate

        Returns:
            Tuple of (is_valid, errors) where errors is a list of error messages

        Example:
            ```python
            client = OpenToCloseAPI()

            property_data = {
                "title": "Test Property",
                "client_type": "InvalidType",  # This will cause an error
                "status": "Active"
            }

            is_valid, errors = client.validate_property_data(property_data)
            if not is_valid:
                for error in errors:
                    print(f"Error: {error}")
            else:
                property = client.properties.create_property(property_data)
            ```
        """
        errors = []
        mappings = self.properties.get_field_mappings()

        # Required fields
        required_fields = {
            "contract_title": ["title", "contract_title"],
            "contract_client_type": ["client_type", "contract_client_type"],
            "contract_status": ["status", "contract_status"],
        }

        # Check required fields
        for field_key, aliases in required_fields.items():
            found = False
            for alias in aliases:
                if alias in property_data and property_data[alias]:
                    found = True
                    break
            if not found:
                errors.append(
                    f"Missing required field: {field_key} (use any of: {', '.join(aliases)})"
                )

        # Validate field values
        for key, value in property_data.items():
            # Check if field exists in mappings
            if key not in mappings:
                # Check if it's an alias for a required field
                is_alias = False
                for field_key, aliases in required_fields.items():
                    if key in aliases:
                        is_alias = True
                        # Use the actual field key for validation
                        key = field_key
                        break

                if not is_alias:
                    errors.append(f"Unknown field: {key}")
                    continue

            field_mapping = mappings.get(key)
            if not field_mapping:
                continue

            # Validate choice fields
            if field_mapping["type"] == "choice" and "options" in field_mapping:
                if isinstance(value, str):
                    # Check if value is valid
                    valid_options = list(field_mapping["options"].keys())
                    if value.lower() not in field_mapping["options"]:
                        # Show only primary option names
                        display_options = [
                            opt
                            for opt in valid_options
                            if "-" not in opt or opt.startswith("listing")
                        ]
                        errors.append(
                            f"Invalid value '{value}' for field '{key}'. "
                            f"Valid options: {', '.join(sorted(set(display_options)))}"
                        )

        return (len(errors) == 0, errors)
