# Contacts API

The Contacts API manages people involved in real estate transactions including buyers, sellers, lenders, inspectors, and other stakeholders. This is essential for maintaining relationships and tracking communication throughout the transaction process.

!!! abstract "ContactsAPI Client"
    Access via `client.contacts` - provides full CRUD operations for contact management.

---

## 🚀 Quick Start

```python
from open_to_close import OpenToCloseAPI

client = OpenToCloseAPI()

# List all contacts
contacts = client.contacts.list_contacts()

# Get a specific contact
contact_data = client.contacts.retrieve_contact(123)

# Create a new contact
new_contact = client.contacts.create_contact({
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@email.com",
    "phone": "+1234567890",
    "contact_type": "Buyer"
})
```

---

## 📋 Available Methods

| Method | Description | HTTP Endpoint |
|--------|-------------|---------------|
| `list_contacts()` | Get all contacts with optional filtering | `GET /contacts` |
| `create_contact()` | Create a new contact | `POST /contacts` |
| `retrieve_contact()` | Get a specific contact by ID | `GET /contacts/{id}` |
| `update_contact()` | Update an existing contact | `PUT /contacts/{id}` |
| `delete_contact()` | Delete a contact by ID | `DELETE /contacts/{id}` |

---

## 🔍 Method Documentation

### **list_contacts()**

Retrieve a list of contacts with optional filtering and pagination.

```python
def list_contacts(
    self, 
    params: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]
```

**Parameters:**

| Name | Type | Required | Description | Default |
|------|------|----------|-------------|---------|
| `params` | `Dict[str, Any]` | No | Query parameters for filtering, pagination, and sorting | `None` |

**Returns:**

| Type | Description |
|------|-------------|
| `List[Dict[str, Any]]` | List of contact dictionaries |

**Common Query Parameters:**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `limit` | `int` | Maximum number of results to return | `50` |
| `offset` | `int` | Number of results to skip for pagination | `100` |
| `contact_type` | `string` | Filter by contact type | `"Buyer"` |
| `search` | `string` | Search in name, email, or phone | `"john"` |
| `sort` | `string` | Sort field and direction | `"last_name"` |

=== ":material-list-box: Basic Listing"

    ```python
    # Get all contacts
    contacts = client.contacts.list_contacts()
    print(f"Found {len(contacts)} contacts")
    
    # Display basic info
    for contact in contacts:
        name = f"{contact.get('first_name', '')} {contact.get('last_name', '')}".strip()
        print(f"Contact {contact['id']}: {name or 'No name'}")
    ```

=== ":material-filter: Filtered Results"

    ```python
    # Get buyers only
    buyers = client.contacts.list_contacts(params={
        "contact_type": "Buyer",
        "limit": 25
    })
    
    # Search for specific contacts
    johns = client.contacts.list_contacts(params={
        "search": "john",
        "sort": "last_name"
    })
    ```

=== ":material-page-next: Pagination"

    ```python
    # Paginate through all contacts
    all_contacts = []
    offset = 0
    limit = 100
    
    while True:
        batch = client.contacts.list_contacts(params={
            "limit": limit,
            "offset": offset
        })
        
        if not batch:
            break
            
        all_contacts.extend(batch)
        offset += limit
    
    print(f"Total contacts: {len(all_contacts)}")
    ```

---

### **create_contact()**

Create a new contact with the provided data.

```python
def create_contact(
    self, 
    contact_data: Dict[str, Any]
) -> Dict[str, Any]
```

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `contact_data` | `Dict[str, Any]` | Yes | Dictionary containing contact information |

**Returns:**

| Type | Description |
|------|-------------|
| `Dict[str, Any]` | Created contact data with assigned ID |

**Common Contact Fields:**

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `first_name` | `string` | No | Contact's first name | `"John"` |
| `last_name` | `string` | No | Contact's last name | `"Doe"` |
| `email` | `string` | No | Email address | `"john@email.com"` |
| `phone` | `string` | No | Phone number | `"+1234567890"` |
| `contact_type` | `string` | No | Type of contact | `"Buyer"` |
| `company` | `string` | No | Company name | `"ABC Realty"` |
| `address` | `string` | No | Street address | `"123 Main St"` |
| `city` | `string` | No | City | `"New York"` |
| `state` | `string` | No | State | `"NY"` |
| `zip_code` | `string` | No | ZIP code | `"10001"` |

