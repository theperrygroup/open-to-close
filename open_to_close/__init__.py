"""Open To Close API Python Client."""

# Import service clients
from .agents import AgentsAPI
from .client import OpenToCloseAPI
from .contacts import ContactsAPI
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
from .properties import PropertiesAPI
from .property_contacts import PropertyContactsAPI
from .property_documents import PropertyDocumentsAPI
from .property_emails import PropertyEmailsAPI
from .property_notes import PropertyNotesAPI
from .property_tasks import PropertyTasksAPI
from .tags import TagsAPI
from .teams import TeamsAPI
from .users import UsersAPI

__version__ = "2.5.0"
__all__ = [
    "OpenToCloseAPI",
    # Service Clients
    "AgentsAPI",
    "ContactsAPI",
    "PropertiesAPI",
    "PropertyContactsAPI",
    "PropertyDocumentsAPI",
    "PropertyEmailsAPI",
    "PropertyNotesAPI",
    "PropertyTasksAPI",
    "TagsAPI",
    "TeamsAPI",
    "UsersAPI",
    # Exceptions
    "OpenToCloseAPIError",
    "AuthenticationError",
    "ValidationError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
    "NetworkError",
    "TimeoutError",
    "ConfigurationError",
    "DataFormatError",
]
