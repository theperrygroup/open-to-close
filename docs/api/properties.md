# Properties API

The Properties API provides complete lifecycle management for real estate properties. This is the central resource in the Open To Close platform, representing individual properties, listings, and transactions.

!!! abstract "PropertiesAPI Client"
    Access via `client.properties` - provides full CRUD operations for property management.

!!! success "v2.5.0 NEW: Simplified Property Creation"
    🎉 **Major Update**: Property creation is now incredibly simple! Use human-readable field names with automatic field ID translation.

    ```python
    # ✨ Simple title only
    property = client.properties.create_property("Beautiful Family Home")
    
    # ✨ Simple dictionary format  
    property = client.properties.create_property({
        "title": "Downtown Condo",
        "client_type": "Buyer",    # "Buyer", "Seller", "Dual"
        "status": "Active"         # "Active", "Under Contract", etc.
    })
    ```

    **Available Field Names:**
    - `title` or `contract_title` - Property title (required)
    - `client_type` or `contract_client_type` - "Buyer", "Seller", "Dual" 
    - `status` or `contract_status` - "Active", "Under Contract", "Closed", etc.

    **What's Automatic:**
    - Field ID lookup and translation
    - Team member auto-detection
    - Smart defaults (Buyer + Active status)
    - Input validation with clear error messages

---

## 🔍 Field Discovery (v2.5.0+)

Discover available fields and validate data before creating properties:

```python
# List all available fields with metadata
fields = client.list_available_fields()
for field in fields[:5]:
    print(f"Field: {field['key']} - {field['title']} ({field['type']})")

# Validate property data before creation
data = {"title": "Test Property", "client_type": "Buyer"}
is_valid, errors = client.validate_property_data(data)
if not is_valid:
    print(f"Validation errors: {errors}")
```

---

## 🚀 Quick Start

```python
from open_to_close import OpenToCloseAPI

client = OpenToCloseAPI()

# List all properties
properties = client.properties.list_properties()

# Get a specific property
property_data = client.properties.retrieve_property(123)

# Create a new property
new_property = client.properties.create_property({
    "address": "123 Main Street",
    "city": "New York",
    "state": "NY",
    "zip_code": "10001"
})
```

---

## 📋 Available Methods

| Method | Description | HTTP Endpoint |
|--------|-------------|---------------|
| `list_properties()` | Get all properties with optional filtering | `GET /properties` |
| `create_property()` | Create a new property | `POST /properties` |
| `retrieve_property()` | Get a specific property by ID | `GET /properties/{id}` |
| `update_property()` | Update an existing property | `PUT /properties/{id}` |
| `delete_property()` | Delete a property by ID | `DELETE /properties/{id}` |

---

## 🔍 Method Documentation

### **list_properties()**

Retrieve a list of properties with optional filtering and pagination.

