"""Properties client for Open To Close API."""

import logging
from typing import Any, Dict, List, Optional, Union

from .base_client import BaseClient
from .exceptions import ValidationError

logger = logging.getLogger(__name__)


class PropertiesAPI(BaseClient):
    """Client for properties API endpoints.

    This client provides methods to manage properties in the Open To Close platform.
    All methods include comprehensive input validation and error handling.
    """

    def __init__(
        self, api_key: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Initialize the properties client.

        Args:
            api_key: API key for authentication
            base_url: Base URL for the API

        Raises:
            AuthenticationError: If API key is missing or invalid
            ConfigurationError: If configuration is invalid
        """
        super().__init__(api_key=api_key, base_url=base_url)
        logger.debug("Initialized PropertiesAPI client")

    def _validate_property_data(
        self, property_data: Dict[str, Any], operation: str
    ) -> None:
        """Validate property data before sending to API.

        Args:
            property_data: Property data to validate
            operation: Operation type for error context (create/update)

        Raises:
            ValidationError: If property data is invalid
        """
        if not isinstance(property_data, dict):
            raise ValidationError(
                f"Property data for {operation} must be a dictionary, got {type(property_data).__name__}"
            )

        if not property_data:
            raise ValidationError(f"Property data for {operation} cannot be empty")

        # Validate required fields for create operations
        if operation == "create":
            # Check for title in different formats
            has_title = False

            # Check traditional field names
            if "contract_title" in property_data or "field_926565" in property_data:
                has_title = True

            # Check fields array format (converted API format)
            elif "fields" in property_data and isinstance(
                property_data["fields"], list
            ):
                for field in property_data["fields"]:
                    if isinstance(field, dict):
                        if (
                            field.get("key") == "contract_title"
                            or field.get("id") == 926565
                        ):
                            has_title = True
                            break

            if not has_title:
                raise ValidationError(
                    f"Property data for {operation} missing required contract title field. "
                    f"Use either 'contract_title' or 'field_926565'"
                )

        # Validate contract_title if provided (both traditional and field ID formats)
        title_fields = ["contract_title", "field_926565"]
        for field_name in title_fields:
            if field_name in property_data:
                title = property_data[field_name]
                if not isinstance(title, str) or len(title.strip()) == 0:
                    raise ValidationError(
                        f"{field_name} must be a non-empty string, got: {title}"
                    )

        # Validate address fields if provided
        address_fields = [
            "property_address",
            "property_city",
            "property_state",
            "property_zip",
        ]
        for field in address_fields:
            if field in property_data:
                value = property_data[field]
                if not isinstance(value, str) or len(value.strip()) == 0:
                    raise ValidationError(
                        f"{field} must be a non-empty string, got: {value}"
                    )

        # Validate numeric fields if provided
        numeric_fields = ["property_price", "sale_price", "list_price"]
        for field in numeric_fields:
            if field in property_data:
                value = property_data[field]
                if value is not None:
                    try:
                        float_value = float(value)
                        if float_value < 0:
                            raise ValidationError(
                                f"{field} must be non-negative, got: {float_value}"
                            )
                    except (ValueError, TypeError):
                        raise ValidationError(
                            f"{field} must be a number, got {type(value).__name__}: {value}"
                        )

        # Validate status if provided
        if "status" in property_data:
            status = property_data["status"]
            if not isinstance(status, str) or len(status.strip()) == 0:
                raise ValidationError(
                    f"status must be a non-empty string, got: {status}"
                )

        logger.debug(f"Property data validated for {operation} operation")

    def _validate_list_params(self, params: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate and normalize parameters for list operations.

        Args:
            params: Parameters to validate

        Returns:
            Validated and normalized parameters

        Raises:
            ValidationError: If parameters are invalid
        """
        if params is None:
            return {}

        if not isinstance(params, dict):
            raise ValidationError(
                f"List parameters must be a dictionary, got {type(params).__name__}"
            )

        validated_params = params.copy()

        # Validate limit parameter
        if "limit" in validated_params:
            limit = validated_params["limit"]
            try:
                limit_int = int(limit)
                if limit_int <= 0:
                    raise ValidationError(
                        f"Limit must be a positive integer, got {limit_int}"
                    )
                if limit_int > 1000:  # Reasonable upper bound
                    logger.warning(
                        f"Large limit value: {limit_int}. Consider using pagination."
                    )
                validated_params["limit"] = limit_int
            except (ValueError, TypeError):
                raise ValidationError(
                    f"Limit must be an integer, got {type(limit).__name__}: {limit}"
                )

        # Validate offset parameter
        if "offset" in validated_params:
            offset = validated_params["offset"]
            try:
                offset_int = int(offset)
                if offset_int < 0:
                    raise ValidationError(
                        f"Offset must be non-negative, got {offset_int}"
                    )
                validated_params["offset"] = offset_int
            except (ValueError, TypeError):
                raise ValidationError(
                    f"Offset must be an integer, got {type(offset).__name__}: {offset}"
                )

        # Validate status filter if provided
        if "status" in validated_params:
            status = validated_params["status"]
            if not isinstance(status, str) or len(status.strip()) == 0:
                raise ValidationError(
                    f"Status filter must be a non-empty string, got: {status}"
                )

        logger.debug("List parameters validated", extra={"params": validated_params})
        return validated_params

    def _get_field_mappings(self) -> Dict[str, Dict[str, Any]]:
        """Get field ID and option mappings for the API.

        Returns:
            Dictionary containing field mappings and option values
        """
        # Use dynamic field mappings from base client
        return self.get_field_mappings()

    def _get_team_member_id(self) -> int:
        """Auto-detect a valid team member ID.

        Returns:
            Team member ID

        Raises:
            ValidationError: If no team members found
        """
        try:
            # Import here to avoid circular imports
            from .teams import TeamsAPI

            teams_client = TeamsAPI(api_key=self.api_key, base_url=self.base_url)
            teams = teams_client.list_teams()

            for team in teams:
                if team.get("team_members"):
                    # Return the first team member ID found
                    return int(team["team_members"][0]["id"])

            raise ValidationError("No team members found in any teams")

        except Exception as e:
            # Fallback to known working team member ID
            logger.warning(f"Could not auto-detect team member, using fallback: {e}")
            return 26392  # John Barry - known working ID

    def _extract_title_from_data(
        self, property_data: Union[str, Dict[str, Any]]
    ) -> str:
        """Extract title from property data for logging.

        Args:
            property_data: Input property data

        Returns:
            Property title
        """
        if isinstance(property_data, str):
            return property_data

        if isinstance(property_data, dict):
            # Check various title fields
            for field in ["title", "contract_title", "field_926565"]:
                if field in property_data:
                    return str(property_data[field])

            # Check fields array
            if "fields" in property_data:
                for field in property_data["fields"]:
                    if isinstance(field, dict):
                        if (
                            field.get("key") == "contract_title"
                            or field.get("id") == 926565
                        ):
                            return str(field.get("value", "Unknown"))

        return "Unknown"

    def _prepare_property_data(
        self,
        property_data: Union[str, Dict[str, Any]],
        team_member_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Convert simple property data format to API format.

        Args:
            property_data: Input data (string or dict)
            team_member_id: Optional team member ID

        Returns:
            API-formatted property data

        Raises:
            ValidationError: If input data is invalid
        """
        # Handle string input (just title)
        if isinstance(property_data, str):
            if not property_data.strip():
                raise ValidationError("Property title cannot be empty")

            return self._build_api_format(
                title=property_data.strip(),
                client_type="Buyer",  # Default for string input
                status="Listing- Active",  # Default for string input
                team_member_id=team_member_id,
            )

        # Handle dictionary input
        if not isinstance(property_data, dict):
            raise ValidationError(
                f"Property data must be string or dict, got {type(property_data).__name__}"
            )

        # If already in API format (has 'fields' key), validate and return
        if "fields" in property_data and "team_member_id" in property_data:
            # Validate existing API format
            if not isinstance(property_data["fields"], list):
                raise ValidationError("API format 'fields' must be a list")
            return property_data.copy()

        # Convert simple format to API format
        return self._convert_simple_to_api_format(property_data, team_member_id)

    def _convert_simple_to_api_format(
        self, simple_data: Dict[str, Any], team_member_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Convert simple dictionary format to API format.

        Args:
            simple_data: Simple property data dictionary
            team_member_id: Optional team member ID

        Returns:
            API-formatted dictionary
        """
        # Get field mappings from API
        field_mappings = self.get_field_mappings()

        # Get team member ID
        if team_member_id is None:
            team_member_id = self._get_team_member_id()

        # Build fields array
        fields = []

        # Define field aliases
        field_aliases = {
            "title": "contract_title",
            "client_type": "contract_client_type",
            "status": "contract_status",
        }

        # Required fields with defaults
        required_defaults = {
            "contract_title": simple_data.get("title")
            or simple_data.get("contract_title"),
            "contract_client_type": simple_data.get("client_type")
            or simple_data.get("contract_client_type", "buyer"),
            "contract_status": simple_data.get("status")
            or simple_data.get("contract_status", "listing- active"),
        }

        # Check for required title
        if not required_defaults["contract_title"]:
            raise ValidationError(
                "Property title is required (use 'title' or 'contract_title' field)"
            )

        # Process all fields including required defaults
        all_data = {**simple_data, **required_defaults}

        # Track processed fields to avoid duplicates
        processed_fields = set()

        for field_key, value in all_data.items():
            if value is None:
                continue

            # Check if this is an alias
            actual_field_key = field_aliases.get(field_key, field_key)

            # Skip if already processed
            if actual_field_key in processed_fields:
                continue

            # Get field mapping
            field_mapping = field_mappings.get(actual_field_key)
            if not field_mapping:
                # Skip unknown fields with a warning
                if field_key not in [
                    "title",
                    "client_type",
                    "status",
                ]:  # Don't warn for known aliases
                    logger.warning(f"Unknown field '{field_key}' - skipping")
                continue

            processed_fields.add(actual_field_key)
            field_id = field_mapping.get("id")
            field_type = field_mapping.get("type")

            # Prepare field value
            field_value: Any = value

            # Handle choice fields - convert human-readable values to option IDs
            if field_type == "choice" and "options" in field_mapping:
                if isinstance(value, str):
                    # Look up option ID (case-insensitive)
                    options = field_mapping["options"]

                    # Try exact match first
                    option_id = options.get(value.lower())

                    if not option_id:
                        # Try with various formats
                        value_normalized = value.lower().replace(" ", "-")
                        option_id = options.get(value_normalized)

                    if not option_id:
                        # Try removing "listing-" prefix
                        if value_normalized.startswith("listing-"):
                            clean_value = value_normalized[8:]
                            option_id = options.get(clean_value)

                    if not option_id:
                        # Try partial matches for common variations
                        for opt_key, opt_id in options.items():
                            if opt_key.replace("-", " ") == value.lower().replace(
                                "-", " "
                            ):
                                option_id = opt_id
                                break

                    if option_id:
                        field_value = option_id
                    else:
                        # Show valid options without duplicates
                        display_options = []
                        seen_normalized = set()
                        for opt in options.keys():
                            normalized = opt.replace("-", " ").replace("listing ", "")
                            if normalized not in seen_normalized:
                                seen_normalized.add(normalized)
                                # Use the cleanest version
                                if not opt.startswith("listing") and "-" not in opt:
                                    display_options.append(opt)

                        logger.warning(
                            f"Unknown option '{value}' for field '{actual_field_key}'. "
                            f"Valid options: {', '.join(sorted(display_options))}"
                        )
                        continue

            # Add field to array
            # Note: For choice fields with numeric IDs, keep as int; otherwise convert to string
            if field_type == "choice" and isinstance(field_value, int):
                # Keep numeric option IDs as integers
                fields.append({"id": field_id, "value": field_value})
            else:
                # Convert other values to strings
                fields.append({"id": field_id, "value": str(field_value)})

        # Ensure required fields are present
        field_ids_present = {f["id"] for f in fields}
        required_field_keys = [
            "contract_title",
            "contract_client_type",
            "contract_status",
        ]

        for req_key in required_field_keys:
            req_mapping = field_mappings.get(req_key)
            if req_mapping and req_mapping["id"] not in field_ids_present:
                raise ValidationError(
                    f"Required field '{req_key}' is missing or has invalid value"
                )

        return {
            "team_member_id": team_member_id,
            "time_zone_id": 1,  # Default time zone
            "fields": fields,
        }

    def _build_api_format(
        self,
        title: str,
        client_type: Optional[str] = None,
        status: Optional[str] = None,
        purchase_amount: Optional[Union[int, float]] = None,
        team_member_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Build the API format dictionary.

        Args:
            title: Property title (required)
            client_type: Client type ("Buyer", "Seller", "Dual")
            status: Property status
            purchase_amount: Purchase amount
            team_member_id: Team member ID

        Returns:
            API-formatted dictionary
        """
        # Use the new conversion method with a simple dict
        simple_data = {
            "contract_title": title,
            "contract_client_type": client_type or "Buyer",
            "contract_status": status or "Listing- Active",
        }

        if purchase_amount is not None:
            simple_data["purchase_amount"] = purchase_amount

        return self._convert_simple_to_api_format(simple_data, team_member_id)

    def list_properties(
        self, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve a list of properties with validation and error handling.

        Args:
            params: Optional dictionary of query parameters for filtering.
                   Supported parameters may include:
                   - limit: Maximum number of properties to return
                   - offset: Number of properties to skip
                   - status: Filter by property status (e.g., 'active', 'closed')
                   - search: Search term for filtering properties

        Returns:
            A list of dictionaries, where each dictionary represents a property

        Raises:
            ValidationError: If parameters are invalid
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            # Get all properties
            properties = client.properties.list_properties()

            # Get properties with custom parameters
            properties = client.properties.list_properties(params={"limit": 50, "status": "active"})
            ```
        """
        try:
            validated_params = self._validate_list_params(params)

            logger.info("Listing properties", extra={"params": validated_params})
            response = self.get("/properties", params=validated_params)
            result = self._process_list_response(response, "/properties")

            logger.info(f"Successfully retrieved {len(result)} properties")
            return result

        except Exception as e:
            logger.error(
                f"Failed to list properties: {str(e)}", extra={"params": params}
            )
            raise

    def create_property(
        self,
        property_data: Union[str, Dict[str, Any]],
        team_member_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Create a new property with simple or advanced options.

        This method supports multiple input formats for ease of use:

        **SIMPLE USAGE:**

        1. Just a title (string):
            ```python
            property = client.properties.create_property("Beautiful Family Home")
            ```

        2. Simple dictionary with human-readable fields:
            ```python
            property = client.properties.create_property({
                "title": "Beautiful Family Home",           # Required
                "client_type": "Buyer",                     # "Buyer", "Seller", or "Dual" (defaults to "Buyer")
                "status": "Active",                         # "Active", "Pre-MLS", "Under Contract", etc. (defaults to "Active")
                "purchase_amount": 450000,                  # Optional dollar amount
                "address": "123 Main St",                   # Optional
                "city": "Anytown",                          # Optional
                "state": "CA",                              # Optional
                "zip_code": "12345"                         # Optional
            })
            ```

        **ADVANCED USAGE:**

        3. Full API format (for advanced users):
            ```python
            property = client.properties.create_property({
                "team_member_id": 26392,
                "time_zone_id": 1,
                "fields": [
                    {"id": 926565, "key": "contract_title", "value": "Custom Property"},
                    {"id": 926553, "key": "contract_client_type", "value": 797212},
                    {"id": 926552, "key": "contract_status", "value": 797206}
                ]
            })
            ```

        **Available Options:**

        Client Types: "Buyer", "Seller", "Dual"

        Status Options: "Pre-MLS", "Active", "Under Contract", "Withdrawn",
                       "Contract", "Closed", "Terminated"

        Args:
            property_data: Property information as string (title only) or dictionary
            team_member_id: Optional team member ID (auto-detected if not provided)

        Returns:
            A dictionary representing the newly created property with at least:
            - id: Property ID
            - created: Creation timestamp

        Raises:
            ValidationError: If property data is invalid or missing required fields
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Examples:
            ```python
            # Simple string title
            property1 = client.properties.create_property("My New Property")

            # Dictionary with common fields
            property2 = client.properties.create_property({
                "title": "Luxury Estate",
                "client_type": "Buyer",
                "status": "Active",
                "purchase_amount": 650000
            })

            # With address details
            property3 = client.properties.create_property({
                "title": "Downtown Condo",
                "client_type": "Seller",
                "status": "Pre-MLS",
                "address": "456 Oak Ave",
                "city": "Downtown",
                "state": "NY",
                "purchase_amount": 425000
            })
            ```
        """
        try:
            # Convert input to API format
            api_data = self._prepare_property_data(property_data, team_member_id)

            # Validate the prepared data
            self._validate_property_data(api_data, "create")

            title = self._extract_title_from_data(property_data)
            logger.info(
                "Creating new property",
                extra={"title": title},
            )

            # Properties POST endpoint requires trailing slash (per successful tests)
            response = self.post("/properties/", json_data=api_data)
            result = self._process_response_data(response, "/properties/")

            property_id = result.get("id")
            logger.info(f"Successfully created property with ID: {property_id}")
            return result

        except Exception as e:
            logger.error(
                f"Failed to create property: {str(e)}",
                extra={
                    "input_type": type(property_data).__name__,
                    "property_data_keys": (
                        list(property_data.keys())
                        if isinstance(property_data, dict)
                        else "string_input"
                    ),
                },
            )
            raise

    def retrieve_property(self, property_id: int) -> Dict[str, Any]:
        """Retrieve a specific property by its ID with validation.

        Args:
            property_id: The ID of the property to retrieve (must be a positive integer)

        Returns:
            A dictionary representing the property

        Raises:
            ValidationError: If property_id is invalid
            NotFoundError: If the property is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            property = client.properties.retrieve_property(123)
            print(f"Property address: {property.get('property_address', 'N/A')}")
            ```
        """
        try:
            validated_id = self._validate_resource_id(property_id, "property")

            logger.info(f"Retrieving property with ID: {validated_id}")
            response = self.get(f"/properties/{validated_id}")
            result = self._process_response_data(
                response, f"/properties/{validated_id}"
            )

            logger.info(f"Successfully retrieved property: {validated_id}")
            return result

        except Exception as e:
            logger.error(f"Failed to retrieve property {property_id}: {str(e)}")
            raise

    def update_property(
        self, property_id: int, property_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update an existing property with validation.

        Args:
            property_id: The ID of the property to update (must be a positive integer)
            property_data: A dictionary containing the fields to update.
                          Fields can include any valid property fields like:
                          - contract_title, property_address, property_city, status, etc.

        Returns:
            A dictionary representing the updated property

        Raises:
            ValidationError: If property_id or property_data is invalid
            NotFoundError: If the property is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            updated_property = client.properties.update_property(123, {
                "status": "sold",
                "sale_price": 350000,
                "closing_date": "2024-01-15"
            })
            ```
        """
        try:
            validated_id = self._validate_resource_id(property_id, "property")
            self._validate_property_data(property_data, "update")

            logger.info(
                f"Updating property with ID: {validated_id}",
                extra={"update_fields": list(property_data.keys())},
            )
            response = self.put(f"/properties/{validated_id}", json_data=property_data)
            result = self._process_response_data(
                response, f"/properties/{validated_id}"
            )

            logger.info(f"Successfully updated property: {validated_id}")
            return result

        except Exception as e:
            logger.error(
                f"Failed to update property {property_id}: {str(e)}",
                extra={
                    "property_data_keys": (
                        list(property_data.keys())
                        if isinstance(property_data, dict)
                        else "invalid"
                    )
                },
            )
            raise

    def delete_property(self, property_id: int) -> Dict[str, Any]:
        """Delete a property by its ID with validation.

        Args:
            property_id: The ID of the property to delete (must be a positive integer)

        Returns:
            A dictionary containing the API response (typically empty for successful deletions)

        Raises:
            ValidationError: If property_id is invalid
            NotFoundError: If the property is not found
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            ServerError: If server error occurs
            NetworkError: If network error occurs
            OpenToCloseAPIError: For other API errors

        Example:
            ```python
            result = client.properties.delete_property(123)
            print("Property deleted successfully")
            ```
        """
        try:
            validated_id = self._validate_resource_id(property_id, "property")

            logger.info(f"Deleting property with ID: {validated_id}")
            result = self.delete(f"/properties/{validated_id}")

            logger.info(f"Successfully deleted property: {validated_id}")
            return result

        except Exception as e:
            logger.error(f"Failed to delete property {property_id}: {str(e)}")
            raise

    def get_property_fields(self) -> List[Dict[str, Any]]:
        """Retrieve property field definitions from the API.

        This method fetches the complete list of available property fields
        with their definitions, types, and structure from the Open To Close API.
        This is useful for understanding what fields are available when creating
        or updating properties.

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
            # Get all property field definitions
            fields = client.properties.get_property_fields()

            # Print field groups and sections
            for group in fields:
                if 'group' in group:
                    print(f"Group: {group['group']['title']}")
                    for section in group['group']['sections']:
                        if 'section' in section:
                            print(f"  Section: {section['section']['title']}")
                            for field in section['section'].get('fields', []):
                                print(f"    Field: {field['title']} ({field['type']})")
            ```
        """
        try:
            logger.info("Retrieving property field definitions")
            response = self.get("/propertyFields")
            result = self._process_list_response(response, "/propertyFields")

            logger.info(
                f"Successfully retrieved property field definitions with {len(result)} field groups"
            )
            return result

        except Exception as e:
            logger.error(f"Failed to retrieve property fields: {str(e)}")
            raise
