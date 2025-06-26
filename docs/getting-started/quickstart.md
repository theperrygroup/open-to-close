# Quick Start

Get up and running with the Open To Close API in under 5 minutes. This tutorial walks you through making your first API calls and exploring core functionality.

!!! note "Prerequisites"
    📋 Before starting, ensure you have:
    
    - Python 3.8+ installed
    - `open-to-close` package installed 
    - API key configured in environment variables

---

## 🚀 Your First API Call

Let's start with the most basic operation - initializing the client and making a simple request:

```python
from open_to_close import OpenToCloseAPI

# Initialize the client (uses OPEN_TO_CLOSE_API_KEY environment variable)
client = OpenToCloseAPI()

# Make your first API call
properties = client.properties.list_properties()
print(f"Found {len(properties)} properties in your account")
```

!!! success "Expected Output"
    ✅ You should see output like: `Found 42 properties in your account`

---

## 🏗️ Core Operations Tutorial

Let's explore the main operations you'll use with the Open To Close API:

### **Step 1: Working with Properties**

Properties are central to the Open To Close platform. Let's explore property operations:

=== ":material-list-box: List Properties"

    ```python
    # Get all properties (with pagination)
    properties = client.properties.list_properties()
    
    # Get properties with custom parameters
    recent_properties = client.properties.list_properties(
        params={"limit": 10, "sort": "-created_at"}
    )
    
    print(f"Total properties: {len(properties)}")
    print(f"Recent properties: {len(recent_properties)}")
    
    # Display property details
    for prop in recent_properties[:3]:
        print(f"Property {prop['id']}: {prop.get('address', 'No address')}")
    ```

=== ":material-plus: Create Property"

    ```python
    # 🆕 NEWEST: UI-friendly text values (v2.6.0+)
    ui_property = client.properties.create_property({
        "title": "Modern Downtown Condo",
        "client_type": "Buyer",                     # Stays as "Buyer" in UI
        "status": "Under Contract"                  # Stays as "Under Contract" in UI
    }, preserve_text_values=True)  # 🆕 NEW parameter for UI display
    
    # 🆕 NEW: Simplified property creation (v2.5.0+)
    # Just pass a title - uses smart defaults!
    simple_property = client.properties.create_property("Beautiful Family Home")
    
    # 🆕 NEW: Simple dictionary format with human-readable fields
    new_property = client.properties.create_property({
        "title": "Downtown Luxury Condo",           # Required
        "client_type": "Buyer",                     # "Buyer", "Seller", or "Dual"
        "status": "Active",                         # "Active", "Under Contract", etc.
        "purchase_amount": 525000                   # Optional dollar amount
    })
    
    # 🔧 LEGACY: Advanced API format (still supported)
    legacy_property = client.properties.create_property({
        "address": "123 Main Street",
        "city": "New York",
        "state": "NY",
        "zip_code": "10001",
        "property_type": "Single Family Home",
        "status": "Active"
    })
    
    print(f"Created property with ID: {new_property['id']}")
    print(f"Address: {new_property.get('address', 'Not specified')}")
    ```

    !!! success "v2.6.0 UI-Friendly Text Values"
        🆕 **LATEST**: Use `preserve_text_values=True` to keep human-readable text in the Open to Close UI! Solves the issue of numeric IDs being displayed instead of readable text.

        **Key Benefits:**
        - 📱 UI shows "Buyer" instead of "797212"
        - 🎯 Dropdowns preselect correctly with proper title case
        - 👀 Better user experience and data clarity
        - ✅ Fully backwards compatible

        **Important:** Use proper title case (`"Buyer"`, `"Under Contract"`) for UI recognition.

    !!! tip "v2.5.0 Simplified Creation"
        🎉 **NEW**: Property creation is now incredibly simple! Use `title`, `client_type`, and `status` fields with automatic field ID translation. The API wrapper handles all the complex formatting behind the scenes.

        **What happens automatically:**
        - 🔍 Auto-detects team member ID from your teams
        - 🎯 Smart defaults: Client type = "Buyer", Status = "Active"  
        - 🔄 Converts to complex API format transparently
        - 🛡️ Validates inputs with clear error messages

=== ":material-pencil: Update Property"

    ```python
    # Update an existing property
    property_id = new_property['id']  # From creation above
    
    updated_property = client.properties.update_property(property_id, {
        "status": "Under Contract",
        "notes": "Updated via API"
    })
    
    print(f"Updated property {property_id}")
    print(f"New status: {updated_property['status']}")
    ```

### **Step 2: Managing Contacts**

Contacts represent people involved in your real estate transactions:

=== ":material-account-group: List & Create Contacts"

    ```python
    # List existing contacts
    contacts = client.contacts.list_contacts(params={"limit": 5})
    print(f"Found {len(contacts)} contacts")
    
    # Create a new contact
    new_contact = client.contacts.create_contact({
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "contact_type": "Client"
    })
    
    print(f"Created contact: {new_contact['first_name']} {new_contact['last_name']}")
    ```