```python
def list_properties(
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
| `List[Dict[str, Any]]` | List of property dictionaries |

**Common Query Parameters:**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `limit` | `int` | Maximum number of results to return | `50` |
| `offset` | `int` | Number of results to skip for pagination | `100` |
| `status` | `string` | Filter by property status | `"Active"` |
| `city` | `string` | Filter by city | `"New York"` |
| `state` | `string` | Filter by state | `"NY"` |
| `sort` | `string` | Sort field and direction | `"-created_at"` |

=== ":material-list-box: Basic Listing"

    ```python
    # Get all properties
    properties = client.properties.list_properties()
    print(f"Found {len(properties)} properties")
    
    # Display basic info
    for prop in properties:
        print(f"Property {prop['id']}: {prop.get('address', 'No address')}")
    ```

=== ":material-filter: Filtered Results"

    ```python
    # Get active properties in New York
    active_ny_properties = client.properties.list_properties(params={
        "status": "Active",
        "state": "NY",
        "limit": 25
    })
    
    # Get recently created properties
    recent_properties = client.properties.list_properties(params={
        "sort": "-created_at",
        "limit": 10
    })
    ```

=== ":material-page-next: Pagination"

    ```python
    # Paginate through all properties
    all_properties = []
    offset = 0
    limit = 100
    
    while True:
        batch = client.properties.list_properties(params={
            "limit": limit,
            "offset": offset
        })
        
        if not batch:
            break
            
        all_properties.extend(batch)
        offset += limit
    
    print(f"Total properties: {len(all_properties)}")
    ```

---

### **create_property()**

Create a new property with simple human-readable fields or advanced API format.

```python
def create_property(
    self, 
    property_data: Union[str, Dict[str, Any]],
    team_member_id: Optional[int] = None
) -> Dict[str, Any]
```

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `property_data` | `Union[str, Dict[str, Any]]` | Yes | Property title (string) or property data (dictionary) |
| `team_member_id` | `Optional[int]` | No | Override auto-detected team member ID |

**Returns:**

| Type | Description |
|------|-------------|
| `Dict[str, Any]` | Created property data with assigned ID |

**✨ NEW: Simplified Format (v2.5.0+)**

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `title` | `string` | Yes | Property title | `"Beautiful Family Home"` |
| `client_type` | `string` | No | Client relationship | `"Buyer"`, `"Seller"`, `"Dual"` |
| `status` | `string` | No | Property status | `"Active"`, `"Under Contract"`, `"Closed"` |
| `purchase_amount` | `number` | No | Purchase amount | `450000` |

**🔧 Legacy Format (Still Supported)**

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `address` | `string` | No | Street address | `"123 Main Street"` |
| `city` | `string` | No | City name | `"New York"` |
| `state` | `string` | No | State abbreviation | `"NY"` |
| `zip_code` | `string` | No | ZIP or postal code | `"10001"` |
| `property_type` | `string` | No | Type of property | `"Single Family Home"` |
| `bedrooms` | `integer` | No | Number of bedrooms | `3` |
| `bathrooms` | `number` | No | Number of bathrooms | `2.5` |
| `square_feet` | `integer` | No | Square footage | `1500` |
| `listing_price` | `number` | No | Listing price | `450000` |
| `status` | `string` | No | Property status | `"Active"` |

=== ":sparkles: NEW: Simple Format"

    ```python
    # 1. Just a title (uses smart defaults)
    property1 = client.properties.create_property("Beautiful Family Home")
    
    # 2. Simple dictionary with common fields
    property2 = client.properties.create_property({
        "title": "Downtown Luxury Condo",
        "client_type": "Buyer",
        "status": "Active", 
        "purchase_amount": 525000
    })
    
    # 3. Seller listing
    property3 = client.properties.create_property({
        "title": "Suburban Family Home",
        "client_type": "Seller",
        "status": "Pre-MLS",
        "purchase_amount": 675000
    })
    
    print(f"Created property: {property2['id']}")
    ```

=== ":material-plus: Legacy Format"

    ```python
    # Traditional comprehensive format (still works)
    property_data = {
        "address": "789 Pine Street",
        "city": "Chicago",
        "state": "IL",
        "zip_code": "60601",
        "property_type": "Condo",
        "bedrooms": 2,
        "bathrooms": 2,
        "square_feet": 1200,
        "listing_price": 350000,
        "status": "Coming Soon",
        "description": "Beautiful downtown condo with city views",
        "year_built": 2015,
        "parking_spaces": 1,
        "hoa_fee": 150
    }
    
    new_property = client.properties.create_property(property_data)
    print(f"Created {new_property['property_type']} at {new_property['address']}")
    ```

=== ":material-shield-check: Validation & Errors"

    ```python
    # The API provides clear validation errors
    try:
        property = client.properties.create_property({
            "title": "Test Property",
            "client_type": "InvalidType"  # ❌ Will fail with clear message
        })
    except ValidationError as e:
        print(f"Validation error: {e}")
        # Output: Invalid client_type: InvalidType. Must be one of: buyer, seller, dual
    
    # Pre-validate data before creation
    data = {"title": "Test", "client_type": "Buyer"}
    is_valid, errors = client.validate_property_data(data)
    if is_valid:
        property = client.properties.create_property(data)
    else:
        print(f"Validation errors: {errors}")
    ```

---

### **retrieve_property()**

Get detailed information about a specific property by its ID.

```python
def retrieve_property(
    self, 
    property_id: int
) -> Dict[str, Any]
```

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `property_id` | `int` | Yes | Unique identifier of the property to retrieve |

**Returns:**

| Type | Description |
|------|-------------|
| `Dict[str, Any]` | Complete property data dictionary |

=== ":material-magnify: Basic Retrieval"

    ```python
    # Get a specific property
    property_data = client.properties.retrieve_property(123)
    
    print(f"Property: {property_data['address']}")
    print(f"Status: {property_data.get('status', 'Unknown')}")
    print(f"Price: ${property_data.get('listing_price', 0):,}")
    ```

=== ":material-information: Detailed Display"

    ```python
    # Display comprehensive property information
    property_data = client.properties.retrieve_property(123)
    
    print("=== Property Details ===")
    print(f"ID: {property_data['id']}")
    print(f"Address: {property_data.get('address', 'Not specified')}")
    print(f"City: {property_data.get('city', 'Not specified')}")
    print(f"State: {property_data.get('state', 'Not specified')}")
    print(f"Type: {property_data.get('property_type', 'Not specified')}")
    print(f"Bedrooms: {property_data.get('bedrooms', 'Not specified')}")
    print(f"Bathrooms: {property_data.get('bathrooms', 'Not specified')}")
    print(f"Square Feet: {property_data.get('square_feet', 'Not specified')}")
    print(f"Status: {property_data.get('status', 'Unknown')}")
    
    if property_data.get('listing_price'):
        print(f"Price: ${property_data['listing_price']:,}")
    ```

=== ":material-shield-check: Error Handling"

    ```python
    from open_to_close.exceptions import NotFoundError
    
    def safe_get_property(property_id):
        try:
            property_data = client.properties.retrieve_property(property_id)
            return property_data
        except NotFoundError:
            print(f"Property {property_id} not found")
            return None
        except Exception as e:
            print(f"Error retrieving property {property_id}: {e}")
            return None
    
    # Usage
    property_data = safe_get_property(123)
    if property_data:
        print(f"Found property: {property_data['address']}")
    ```

---

### **update_property()**

Update an existing property with new or modified data.

```python
def update_property(
    self, 
    property_id: int, 
    property_data: Dict[str, Any]
) -> Dict[str, Any]
```

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `property_id` | `int` | Yes | Unique identifier of the property to update |
| `property_data` | `Dict[str, Any]` | Yes | Dictionary containing fields to update |

**Returns:**

| Type | Description |
|------|-------------|
| `Dict[str, Any]` | Updated property data |

=== ":material-pencil: Basic Updates"

    ```python
    # Update property status
    updated_property = client.properties.update_property(123, {
        "status": "Under Contract"
    })
    
    # Update pricing
    updated_property = client.properties.update_property(123, {
        "listing_price": 375000,
        "price_reduction": True
    })
    
    print(f"Updated property {updated_property['id']}")
    ```

=== ":material-home-edit: Status Changes"

    ```python
    # Mark property as sold
    def mark_property_sold(property_id, sale_price, closing_date):
        return client.properties.update_property(property_id, {
            "status": "Sold",
            "sale_price": sale_price,
            "closing_date": closing_date,
            "days_on_market": calculate_days_on_market(property_id)
        })
    
    # Mark as contingent
    def mark_property_contingent(property_id, offer_price):
        return client.properties.update_property(property_id, {
            "status": "Contingent",
            "offer_price": offer_price,
            "contingent_date": datetime.now().isoformat()
        })
    
    # Usage
    sold_property = mark_property_sold(123, 365000, "2024-02-15")
    ```

=== ":material-update: Bulk Updates"

    ```python
    # Update multiple fields at once
    comprehensive_update = client.properties.update_property(123, {
        "status": "Active",
        "listing_price": 425000,
        "description": "Price reduced! Beautiful home with updates.",
        "marketing_remarks": "New price reflects motivated seller",
        "virtual_tour_url": "https://tour.example.com/property123",
        "photos_updated": True,
        "last_modified": datetime.now().isoformat()
    })
    ```

---

### **delete_property()**

Delete a property from the system. Use with caution as this action may be irreversible.

```python
def delete_property(
    self, 
    property_id: int
) -> Dict[str, Any]
```

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `property_id` | `int` | Yes | Unique identifier of the property to delete |

**Returns:**

| Type | Description |
|------|-------------|
| `Dict[str, Any]` | Deletion confirmation response |

!!! warning "Permanent Action"
    ⚠️ Property deletion may be permanent and could affect related records. Consider updating the status to "Inactive" instead of deleting when possible.

=== ":material-delete: Basic Deletion"

    ```python
    # Delete a property
    result = client.properties.delete_property(123)
    print("Property deleted successfully")
    ```

=== ":material-shield-alert: Safe Deletion"

    ```python
    def safe_delete_property(property_id, confirm=False):
        """Safely delete a property with confirmation."""
        if not confirm:
            print("This will permanently delete the property.")
            print("Call with confirm=True to proceed.")
            return None
            
        try:
            # Check if property has related records
            contacts = client.property_contacts.list_property_contacts(property_id)
            tasks = client.property_tasks.list_property_tasks(property_id)
            
            if contacts or tasks:
                print(f"Warning: Property has {len(contacts)} contacts and {len(tasks)} tasks")
                print("Consider cleaning up related data first.")
                
            result = client.properties.delete_property(property_id)
            print(f"Property {property_id} deleted successfully")
            return result
            
        except Exception as e:
            print(f"Error deleting property {property_id}: {e}")
            return None
    
    # Usage
    safe_delete_property(123, confirm=True)
    ```

=== ":material-archive: Alternative: Archive"

    ```python
    # Instead of deleting, mark as archived
    def archive_property(property_id):
        """Archive a property instead of deleting it."""
        return client.properties.update_property(property_id, {
            "status": "Archived",
            "archived_date": datetime.now().isoformat(),
            "active": False
        })
    
    # Usage
    archived_property = archive_property(123)
    print(f"Property {archived_property['id']} archived")
    ```

---

## 🏗️ Common Property Workflows

### **Property Listing Workflow**

```python
def create_new_listing(address, city, state, zip_code, listing_data):
    """Complete workflow for creating a new property listing."""
    
    # Step 1: Create the property
    property_data = {
        "address": address,
        "city": city,
        "state": state,
        "zip_code": zip_code,
        "status": "Coming Soon",
        **listing_data
    }
    
    new_property = client.properties.create_property(property_data)
    property_id = new_property['id']
    
    # Step 2: Add initial tasks
    client.property_tasks.create_property_task(property_id, {
        "title": "Professional Photography",
        "due_date": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
        "priority": "High"
    })
    
    # Step 3: Add initial note
    client.property_notes.create_property_note(property_id, {
        "content": f"New listing created for {address}. Ready for marketing preparation.",
        "note_type": "Listing"
    })
    
    return new_property

