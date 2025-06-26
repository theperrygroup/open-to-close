# Open To Close API Python Client

[![PyPI version](https://img.shields.io/pypi/v/open-to-close?color=blue&label=version)](https://pypi.org/project/open-to-close/)
[![Python versions](https://img.shields.io/pypi/pyversions/open-to-close)](https://pypi.org/project/open-to-close/)
[![License](https://img.shields.io/github/license/theperrygroup/open-to-close)](https://github.com/theperrygroup/open-to-close/blob/main/LICENSE)
[![Build Status](https://img.shields.io/github/actions/workflow/status/theperrygroup/open-to-close/ci.yml?branch=main)](https://github.com/theperrygroup/open-to-close/actions)
[![Documentation](https://img.shields.io/badge/docs-mkdocs-blue)](https://theperrygroup.github.io/open-to-close/)
[![Coverage](https://img.shields.io/codecov/c/github/theperrygroup/open-to-close)](https://codecov.io/gh/theperrygroup/open-to-close)

A modern, type-safe Python wrapper for the Open To Close API. Manage properties, agents, contacts, and more with a clean, intuitive interface designed for real estate professionals and developers.

**🎉 Latest Update**: All API endpoint issues have been fully resolved! The wrapper now features 100% working CRUD operations across all endpoints with production-ready reliability.

**🚀 v2.5.0 NEW**: **Dynamic Field Mapping** - Revolutionary simplified property creation with automatic field ID translation and human-readable field names!

## ✨ Features

- **🏠 Complete Property Management** - Full CRUD operations for properties, listings, and transactions
- **👥 Contact & Team Management** - Manage agents, contacts, teams, and user relationships  
- **📄 Document Tracking** - Handle property documents, emails, notes, and tasks
- **🔒 Type Safety** - Full type hints and IDE support for better development experience
- **🛡️ Robust Error Handling** - Comprehensive exception handling with detailed error messages
- **⚡ Production Ready** - Built-in rate limiting, retry logic, and authentication management
- **🧪 Well Tested** - Comprehensive test suite with 100% coverage
- **📚 Excellent Documentation** - Complete guides, examples, and API reference
- **✅ Endpoint Reliability** - All 6 core API endpoints tested and verified working (100% success rate)
- **🔧 Smart URL Routing** - Automatic handling of different URL patterns for optimal API compatibility
- **🎯 Simplified Property Creation** - Create properties with just a title or simple dictionary format
- **🆕 Dynamic Field Mapping** - Automatic field ID translation with human-readable names (v2.5.0)
- **🔍 Field Discovery** - List and validate available fields before API calls (v2.5.0)
- **🎛️ Smart Defaults** - Automatic team member detection and sensible field defaults (v2.5.0)

## 🚀 Quick Start

### Installation

```bash
pip install open-to-close
```

### Authentication

Set your API key as an environment variable:

```bash
export OPEN_TO_CLOSE_API_KEY="your_api_key_here"
```

### Basic Usage

```python
from open_to_close import OpenToCloseAPI

# Initialize the client
client = OpenToCloseAPI()

# Create a new property (simplified format) 🆕
property_data = client.properties.create_property({
    "title": "Beautiful Family Home",
    "client_type": "Buyer", 
    "status": "Active",
    "purchase_amount": 450000
})

# Or even simpler - just pass a title!
simple_property = client.properties.create_property("Downtown Condo")

# Get all properties
properties = client.properties.list_properties()

# Add a note to the property
note = client.property_notes.create_property_note(
    property_data["id"],
    {"content": "Initial property intake completed"}
)

print(f"Created property {property_data['id']} with note {note['id']}")
```

## 🎯 Simplified Property Creation

Creating properties is now incredibly easy! Choose from multiple input formats:

```python
# 1. Simple title only (uses smart defaults)
property1 = client.properties.create_property("Beautiful Family Home")

# 2. Dictionary with common fields
property2 = client.properties.create_property({
    "title": "Luxury Estate with Pool",
    "client_type": "Buyer",      # "Buyer", "Seller", or "Dual" 
    "status": "Active",          # "Active", "Pre-MLS", "Under Contract", etc.
    "purchase_amount": 650000
})

# 3. Seller property
property3 = client.properties.create_property({
    "title": "Downtown Condo for Sale",
    "client_type": "Seller",
    "status": "Pre-MLS",
    "purchase_amount": 425000
})
```

**What happens automatically:**
- 🔍 **Auto-detects team member ID** from your teams
- 🎯 **Smart defaults**: Client type = "Buyer", Status = "Active"  
- 🛡️ **Input validation** with clear error messages
- 🔄 **Format conversion** to complex API structure behind the scenes
- ⚡ **Legacy support** - advanced format still works for power users

👉 **See [Property Creation Guide](docs/property-creation-guide.md) for complete examples and options**

## 🔍 Field Discovery & Validation (v2.5.0)

Discover available fields and validate data before making API calls:

```python
# List all available property fields with metadata
fields = client.list_available_fields()
print(f"Found {len(fields)} available fields")

# Show field details
for field in fields[:5]:
    required = "✅ Required" if field['required'] else "⭕ Optional"
    print(f"{field['key']}: {field['title']} ({field['type']}) - {required}")

# Validate property data before creation
property_data = {
    "title": "Beautiful Home",
    "client_type": "Buyer",
    "status": "Active"
}

is_valid, errors = client.validate_property_data(property_data)
if is_valid:
    property = client.properties.create_property(property_data)
    print(f"✅ Created property {property['id']}")
else:
    print(f"❌ Validation errors: {errors}")
```

**Field Discovery Features:**
- 🔍 **Dynamic Field Lookup** - Fetch current field definitions from API
- 🏷️ **Field Metadata** - Get field types, requirements, and available options
- ✅ **Pre-Validation** - Validate data before API calls to prevent errors
- 🔄 **Auto-Refresh** - Field mappings update automatically when API changes

## 🏠 Complete Transaction Workflow

Create complete real estate transactions with properties and associated contacts:

```python
from open_to_close import OpenToCloseAPI

client = OpenToCloseAPI()

# Step 1: Create property (transaction)
property_result = client.properties.create_property({
    "title": "123 Main Street Sale Transaction",
    "client_type": "Buyer",
    "status": "Active",
    "purchase_amount": 450000
})

# Step 2: Create contacts with correct field format
contacts = [
    {
        "first_name": "John",
        "last_name": "Smith", 
        "email": "john.smith@email.com",
        "phone": "+1-555-0101"
    },
    {
        "first_name": "Sarah",
        "last_name": "Johnson",
        "email": "sarah.johnson@email.com", 
        "phone": "+1-555-0102"
    }
]

# Create all contacts
created_contacts = []
for contact_data in contacts:
    contact = client.contacts.create_contact(contact_data)
    created_contacts.append(contact)

# Step 3: Link contacts to property
for contact in created_contacts:
    association = client.property_contacts.create_property_contact(
        property_id=property_result['id'],
        contact_data={"contact_id": contact['id']}
    )
    print(f"Linked contact {contact['first_name']} {contact['last_name']}")
```

!!! warning "Important Contact Field Requirements"
    🚨 **Critical**: The `name` field is **NOT supported** by the Open To Close API. You must use `first_name` and `last_name` fields separately, or the API will return "Bad request" errors.

👉 **See [Property-Contact Workflow Guide](docs/guides/property-contact-workflow.md) for the complete tested workflow**

## 🛡️ Reliability & Testing

This API wrapper has undergone comprehensive testing and debugging to ensure production reliability:

- **✅ All 6 Core Endpoints Verified** - Properties, Contacts, Agents, Teams, Users, and Tags
- **✅ 100% CRUD Success Rate** - Create, Read, Update, Delete operations all working
- **✅ URL Pattern Resolution** - Smart routing handles API's different URL patterns automatically
- **✅ Production Testing** - Extensively tested with real API calls and edge cases

For detailed information about the testing and debugging process, see:
- [`ENDPOINT_ISSUES_RESOLVED.md`](ENDPOINT_ISSUES_RESOLVED.md) - Complete resolution summary
- [`tests/INVESTIGATION_TESTS_README.md`](tests/INVESTIGATION_TESTS_README.md) - Investigation test documentation

## 📋 Core Resources

| Resource | Description | Example Usage |
|----------|-------------|---------------|
| **Properties** | Manage real estate listings and transactions | `client.properties.list_properties()` |
| **Agents** | Handle agent profiles and assignments | `client.agents.list_agents()` |
| **Contacts** | Customer and lead management | `client.contacts.create_contact(data)` |
| **Teams** | Team organization and structure | `client.teams.list_teams()` |
| **Users** | User account management | `client.users.retrieve_user(123)` |
| **Tags** | Classification and labeling | `client.tags.list_tags()` |

## 🏗️ Property Sub-Resources

Extend property functionality with related data:

| Sub-Resource | Description | Example Usage |
|-------------|-------------|---------------|
| **Documents** | File attachments per property | `client.property_documents.list_property_documents(prop_id)` |
| **Emails** | Communication tracking | `client.property_emails.create_property_email(prop_id, data)` |
| **Notes** | Internal annotations | `client.property_notes.list_property_notes(prop_id)` |
| **Tasks** | Workflow management | `client.property_tasks.create_property_task(prop_id, data)` |
| **Contacts** | Property-specific relationships | `client.property_contacts.list_property_contacts(prop_id)` |

## 🎯 Real-World Example

Here's a complete workflow for onboarding a new property listing:

```python
from open_to_close import OpenToCloseAPI
from datetime import datetime, timedelta

def onboard_new_listing():
    client = OpenToCloseAPI()
    
    # Create the property
    property_data = client.properties.create_property({
        "address": "456 Oak Avenue",
        "city": "Los Angeles",
        "state": "CA",
        "zip_code": "90210",
        "property_type": "Condo",
        "bedrooms": 2,
        "bathrooms": 2,
        "listing_price": 750000,
        "status": "Coming Soon"
    })
    
    # Create seller contact (using only reliably supported fields)
    seller = client.contacts.create_contact({
        "first_name": "Sarah",
        "last_name": "Johnson",
        "email": "sarah.johnson@email.com"
        # Note: "contact_type" field has limited API support
    })
    
    # Link seller to property
    client.property_contacts.create_property_contact(
        property_data["id"],
        {
            "contact_id": seller["id"],
            "role": "Seller",
            "primary": True
        }
    )
    
    # Add initial tasks
    client.property_tasks.create_property_task(
        property_data["id"],
        {
            "title": "Professional photography",
            "due_date": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
            "priority": "High"
        }
    )
    
    # Log initial note
    client.property_notes.create_property_note(
        property_data["id"],
        {
            "content": "Property onboarding completed. Ready for marketing.",
            "note_type": "Listing"
        }
    )
    
    return property_data

# Run the workflow
new_property = onboard_new_listing()
print(f"Successfully onboarded property: {new_property['address']}")
```

## 🔧 Advanced Configuration

### Environment-Specific Setup

```python
from open_to_close import OpenToCloseAPI

# Production
prod_client = OpenToCloseAPI(
    api_key="prod_key_here",
    base_url="https://api.opentoclose.com/v1"
)

# Development
dev_client = OpenToCloseAPI(
    api_key="dev_key_here",
    base_url="https://dev-api.opentoclose.com/v1"
)
```

### Error Handling

```python
from open_to_close import OpenToCloseAPI
from open_to_close.exceptions import (
    NotFoundError,
    ValidationError,
    AuthenticationError,
    RateLimitError
)

client = OpenToCloseAPI()

try:
    property_data = client.properties.retrieve_property(123)
except NotFoundError:
    print("Property not found")
except ValidationError as e:
    print(f"Invalid request: {e}")
except AuthenticationError:
    print("Check your API key")
except RateLimitError:
    print("Rate limit exceeded, retrying...")
```

## 📚 Documentation

- **[Complete Documentation](https://theperrygroup.github.io/open-to-close/)** - Full guides and API reference
- **[Getting Started](https://theperrygroup.github.io/open-to-close/getting-started/)** - Installation and setup
- **[API Reference](https://theperrygroup.github.io/open-to-close/api/)** - Detailed method documentation
- **[Examples](https://theperrygroup.github.io/open-to-close/guides/examples/)** - Real-world usage patterns
- **[Best Practices](https://theperrygroup.github.io/open-to-close/guides/best-practices/)** - Production guidelines

## 🧪 Testing

Run the test suite:

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests with coverage
pytest --cov=open_to_close --cov-report=term-missing

# Run with specific Python version
python -m pytest tests/
```

## 🛠️ Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/theperrygroup/open-to-close.git
cd open-to-close

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Code Quality

This project maintains high code quality standards:

- **Formatting**: [Black](https://black.readthedocs.io/)
- **Import Sorting**: [isort](https://pycqa.github.io/isort/)
- **Linting**: [flake8](https://flake8.pycqa.org/)
- **Type Checking**: [mypy](https://mypy.readthedocs.io/)
- **Testing**: [pytest](https://docs.pytest.org/) with 100% coverage

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](https://theperrygroup.github.io/open-to-close/development/contributing/) for details.

### Quick Contribution Steps

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Make** your changes with tests
4. **Ensure** all tests pass (`pytest`)
5. **Commit** your changes (`git commit -am 'Add amazing feature'`)
6. **Push** to the branch (`git push origin feature/amazing-feature`)
7. **Open** a Pull Request

## 📋 Requirements

- **Python**: 3.8 or higher
- **Dependencies**: `requests>=2.25.0`, `python-dotenv>=0.19.0`
- **API Access**: Valid Open To Close API key

## 🔗 Links

- **[PyPI Package](https://pypi.org/project/open-to-close/)**
- **[GitHub Repository](https://github.com/theperrygroup/open-to-close)**
- **[Documentation](https://theperrygroup.github.io/open-to-close/)**
- **[Issue Tracker](https://github.com/theperrygroup/open-to-close/issues)**
- **[Changelog](https://theperrygroup.github.io/open-to-close/reference/changelog/)**

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏢 About The Perry Group

The Open To Close API Python client is developed and maintained by [The Perry Group](https://theperry.group), a leading real estate technology company.

---

**Built with ❤️ for the real estate community** 