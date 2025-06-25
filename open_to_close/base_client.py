"""Base client for Open To Close API."""

import logging
import os
import time
from typing import Any, Dict, List, Optional, Union

import requests
from dotenv import load_dotenv
from requests.exceptions import ConnectionError, HTTPError, RequestException, Timeout

from .exceptions import (
    AuthenticationError,
    ConfigurationError,
    DataFormatError,
    NetworkError,
    NotFoundError,
    OpenToCloseAPIError,
    RateLimitError,
    ServerError,
    TimeoutError,
    ValidationError,
)

load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Constants
DEFAULT_BASE_URL = "https://api.opentoclose.com/v1"
NON_V1_BASE_URL = "https://api.opentoclose.com"
DEFAULT_TIMEOUT = 30.0
MAX_RETRIES = 3
RETRY_BACKOFF_FACTOR = 2.0


class BaseClient:
    """Base client with common functionality and enhanced error handling."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = MAX_RETRIES,
        retry_backoff_factor: float = RETRY_BACKOFF_FACTOR,
    ) -> None:
        """Initialize the base client.

        Args:
            api_key: API key for authentication
            base_url: Base URL for the API
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
            retry_backoff_factor: Backoff factor for retries

        Raises:
            AuthenticationError: If API key is missing or invalid format
            ConfigurationError: If configuration parameters are invalid
        """
        self._validate_and_set_api_key(api_key)
        self._validate_and_set_configuration(
            base_url, timeout, max_retries, retry_backoff_factor
        )
        self._setup_session()

        # Initialize field mappings cache
        self._field_mappings_cache: Optional[Dict[str, Dict[str, Any]]] = None
        self._field_mappings_raw: Optional[List[Dict[str, Any]]] = None

        logger.info(
            "Initialized Open To Close API client",
            extra={
                "base_url": self.base_url,
                "timeout": self.timeout,
                "max_retries": self.max_retries,
            },
        )

    def _validate_and_set_api_key(self, api_key: Optional[str]) -> None:
        """Validate and set API key.

        Args:
            api_key: API key to validate

        Raises:
            AuthenticationError: If API key is missing or invalid format
        """
        self.api_key = api_key or os.getenv("OPEN_TO_CLOSE_API_KEY")

        if not self.api_key:
            raise AuthenticationError(
                "API key is required. Set OPEN_TO_CLOSE_API_KEY environment variable "
                "or pass api_key parameter."
            )

        # Basic API key format validation
        if not isinstance(self.api_key, str) or len(self.api_key.strip()) == 0:
            raise AuthenticationError("API key must be a non-empty string.")

        # Log API key validation (without exposing the key)
        logger.debug("API key validated successfully")

    def _validate_and_set_configuration(
        self,
        base_url: Optional[str],
        timeout: float,
        max_retries: int,
        retry_backoff_factor: float,
    ) -> None:
        """Validate and set configuration parameters.

        Args:
            base_url: Base URL for API
            timeout: Request timeout
            max_retries: Maximum retry attempts
            retry_backoff_factor: Backoff factor for retries

        Raises:
            ConfigurationError: If any configuration parameter is invalid
        """
        # Validate base URL
        self.base_url = base_url or DEFAULT_BASE_URL
        if not isinstance(self.base_url, str) or not self.base_url.startswith(
            ("http://", "https://")
        ):
            raise ConfigurationError(
                f"Invalid base_url: {self.base_url}. Must be a valid HTTP/HTTPS URL."
            )

        # Validate timeout
        if not isinstance(timeout, (int, float)) or timeout <= 0:
            raise ConfigurationError(
                f"Invalid timeout: {timeout}. Must be a positive number."
            )
        self.timeout = float(timeout)

        # Validate max_retries
        if not isinstance(max_retries, int) or max_retries < 0:
            raise ConfigurationError(
                f"Invalid max_retries: {max_retries}. Must be a non-negative integer."
            )
        self.max_retries = max_retries

        # Validate retry backoff factor
        if (
            not isinstance(retry_backoff_factor, (int, float))
            or retry_backoff_factor < 1
        ):
            raise ConfigurationError(
                f"Invalid retry_backoff_factor: {retry_backoff_factor}. Must be >= 1."
            )
        self.retry_backoff_factor = float(retry_backoff_factor)

    def _setup_session(self) -> None:
        """Set up the requests session with proper configuration."""
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": "open-to-close-python-client/1.0.0",
            }
        )

        # Session timeout is configured per request in the _request method

    def _get_base_url_for_operation(self, method: str, endpoint: str) -> str:
        """Get the appropriate base URL based on operation type and endpoint.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, PATCH)
            endpoint: API endpoint

        Returns:
            Appropriate base URL for the operation
        """
        if self.base_url != DEFAULT_BASE_URL:
            # If user provided custom base URL, use it as-is
            return self.base_url

        # Use consistent v1 URLs for all operations to maintain compatibility
        return DEFAULT_BASE_URL

    def _validate_endpoint(self, endpoint: str) -> str:
        """Validate and normalize API endpoint.

        Args:
            endpoint: API endpoint to validate

        Returns:
            Normalized endpoint

        Raises:
            ValidationError: If endpoint is invalid
        """
        if not isinstance(endpoint, str):
            raise ValidationError(
                f"Endpoint must be a string, got {type(endpoint).__name__}"
            )

        if not endpoint:
            raise ValidationError("Endpoint cannot be empty")

        # Normalize endpoint (ensure leading slash)
        normalized_endpoint = endpoint if endpoint.startswith("/") else f"/{endpoint}"

        logger.debug(f"Validated endpoint: {normalized_endpoint}")
        return normalized_endpoint

    def _validate_resource_id(
        self, resource_id: Any, resource_type: str = "resource"
    ) -> int:
        """Validate resource ID parameter.

        Args:
            resource_id: Resource ID to validate
            resource_type: Type of resource for error messages

        Returns:
            Validated resource ID as integer

        Raises:
            ValidationError: If resource ID is invalid
        """
        if resource_id is None:
            raise ValidationError(f"{resource_type} ID cannot be None")

        try:
            id_int = int(resource_id)
            if id_int <= 0:
                raise ValidationError(
                    f"{resource_type} ID must be a positive integer, got {id_int}"
                )
            return id_int
        except (ValueError, TypeError):
            raise ValidationError(
                f"{resource_type} ID must be a valid integer, got {type(resource_id).__name__}: {resource_id}"
            )

    def _validate_request_data(self, data: Any, endpoint: str) -> None:
        """Validate request data before sending.

        Args:
            data: Data to validate
            endpoint: Endpoint for context

        Raises:
            ValidationError: If data is invalid
        """
        if data is None:
            return

        if not isinstance(data, (dict, list)):
            raise ValidationError(
                f"Request data must be a dictionary or list, got {type(data).__name__}"
            )

        # Log data validation (without sensitive data)
        try:
            data_size = len(data) if hasattr(data, "__len__") else 0
        except (TypeError, AttributeError):
            data_size = 0

        logger.debug(
            f"Request data validated for endpoint: {endpoint}",
            extra={"data_type": type(data).__name__, "data_size": data_size},
        )

    def _should_retry(self, exception: Exception, attempt: int) -> bool:
        """Determine if request should be retried.

        Args:
            exception: Exception that occurred
            attempt: Current attempt number (1-based)

        Returns:
            True if should retry, False otherwise
        """
        if attempt >= self.max_retries:
            return False

        # Retry on network errors
        if isinstance(exception, (ConnectionError, Timeout)):
            return True

        # Retry on rate limit errors
        if isinstance(exception, RateLimitError):
            return True

        # Retry on server errors (5xx)
        if isinstance(exception, ServerError):
            return True

        return False

    def _calculate_retry_delay(
        self, attempt: int, retry_after: Optional[int] = None
    ) -> float:
        """Calculate delay before retry.

        Args:
            attempt: Current attempt number (1-based)
            retry_after: Specific retry-after value from server

        Returns:
            Delay in seconds
        """
        if retry_after:
            return float(retry_after)

        # Exponential backoff
        return self.retry_backoff_factor ** (attempt - 1)

    def _handle_response(
        self, response: requests.Response, endpoint: str, method: str
    ) -> Dict[str, Any]:
        """Handle HTTP response and raise appropriate exceptions with enhanced context.

        Args:
            response: HTTP response object
            endpoint: API endpoint that was called
            method: HTTP method used

        Returns:
            Response data as dictionary

        Raises:
            Various OpenToCloseAPIError subclasses based on response
        """
        # Parse response data safely
        try:
            response_data = response.json() if response.content else {}
        except ValueError as e:
            logger.warning(f"Failed to parse JSON response: {e}")
            response_data = {"message": response.text, "raw_content": response.text}

        # Log response for debugging
        try:
            response_size = (
                len(response.content)
                if hasattr(response, "content") and response.content
                else 0
            )
        except (TypeError, AttributeError):
            response_size = 0

        logger.debug(
            f"Received response from {method} {endpoint}",
            extra={
                "status_code": getattr(response, "status_code", 0),
                "response_size": response_size,
            },
        )

        # Handle successful responses
        if response.status_code in (200, 201):
            # Check if we got HTML instead of JSON (indicates auth redirect or server error)
            content_type = response.headers.get("content-type", "").lower()
            if "text/html" in content_type:
                # Check if it's an error page
                if (
                    "error occurred" in response.text.lower()
                    or "internal server error" in response.text.lower()
                ):
                    raise ServerError(
                        f"Server returned HTML error page for {method} {endpoint}. The endpoint may not be available or implemented.",
                        status_code=response.status_code,
                        response_data={
                            "message": "Server error returned as HTML",
                            "content_type": content_type,
                        },
                        endpoint=endpoint,
                        method=method,
                    )
                else:
                    raise AuthenticationError(
                        f"Received HTML login page instead of JSON for {method} {endpoint}. Check authentication or endpoint availability.",
                        status_code=response.status_code,
                        response_data={
                            "message": "Authentication required",
                            "content_type": content_type,
                        },
                        endpoint=endpoint,
                        method=method,
                    )
            return response_data
        if response.status_code == 204:
            return {}

        # Enhanced error handling with context
        error_kwargs = {
            "status_code": response.status_code,
            "response_data": response_data,
            "endpoint": endpoint,
            "method": method,
        }

        if response.status_code == 400:
            # Extract field-specific errors if available
            field_errors = None
            if isinstance(response_data, dict):
                field_errors = response_data.get("errors") or response_data.get(
                    "field_errors"
                )

            raise ValidationError(
                f"Bad request to {method} {endpoint}: {response_data.get('message', 'Invalid request')}",
                field_errors=field_errors,
                **error_kwargs,
            )

        elif response.status_code == 401:
            message = response_data.get("message", "Invalid credentials")
            raise AuthenticationError(
                f"Authentication failed for {method} {endpoint}: {message}",
                **error_kwargs,
            )

        elif response.status_code == 404:
            raise NotFoundError(
                f"Resource not found for {method} {endpoint}: {response_data.get('message', 'Not found')}",
                status_code=response.status_code,
                response_data=response_data,
                endpoint=endpoint,
                method=method,
            )

        elif response.status_code == 429:
            message = response_data.get("message", "Too many requests")
            retry_after = None
            if "retry-after" in response.headers:
                try:
                    retry_after = int(response.headers["retry-after"])
                except ValueError:
                    pass

            raise RateLimitError(
                f"Rate limit exceeded for {method} {endpoint}: {message}",
                retry_after=retry_after,
                **error_kwargs,
            )

        elif 500 <= response.status_code < 600:
            message = response_data.get("message", "Internal server error")
            raise ServerError(
                f"Server error for {method} {endpoint}: {message}",
                **error_kwargs,
            )

        # Generic error for other status codes
        raise OpenToCloseAPIError(
            f"Unexpected error for {method} {endpoint}: {response_data.get('message', 'Unknown error')}",
            status_code=response.status_code,
            response_data=response_data,
            endpoint=endpoint,
            method=method,
        )

    def _process_response_data(
        self, response: Dict[str, Any], endpoint: str
    ) -> Dict[str, Any]:
        """Process API response data with consistent format handling and validation.

        Args:
            response: Raw response from API
            endpoint: Endpoint for error context

        Returns:
            Processed response data

        Raises:
            DataFormatError: If response format is unexpected
        """
        if not isinstance(response, dict):
            raise DataFormatError(
                f"Expected dictionary response from {endpoint}",
                expected_format="dict",
                actual_format=type(response).__name__,
                endpoint=endpoint,
            )

        # Handle direct object responses (with ID field)
        if response.get("id"):
            return response

        # Handle wrapped responses
        if "data" in response:
            data = response["data"]
            if isinstance(data, dict):
                return data
            else:
                logger.warning(f"Unexpected data format in response from {endpoint}")
                return {}

        # Return response as-is if it's a valid dict
        return response

    def _process_list_response(
        self, response: Dict[str, Any], endpoint: str
    ) -> List[Dict[str, Any]]:
        """Process API response for list endpoints with consistent format handling and validation.

        Args:
            response: Raw response from API
            endpoint: Endpoint for error context

        Returns:
            List of processed response data

        Raises:
            DataFormatError: If response format is unexpected
        """
        # Handle direct list responses
        if isinstance(response, list):
            return response

        if isinstance(response, dict):
            # Handle wrapped list responses
            if "data" in response:
                data = response["data"]
                if isinstance(data, list):
                    return data
                else:
                    logger.warning(
                        f"Expected list in data field from {endpoint}, got {type(data).__name__}"
                    )
                    return []

            # Handle empty responses
            if not response:
                return []

            # Single object response - wrap in list
            if response.get("id"):
                return [response]

        # Invalid response format
        raise DataFormatError(
            f"Expected list or dict with list data from {endpoint}",
            expected_format="list or dict",
            actual_format=type(response).__name__,
            endpoint=endpoint,
        )

    def _request(
        self,
        method: str,
        endpoint: str,
        *,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        files: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make HTTP request to API with comprehensive error handling and retry logic.

        Args:
            method: HTTP method
            endpoint: API endpoint
            data: Form data
            json_data: JSON data
            files: File uploads
            params: Query parameters

        Returns:
            Response data

        Raises:
            Various OpenToCloseAPIError subclasses
        """
        # Validate inputs
        endpoint = self._validate_endpoint(endpoint)
        self._validate_request_data(json_data or data, endpoint)

        # Get the appropriate base URL for this operation
        base_url = self._get_base_url_for_operation(method, endpoint)
        url = f"{base_url}/{endpoint.lstrip('/')}"

        # Add api_token to params for all requests
        if params is None:
            params = {}
        params["api_token"] = self.api_key

        # Log request details
        try:
            params_count = len(params) if params and hasattr(params, "__len__") else 0
        except (TypeError, AttributeError):
            params_count = 0

        logger.info(
            f"Making {method} request to {endpoint}",
            extra={
                "url": url,
                "has_json_data": json_data is not None,
                "has_form_data": data is not None,
                "has_files": files is not None,
                "params_count": params_count,
            },
        )

        # Retry logic
        last_exception: Optional[Exception] = None
        for attempt in range(1, self.max_retries + 1):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    json=json_data,
                    data=data,
                    files=files,
                    params=params,
                    timeout=self.timeout,
                )

                return self._handle_response(response, endpoint, method)

            except (ConnectionError, Timeout) as e:
                last_exception = NetworkError(
                    f"Network error for {method} {endpoint}: {str(e)}",
                    original_error=e,
                    endpoint=endpoint,
                    method=method,
                )

            except RequestException as e:
                last_exception = NetworkError(
                    f"Request error for {method} {endpoint}: {str(e)}",
                    original_error=e,
                    endpoint=endpoint,
                    method=method,
                )

            except (RateLimitError, ServerError) as e:
                last_exception = e

            except Exception as e:
                # Convert unexpected exceptions to our exception types
                last_exception = OpenToCloseAPIError(
                    f"Unexpected error for {method} {endpoint}: {str(e)}",
                    endpoint=endpoint,
                    method=method,
                )

            # Check if we should retry
            if not self._should_retry(last_exception, attempt):
                break

            # Calculate delay and wait
            if attempt < self.max_retries:
                retry_after = getattr(last_exception, "retry_after", None)
                delay = self._calculate_retry_delay(attempt, retry_after)

                logger.warning(
                    f"Request failed, retrying in {delay:.1f}s (attempt {attempt}/{self.max_retries})",
                    extra={
                        "endpoint": endpoint,
                        "method": method,
                        "attempt": attempt,
                        "delay": delay,
                        "error": str(last_exception),
                    },
                )

                time.sleep(delay)

        # All retries exhausted, raise the last exception
        if last_exception:
            raise last_exception

        # Should never reach here, but just in case
        raise OpenToCloseAPIError(f"Request failed for {method} {endpoint}")

    def get(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make GET request with validation.

        Args:
            endpoint: API endpoint
            params: Query parameters

        Returns:
            Response data
        """
        return self._request("GET", endpoint, params=params)

    def post(
        self,
        endpoint: str,
        json_data: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make POST request with validation.

        Args:
            endpoint: API endpoint
            json_data: JSON data to send
            data: Form data to send
            files: Files to upload

        Returns:
            Response data
        """
        return self._request(
            "POST", endpoint, json_data=json_data, data=data, files=files
        )

    def put(
        self,
        endpoint: str,
        json_data: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make PUT request with validation.

        Args:
            endpoint: API endpoint
            json_data: JSON data to send
            data: Form data to send
            files: Files to upload

        Returns:
            Response data
        """
        return self._request(
            "PUT", endpoint, json_data=json_data, data=data, files=files
        )

    def delete(self, endpoint: str) -> Dict[str, Any]:
        """Make DELETE request with validation.

        Args:
            endpoint: API endpoint

        Returns:
            Response data
        """
        return self._request("DELETE", endpoint)

    def patch(
        self,
        endpoint: str,
        json_data: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make PATCH request with validation.

        Args:
            endpoint: API endpoint
            json_data: JSON data to send
            data: Form data to send
            files: Files to upload

        Returns:
            Response data
        """
        return self._request(
            "PATCH", endpoint, json_data=json_data, data=data, files=files
        )

    def get_field_mappings(
        self, force_refresh: bool = False
    ) -> Dict[str, Dict[str, Any]]:
        """Fetch and cache field ID mappings from the API.

        This method retrieves property field definitions from the API and creates
        a mapping dictionary for easy field name to ID lookups.

        Args:
            force_refresh: Force refresh of cached mappings

        Returns:
            Dictionary mapping field names to their metadata including:
            - id: Field ID
            - type: Field type (text, choice, date, etc.)
            - options: For choice fields, maps option names to IDs

        Raises:
            AuthenticationError: If authentication fails
            ServerError: If server error occurs
            NetworkError: If network error occurs
        """
        if self._field_mappings_cache is not None and not force_refresh:
            return self._field_mappings_cache

        logger.info("Fetching field mappings from API")

        try:
            # Get raw field data
            response = self.get("/propertyFields")
            self._field_mappings_raw = self._process_list_response(
                response, "/propertyFields"
            )

            # Build field mappings
            field_mappings = {}

            for group in self._field_mappings_raw:
                if "group" not in group:
                    continue

                for section in group["group"].get("sections", []):
                    if "section" not in section:
                        continue

                    for field in section["section"].get("fields", []):
                        field_key = field.get("key", "")
                        if not field_key:
                            continue

                        # Build field mapping entry
                        mapping = {
                            "id": field.get("id"),
                            "type": field.get("type"),
                            "title": field.get("title"),
                            "key": field_key,
                        }

                        # For choice fields, map option names to IDs
                        if field.get("type") == "choice" and "options" in field:
                            mapping["options"] = {}
                            for option in field.get("options", []):
                                option_title = option.get("title", "").lower()
                                # Handle various formats
                                mapping["options"][option_title] = option.get("id")
                                # Also map with hyphens instead of spaces
                                mapping["options"][option_title.replace(" ", "-")] = (
                                    option.get("id")
                                )
                                # Remove "listing-" prefix variations
                                if option_title.startswith("listing-"):
                                    clean_title = option_title[8:]  # Remove "listing-"
                                    mapping["options"][clean_title] = option.get("id")

                        field_mappings[field_key] = mapping

            self._field_mappings_cache = field_mappings
            logger.info(f"Successfully cached {len(field_mappings)} field mappings")

            return field_mappings

        except Exception as e:
            logger.error(f"Failed to fetch field mappings: {str(e)}")
            raise

    def refresh_field_mappings(self) -> Dict[str, Dict[str, Any]]:
        """Force refresh of field mappings cache.

        Returns:
            Updated field mappings dictionary
        """
        return self.get_field_mappings(force_refresh=True)

    def get_raw_field_definitions(self) -> Optional[List[Dict[str, Any]]]:
        """Get the raw field definitions as returned by the API.

        Returns:
            List of field groups with their sections and fields, or None if not cached
        """
        if self._field_mappings_raw is None:
            # Fetch mappings if not cached
            self.get_field_mappings()
        return self._field_mappings_raw