# Usage
new_listing = create_new_listing(
    "123 Dream Street",
    "Beverly Hills", 
    "CA",
    "90210",
    {
        "property_type": "Single Family Home",
        "bedrooms": 4,
        "bathrooms": 3,
        "square_feet": 2500,
        "listing_price": 1250000
    }
)
```

### **Property Status Management**

```python
class PropertyStatusManager:
    """Helper class for managing property status transitions."""
    
    def __init__(self, client):
        self.client = client
    
    def activate_listing(self, property_id):
        """Activate a property listing."""
        return self.client.properties.update_property(property_id, {
            "status": "Active",
            "list_date": datetime.now().isoformat(),
            "days_on_market": 0
        })
    
    def mark_under_contract(self, property_id, offer_price):
        """Mark property as under contract."""
        property_data = self.client.properties.retrieve_property(property_id)
        days_on_market = self._calculate_days_on_market(property_data.get('list_date'))
        
        return self.client.properties.update_property(property_id, {
            "status": "Under Contract",
            "offer_price": offer_price,
            "contract_date": datetime.now().isoformat(),
            "days_on_market": days_on_market
        })
    
    def mark_sold(self, property_id, sale_price, closing_date):
        """Mark property as sold."""
        property_data = self.client.properties.retrieve_property(property_id)
        days_on_market = self._calculate_days_on_market(property_data.get('list_date'))
        
        return self.client.properties.update_property(property_id, {
            "status": "Sold",
            "sale_price": sale_price,
            "closing_date": closing_date,
            "days_on_market": days_on_market
        })
    
    def _calculate_days_on_market(self, list_date):
        """Calculate days on market from list date."""
        if not list_date:
            return None
        # Implementation would calculate actual days
        return 30  # Placeholder