=== ":material-home-account: Link Contact to Property"

    ```python
    # Associate the contact with a property
    property_contact = client.property_contacts.create_property_contact(
        property_id=new_property['id'],
        contact_data={
            "contact_id": new_contact['id'],
            "role": "Buyer",
            "primary": True
        }
    )
    
    print(f"Linked contact {new_contact['id']} to property {new_property['id']}")
    print(f"Role: {property_contact['role']}")
    ```

### **Step 3: Adding Property Documentation**

Keep track of important documents and communications:

=== ":material-note-text: Add Notes"

    ```python
    # Add a note to the property
    note = client.property_notes.create_property_note(
        property_id=new_property['id'],
        note_data={
            "content": "Initial client consultation completed. Ready to schedule property showing.",
            "note_type": "General",
            "created_by": "API User"
        }
    )
    
    print(f"Added note {note['id']} to property {new_property['id']}")
    ```

=== ":material-calendar-check: Create Tasks"

    ```python
    # Create a task for the property
    task = client.property_tasks.create_property_task(
        property_id=new_property['id'],
        task_data={
            "title": "Schedule property inspection",
            "description": "Coordinate with buyer for property inspection appointment",
            "due_date": "2024-01-15",
            "priority": "High",
            "assigned_to": "Agent Name"
        }
    )
    
    print(f"Created task '{task['title']}' for property {new_property['id']}")
    ```

=== ":material-email: Track Communications"

    ```python
    # Log an email communication
    email = client.property_emails.create_property_email(
        property_id=new_property['id'],
        email_data={
            "subject": "Property Information Packet",
            "sender": "agent@realestate.com",
            "recipient": "john.doe@example.com",
            "body": "Please find attached the property information packet...",
            "sent_date": "2024-01-10T10:30:00Z"
        }
    )
    
    print(f"Logged email communication: {email['subject']}")
    ```

---

## 📋 Working with Teams and Users

Manage your team and user assignments:

```python
# List teams in your organization
teams = client.teams.list_teams()
print(f"Available teams: {len(teams)}")

# List users
users = client.users.list_users(params={"limit": 10})
print(f"Team members: {len(users)}")

# Get agents (users with agent role)
agents = client.agents.list_agents()
print(f"Active agents: {len(agents)}")

# Display team information
for team in teams[:3]:
    print(f"Team: {team.get('name', 'Unnamed')} (ID: {team['id']})")
```

---

## 🔍 Real-World Example: Complete Property Workflow

Let's combine everything into a realistic workflow - onboarding a new property listing:

```python
from open_to_close import OpenToCloseAPI
from datetime import datetime, timedelta

def onboard_new_listing():
    """Complete workflow for onboarding a new property listing."""
    client = OpenToCloseAPI()
    
    print("🏠 Starting property onboarding workflow...")
    
    # Step 1: Create the property
    property_data = client.properties.create_property({
        "address": "456 Oak Avenue",
        "city": "Los Angeles", 
        "state": "CA",
        "zip_code": "90210",
        "property_type": "Condo",
        "bedrooms": 2,
        "bathrooms": 2,
        "square_feet": 1200,
        "listing_price": 750000,
        "status": "Coming Soon"
    })
    
    property_id = property_data['id']
    print(f"✅ Created property {property_id}: {property_data['address']}")
    
    # Step 2: Create and link the seller contact
    seller = client.contacts.create_contact({
        "first_name": "Sarah",
        "last_name": "Johnson", 
        "email": "sarah.johnson@email.com",
        "phone": "+1555123456",
        "contact_type": "Seller"
    })
    
    # Link seller to property
    client.property_contacts.create_property_contact(
        property_id=property_id,
        contact_data={
            "contact_id": seller['id'],
            "role": "Seller",
            "primary": True
        }
    )
    print(f"✅ Linked seller {seller['first_name']} {seller['last_name']} to property")
    
    # Step 3: Add initial documentation
    intake_note = client.property_notes.create_property_note(
        property_id=property_id,
        note_data={
            "content": "Property intake completed. Seller motivated to close within 60 days. Property has been recently updated with new flooring and paint.",
            "note_type": "Intake"
        }
    )
    print(f"✅ Added intake notes")
    
    # Step 4: Create initial tasks
    tasks = [
        {
            "title": "Professional photography",
            "description": "Schedule photographer for listing photos",
            "due_date": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
            "priority": "High"
        },
        {
            "title": "Comparative Market Analysis",
            "description": "Complete CMA to verify listing price",
            "due_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "priority": "High"
        },
        {
            "title": "Prepare listing documents",
            "description": "Gather all required listing paperwork",
            "due_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
            "priority": "Medium"
        }
    ]
    
    for task_data in tasks:
        task = client.property_tasks.create_property_task(
            property_id=property_id,
            task_data=task_data
        )
        print(f"✅ Created task: {task['title']}")
    
    # Step 5: Log initial communication
    welcome_email = client.property_emails.create_property_email(
        property_id=property_id,
        email_data={
            "subject": "Welcome to Our Listing Process",
            "sender": "agent@realestate.com",
            "recipient": seller['email'],
            "body": "Thank you for choosing us to list your property. We've created your property profile and initial action items.",
            "sent_date": datetime.now().isoformat()
        }
    )
    print(f"✅ Logged welcome email to seller")
    
    print(f"\n🎉 Property onboarding complete!")
    print(f"Property ID: {property_id}")
    print(f"Address: {property_data['address']}")
    print(f"Seller: {seller['first_name']} {seller['last_name']}")
    print(f"Tasks created: {len(tasks)}")
    
    return property_id

# Run the workflow
if __name__ == "__main__":
    property_id = onboard_new_listing()
```