=== ":material-plus: Basic Creation"

    ```python
    # Create a basic contact
    new_contact = client.contacts.create_contact({
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@email.com",
        "phone": "+1555123456"
    })
    
    print(f"Created contact with ID: {new_contact['id']}")
    print(f"Name: {new_contact['first_name']} {new_contact['last_name']}")
    ```

=== ":material-account-group: Complete Profile"

    ```python
    # Create a comprehensive contact profile
    contact_data = {
        "first_name": "Michael",
        "last_name": "Johnson",
        "email": "michael.johnson@email.com",
        "phone": "+1555987654",
        "contact_type": "Seller",
        "company": "Johnson Enterprises",
        "address": "456 Oak Avenue",
        "city": "Los Angeles",
        "state": "CA",
        "zip_code": "90210",
        "preferred_contact_method": "email",
        "notes": "Prefers morning communications"
    }
    
    new_contact = client.contacts.create_contact(contact_data)
    print(f"Created {new_contact['contact_type']}: {new_contact['first_name']} {new_contact['last_name']}")
    ```

=== ":material-business: Business Contact"

    ```python
    # Create a business/professional contact
    business_contact = client.contacts.create_contact({
        "first_name": "Sarah",
        "last_name": "Williams",
        "email": "sarah@inspectionpro.com",
        "phone": "+1555456789",
        "contact_type": "Inspector",
        "company": "Professional Inspections Inc",
        "license_number": "INS789456",
        "specialties": ["Home Inspection", "Commercial Inspection"]
    })
    ```

---

### **retrieve_contact()**

Get detailed information about a specific contact by their ID.

```python
def retrieve_contact(
    self, 
    contact_id: int
) -> Dict[str, Any]
```

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `contact_id` | `int` | Yes | Unique identifier of the contact to retrieve |

**Returns:**

| Type | Description |
|------|-------------|
| `Dict[str, Any]` | Complete contact data dictionary |

=== ":material-magnify: Basic Retrieval"

    ```python
    # Get a specific contact
    contact_data = client.contacts.retrieve_contact(123)
    
    name = f"{contact_data.get('first_name', '')} {contact_data.get('last_name', '')}".strip()
    print(f"Contact: {name}")
    print(f"Email: {contact_data.get('email', 'Not provided')}")
    print(f"Type: {contact_data.get('contact_type', 'Unknown')}")
    ```

=== ":material-information: Detailed Display"

    ```python
    # Display comprehensive contact information
    contact_data = client.contacts.retrieve_contact(123)
    
    print("=== Contact Profile ===")
    print(f"ID: {contact_data['id']}")
    print(f"Name: {contact_data.get('first_name', '')} {contact_data.get('last_name', '')}")
    print(f"Email: {contact_data.get('email', 'Not specified')}")
    print(f"Phone: {contact_data.get('phone', 'Not specified')}")
    print(f"Type: {contact_data.get('contact_type', 'Not specified')}")
    print(f"Company: {contact_data.get('company', 'Not specified')}")
    
    if contact_data.get('address'):
        print(f"Address: {contact_data['address']}")
        if contact_data.get('city'):
            print(f"City: {contact_data['city']}, {contact_data.get('state', '')} {contact_data.get('zip_code', '')}")
    ```

=== ":material-shield-check: Error Handling"

    ```python
    from open_to_close.exceptions import NotFoundError
    
    def safe_get_contact(contact_id):
        try:
            contact_data = client.contacts.retrieve_contact(contact_id)
            return contact_data
        except NotFoundError:
            print(f"Contact {contact_id} not found")
            return None
        except Exception as e:
            print(f"Error retrieving contact {contact_id}: {e}")
            return None
    
    # Usage
    contact_data = safe_get_contact(123)
    if contact_data:
        name = f"{contact_data.get('first_name', '')} {contact_data.get('last_name', '')}".strip()
        print(f"Found contact: {name}")
    ```

---

### **update_contact()**