# Usage
status_manager = PropertyStatusManager(client)
status_manager.activate_listing(123)
status_manager.mark_under_contract(123, 425000)
```

---

## 🆘 Error Handling

All property methods can raise these exceptions:

!!! warning "Common Exceptions"
    - **`AuthenticationError`**: Invalid or missing API key
    - **`ValidationError`**: Invalid property data or parameters
    - **`NotFoundError`**: Property not found (retrieve, update, delete)
    - **`OpenToCloseAPIError`**: General API error

```python
from open_to_close.exceptions import (
    NotFoundError, 
    ValidationError, 
    AuthenticationError
)

def robust_property_operations(property_id):
    """Example of comprehensive error handling."""
    try:
        # Attempt property operations
        property_data = client.properties.retrieve_property(property_id)
        
        updated_property = client.properties.update_property(property_id, {
            "status": "Active"
        })
        
        return updated_property
        
    except NotFoundError:
        print(f"Property {property_id} does not exist")
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

**Property Sub-Resources:**
- **Property Contacts** - Associate people with properties *(Documentation coming soon)*
- **Property Documents** - Manage property files *(Documentation coming soon)*
- **Property Emails** - Track communications *(Documentation coming soon)*
- **Property Notes** - Add annotations *(Documentation coming soon)*
- **Property Tasks** - Manage workflows *(Documentation coming soon)*

**Related APIs:**
- **Contacts API** - Manage people and relationships *(Documentation coming soon)*
- **Agents API** - Agent assignment and management *(Documentation coming soon)*

---

*Properties form the core of the Open To Close platform. Master these operations to build powerful real estate applications.* 