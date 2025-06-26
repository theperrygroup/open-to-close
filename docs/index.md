# Open To Close API Python Client

A modern, type-safe Python wrapper for the Open To Close API. Manage properties, agents, contacts, and more with a clean, intuitive interface.

!!! success "✅ Production Ready"
    Version 2.2.8 with comprehensive test coverage and **100% verified API endpoint support**. All endpoint issues have been resolved and tested.

!!! success "🎉 v2.5.0 Update: Simplified Property Creation"
    **Major new feature**: Property creation is now incredibly simple! Use human-readable field names with automatic field ID translation.

    ```python
    # Before (complex)
    property = client.properties.create_property({
        "team_member_id": 26392,
        "time_zone_id": 1,
        "fields": [{"id": 926565, "value": "My Property"}]
    })
    
    # After (simple) ✨
    property = client.properties.create_property({
        "title": "My Property",
        "client_type": "Buyer", 
        "status": "Active"
    })
    ```

    [Learn more about simplified property creation →](property-creation-guide.md){ .md-button .md-button--primary }

---

## 🚀 Quick Start

<div class="grid cards" markdown>

-   :material-download:{ .lg .middle } **Installation**

    ---

    Install the Python client and set up your development environment

    [:octicons-arrow-right-24: Install Now](getting-started/installation.md)

-   :material-key-variant:{ .lg .middle } **Authentication**

    ---

    Configure your API key and start making authenticated requests

    [:octicons-arrow-right-24: Setup Authentication](getting-started/authentication.md)

-   :material-rocket-launch:{ .lg .middle } **Quick Start Guide**

    ---

    Make your first API call and explore basic operations in minutes

    [:octicons-arrow-right-24: Start Tutorial](getting-started/quickstart.md)

-   :material-api:{ .lg .middle } **API Reference**

    ---

    Complete method documentation with examples and parameters

    [:octicons-arrow-right-24: View API Docs](api/index.md)

</div>

---

## 🏗️ Core Features

### **Resource Management**
- **Properties**: Complete property lifecycle management with CRUD operations
- **Agents**: Agent profiles, contact information, and team assignments  
- **Contacts**: Customer and lead management with relationship tracking
- **Teams**: Team organization and user management

### **Property Sub-Resources**
- **Documents**: File attachments and document management per property
- **Emails**: Email tracking and communication history
- **Notes**: Internal notes and annotations for properties
- **Tasks**: Task management and workflow automation
- **Contacts**: Property-specific contact relationships

### **Advanced Capabilities**
- **Type Safety**: Full type hints and IDE support for better development experience
- **Error Handling**: Comprehensive exception handling with detailed error messages
- **Rate Limiting**: Built-in respect for API rate limits and automatic retries
- **Lazy Loading**: Efficient client initialization with on-demand service loading

---

## 📋 API Overview

=== ":material-home: Core Resources"

    ```python
    from open_to_close import OpenToCloseAPI
    
    # Initialize client
    client = OpenToCloseAPI()
    
    # Core resource operations
    properties = client.properties.list_properties()
    agents = client.agents.list_agents()
    contacts = client.contacts.list_contacts()
    teams = client.teams.list_teams()
    users = client.users.list_users()
    tags = client.tags.list_tags()
    ```

=== ":material-file-document: Property Resources"

    ```python
    # Property-specific operations
    property_id = 123
    
    # Manage property documents
    documents = client.property_documents.list_property_documents(property_id)
    
    # Track emails and communication
    emails = client.property_emails.list_property_emails(property_id)
    
    # Handle notes and tasks
    notes = client.property_notes.list_property_notes(property_id)
    tasks = client.property_tasks.list_property_tasks(property_id)
    
    # Manage property contacts
    contacts = client.property_contacts.list_property_contacts(property_id)
    ```

=== ":material-cog: Error Handling"

    ```python
    from open_to_close import OpenToCloseAPI
    from open_to_close.exceptions import NotFoundError, ValidationError
    
    client = OpenToCloseAPI()
    
    try:
        property_data = client.properties.retrieve_property(123)
    except NotFoundError:
        print("Property not found")
    except ValidationError as e:
        print(f"Invalid request: {e}")
    ```

---

## 🎯 Key Benefits

!!! tip "Developer Experience"
    💡 Built with modern Python best practices including type hints, comprehensive docstrings, and IDE-friendly design.

!!! info "Complete Coverage"
    📋 Supports all Open To Close API endpoints with consistent patterns and full CRUD operations.

!!! success "Production Ready"
    ✅ Comprehensive test suite, error handling, and production-ready code with rate limiting support.

!!! check "Endpoint Reliability"
    🎯 **100% Success Rate**: All 6 core endpoints (Properties, Contacts, Agents, Teams, Users, Tags) have been tested and verified working with full CRUD operations.

---

## 📚 Documentation Sections

### **Getting Started**
Perfect for new users and initial setup:

- **[Installation Guide](getting-started/installation.md)** - Set up the client library
- **[Authentication Setup](getting-started/authentication.md)** - Configure API access
- **[Quick Start Tutorial](getting-started/quickstart.md)** - Your first API calls

### **API Reference**
Complete technical documentation:

- **[API Overview](api/index.md)** - Core resources and endpoints
- **[Properties](api/properties.md)** - Property management operations

### **Guides & Examples**
Practical usage and best practices:

- **[Guides Overview](guides/index.md)** - Usage patterns and examples

---

## 🔍 Quick Access

!!! example "Live Example"
    ```python
    from open_to_close import OpenToCloseAPI
    
    # Initialize with automatic API key detection
    client = OpenToCloseAPI()
    
    # Create a new property
    property_data = client.properties.create_property({
        "address": "123 Main St",
        "city": "New York",
        "state": "NY",
        "zip_code": "10001"
    })
    
    # Add a note to the property
    note = client.property_notes.create_property_note(
        property_data["id"],
        {"content": "Initial property intake completed"}
    )
    
    print(f"Created property {property_data['id']} with note {note['id']}")
    ```

---

## 🚀 Next Steps

New to the Open To Close API? Start here:

1. **[Install the client](getting-started/installation.md)** - Get up and running in minutes
2. **[Configure authentication](getting-started/authentication.md)** - Set up your API key
3. **[Try the quick start](getting-started/quickstart.md)** - Make your first API call
4. **[Explore guides](guides/index.md)** - See usage patterns and examples

Already familiar with the basics? Jump to:

- **[API Reference](api/index.md)** - Complete method documentation
- **[Properties API](api/properties.md)** - Property management operations
- **[Guides](guides/index.md)** - Usage patterns and examples

---

*Open To Close API Python Client - Built for modern Python development* 