Update an existing contact with new or modified data.

```python
def update_contact(
    self, 
    contact_id: int, 
    contact_data: Dict[str, Any]
) -> Dict[str, Any]
```

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `contact_id` | `int` | Yes | Unique identifier of the contact to update |
| `contact_data` | `Dict[str, Any]` | Yes | Dictionary containing fields to update |

**Returns:**

| Type | Description |
|------|-------------|
| `Dict[str, Any]` | Updated contact data |

=== ":material-pencil: Basic Updates"

    ```python
    # Update contact information
    updated_contact = client.contacts.update_contact(123, {
        "email": "new.email@domain.com",
        "phone": "+1555999888"
    })
    
    # Update contact type
    updated_contact = client.contacts.update_contact(123, {
        "contact_type": "Seller"
    })
    
    print(f"Updated contact {updated_contact['id']}")
    ```

=== ":material-account-edit: Profile Changes"

    ```python
    # Update contact address
    def update_contact_address(contact_id, address_info):
        return client.contacts.update_contact(contact_id, {
            "address": address_info["address"],
            "city": address_info["city"],
            "state": address_info["state"],
            "zip_code": address_info["zip_code"],
            "address_updated": datetime.now().isoformat()
        })
    
    # Update contact preferences
    def update_contact_preferences(contact_id, preferences):
        return client.contacts.update_contact(contact_id, {
            "preferred_contact_method": preferences.get("method", "email"),
            "contact_notes": preferences.get("notes"),
            "best_contact_time": preferences.get("time")
        })
    
    # Usage
    updated_contact = update_contact_address(123, {
        "address": "789 New Street",
        "city": "Miami",
        "state": "FL",
        "zip_code": "33101"
    })
    ```

=== ":material-update: Status Management"

    ```python
    # Contact status management functions
    def mark_contact_active(contact_id):
        return client.contacts.update_contact(contact_id, {
            "status": "Active",
            "status_updated": datetime.now().isoformat()
        })
    
    def archive_contact(contact_id, reason=None):
        update_data = {
            "status": "Archived",
            "archived_date": datetime.now().isoformat()
        }
        if reason:
            update_data["archive_reason"] = reason
        
        return client.contacts.update_contact(contact_id, update_data)
    
    # Usage
    active_contact = mark_contact_active(123)
    archived_contact = archive_contact(124, "Transaction completed")
    ```

---

### **delete_contact()**

Delete a contact from the system. Use with caution as this action may be irreversible.

```python
def delete_contact(
    self, 
    contact_id: int
) -> Dict[str, Any]
```

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `contact_id` | `int` | Yes | Unique identifier of the contact to delete |

**Returns:**

| Type | Description |
|------|-------------|
| `Dict[str, Any]` | Deletion confirmation response |

!!! warning "Permanent Action"
    ⚠️ Contact deletion may be permanent and could affect related records (properties, communications, transactions). Consider updating the status to "Archived" instead of deleting when possible.

=== ":material-delete: Basic Deletion"

    ```python
    # Delete a contact
    result = client.contacts.delete_contact(123)
    print("Contact deleted successfully")
    ```

=== ":material-shield-alert: Safe Deletion"

    ```python
    def safe_delete_contact(contact_id, confirm=False):
        """Safely delete a contact with confirmation."""
        if not confirm:
            print("This will permanently delete the contact.")
            print("Call with confirm=True to proceed.")
            return None
            
        try:
            # Get contact info before deletion
            contact_data = client.contacts.retrieve_contact(contact_id)
            name = f"{contact_data.get('first_name', '')} {contact_data.get('last_name', '')}".strip()
            
            result = client.contacts.delete_contact(contact_id)
            print(f"Contact {name} (ID: {contact_id}) deleted successfully")
            return result
            
        except Exception as e:
            print(f"Error deleting contact {contact_id}: {e}")
            return None
    
    # Usage
    safe_delete_contact(123, confirm=True)
    ```

---

## 🏗️ Common Contact Workflows

### **Lead Management Workflow**