---

## 🔧 Error Handling Example

Always implement proper error handling in production code:

```python
from open_to_close import OpenToCloseAPI
from open_to_close.exceptions import (
    NotFoundError, 
    ValidationError, 
    AuthenticationError,
    OpenToCloseAPIError
)

def safe_api_operations():
    """Example of proper error handling."""
    client = OpenToCloseAPI()
    
    try:
        # Attempt to retrieve a property
        property_data = client.properties.retrieve_property(999999)
        print(f"Found property: {property_data['address']}")
        
    except NotFoundError:
        print("❌ Property not found - check the property ID")
        
    except ValidationError as e:
        print(f"❌ Invalid request parameters: {e}")
        
    except AuthenticationError:
        print("❌ Authentication failed - check your API key")
        
    except OpenToCloseAPIError as e:
        print(f"❌ API error occurred: {e}")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

# Test error handling
safe_api_operations()
```

---

## 📊 Quick Data Exploration

Get a quick overview of your data:

```python
def explore_account_data():
    """Get an overview of data in your account."""
    client = OpenToCloseAPI()
    
    try:
        # Get counts of main resources
        properties = client.properties.list_properties(params={"limit": 1000})
        contacts = client.contacts.list_contacts(params={"limit": 1000})
        agents = client.agents.list_agents()
        teams = client.teams.list_teams()
        
        print("📊 Account Data Overview")
        print("-" * 30)
        print(f"Properties: {len(properties)}")
        print(f"Contacts: {len(contacts)}")
        print(f"Agents: {len(agents)}")
        print(f"Teams: {len(teams)}")
        
        # Show recent activity (if properties exist)
        if properties:
            print(f"\nRecent Properties:")
            for prop in properties[:5]:
                print(f"  • {prop.get('address', 'No address')} ({prop.get('status', 'No status')})")
        
    except Exception as e:
        print(f"Error exploring data: {e}")

# Run data exploration
explore_account_data()
```

---

## 🚀 Next Steps

Congratulations! You've successfully made your first API calls. Here's what to explore next:

### **Immediate Next Steps**
1. **[API Reference](../api/index.md)** - Explore all available operations
2. **[Properties API](../api/properties.md)** - Complete property management documentation
3. **[Guides](../guides/index.md)** - Usage patterns and examples

### **Explore More Features**
- **[API Reference](../api/index.md)** - Complete documentation of all available methods
- **[Guides](../guides/index.md)** - More real-world usage scenarios
- **[Guides](../guides/index.md)** - Common integration approaches and patterns

### **Build Something Real**
Try implementing these common scenarios:
- Build a property dashboard
- Create an automated workflow
- Integrate with your CRM system
- Set up data synchronization

---

## 🎯 Quick Reference

### **Common Operations**
```python
# Initialize client
client = OpenToCloseAPI()

# Core resource operations
properties = client.properties.list_properties()
property = client.properties.retrieve_property(123)
new_property = client.properties.create_property(data)

# Property sub-resources
notes = client.property_notes.list_property_notes(property_id)
tasks = client.property_tasks.list_property_tasks(property_id)
contacts = client.property_contacts.list_property_contacts(property_id)
```

### **Resource Types**
- **Properties**: Real estate listings and transactions
- **Contacts**: People involved in transactions
- **Agents**: Team members with agent roles
- **Teams**: Organizational groups
- **Users**: All system users
- **Tags**: Classification and organization

### **Sub-Resources (Property-specific)**
- **Documents**: File attachments
- **Emails**: Communication history  
- **Notes**: Internal annotations
- **Tasks**: Work items and reminders
- **Contacts**: People associated with specific properties

---

*You're now ready to build powerful applications with the Open To Close API! 🎉* 