```python
def create_lead_from_inquiry(inquiry_data):
    """Convert an inquiry into a contact lead."""
    
    # Create contact from inquiry
    contact_data = {
        "first_name": inquiry_data.get("first_name"),
        "last_name": inquiry_data.get("last_name"),
        "email": inquiry_data.get("email"),
        "phone": inquiry_data.get("phone"),
        "contact_type": "Lead",
        "lead_source": inquiry_data.get("source", "Website"),
        "inquiry_date": datetime.now().isoformat(),
        "notes": inquiry_data.get("message", "")
    }
    
    new_contact = client.contacts.create_contact(contact_data)
    
    print(f"Created lead: {new_contact['first_name']} {new_contact['last_name']}")
    return new_contact

# Usage
lead = create_lead_from_inquiry({
    "first_name": "Emily",
    "last_name": "Davis",
    "email": "emily.davis@email.com",
    "phone": "+1555741852",
    "source": "Referral",
    "message": "Interested in downtown condos"
})
```

### **Contact Relationship Management**

```python
class ContactManager:
    """Helper class for managing contact operations."""
    
    def __init__(self, client):
        self.client = client
    
    def find_contacts_by_type(self, contact_type):
        """Get all contacts of a specific type."""
        return self.client.contacts.list_contacts(params={
            "contact_type": contact_type
        })
    
    def search_contacts(self, search_term):
        """Search contacts by name, email, or phone."""
        return self.client.contacts.list_contacts(params={
            "search": search_term,
            "limit": 50
        })
    
    def get_contact_summary(self, contact_id):
        """Get comprehensive contact information."""
        try:
            contact = self.client.contacts.retrieve_contact(contact_id)
            
            summary = {
                "basic_info": {
                    "name": f"{contact.get('first_name', '')} {contact.get('last_name', '')}".strip(),
                    "email": contact.get("email"),
                    "phone": contact.get("phone"),
                    "type": contact.get("contact_type")
                },
                "company_info": {
                    "company": contact.get("company"),
                    "title": contact.get("title")
                },
                "address": {
                    "street": contact.get("address"),
                    "city": contact.get("city"),
                    "state": contact.get("state"),
                    "zip": contact.get("zip_code")
                }
            }
            
            return summary
            
        except Exception as e:
            print(f"Error getting contact summary: {e}")
            return None
    
    def convert_lead_to_client(self, contact_id, new_type="Buyer"):
        """Convert a lead to an active client."""
        return self.client.contacts.update_contact(contact_id, {
            "contact_type": new_type,
            "conversion_date": datetime.now().isoformat(),
            "status": "Active Client"
        })

# Usage
contact_manager = ContactManager(client)
buyers = contact_manager.find_contacts_by_type("Buyer")
search_results = contact_manager.search_contacts("john")
contact_summary = contact_manager.get_contact_summary(123)
```

---

## 🆘 Error Handling

All contact methods can raise these exceptions:

!!! warning "Common Exceptions"
    - **`AuthenticationError`**: Invalid or missing API key
    - **`ValidationError`**: Invalid contact data or parameters
    - **`NotFoundError`**: Contact not found (retrieve, update, delete)
    - **`OpenToCloseAPIError`**: General API error

```python
from open_to_close.exceptions import (
    NotFoundError, 
    ValidationError, 
    AuthenticationError
)

def robust_contact_operations(contact_id):
    """Example of comprehensive error handling."""
    try:
        # Attempt contact operations
        contact_data = client.contacts.retrieve_contact(contact_id)
        
        updated_contact = client.contacts.update_contact(contact_id, {
            "status": "Active"
        })
        
        return updated_contact
        
    except NotFoundError:
        print(f"Contact {contact_id} does not exist")
        return None
        
    except ValidationError as e:
        print(f"Invalid data provided: {e}")
        return None
        
    except AuthenticationError:
        print("Authentication failed - check your API key")
        return None
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
```

---

## 📚 Related Resources

**Related APIs:**
- **[Properties API](properties.md)** - Link contacts to properties
- **[Property Contacts API](property-contacts.md)** - Manage property-contact relationships
- **[Agents API](agents.md)** - Agent contact management
- **[Property Emails API](property-emails.md)** - Communication tracking

---

*Contacts are essential for relationship management in real estate. Master these operations to build comprehensive CRM functionality.* 