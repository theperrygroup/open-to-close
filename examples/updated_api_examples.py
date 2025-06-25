"""
Examples for using the Open to Close API with dynamic field mapping.

These examples demonstrate the key features of the updated API wrapper:
- Automatic field ID discovery
- Simple human-readable field names
- Field validation with helpful errors
- Helper methods for field discovery
"""

from open_to_close import OpenToCloseAPI

# Initialize the client
client = OpenToCloseAPI()  # Uses OPEN_TO_CLOSE_API_KEY env variable

# Example 1: Create a property with simple field names
# The API automatically translates these to field IDs
property1 = client.properties.create_property(
    {
        "title": "Beautiful Family Home",
        "client_type": "buyer",  # Automatically mapped to ID 797212
        "status": "under contract",  # Automatically mapped to ID 797207
        "purchase_amount": 450000,
    }
)
print(f"Created property ID: {property1['id']}")

# Example 2: Use the original field names (also supported)
property2 = client.properties.create_property(
    {
        "contract_title": "Luxury Downtown Condo",
        "contract_client_type": "seller",  # Mapped to ID 797213
        "contract_status": "listing- active",  # Mapped to ID 797206
        "mls_number": "MLS123456",
        "year_built": "2020",
        "property_type": "Condo",  # Mapped to ID 797222
    }
)
print(f"Created property ID: {property2['id']}")

# Example 3: Create from just a title (simplest form)
property3 = client.properties.create_property("Quick Sale Property")
print(f"Created property ID: {property3['id']}")

# Example 4: Discover available fields
print("\nAvailable property fields:")
fields = client.list_available_fields()

# Show required fields
print("\nRequired fields:")
for field in fields:
    if field["required"]:
        print(f"  {field['name']} ({field['type']})")
        if field.get("options"):
            print(f"    Options: {', '.join(field['options'])}")

# Show some optional fields
print("\nSample optional fields:")
count = 0
for field in fields:
    if not field["required"] and count < 5:
        print(f"  {field['name']} ({field['type']})")
        count += 1

# Example 5: Validate before creating
property_data = {"title": "Test Property", "client_type": "dual", "status": "closed"}

is_valid, errors = client.validate_property_data(property_data)
if is_valid:
    property5 = client.properties.create_property(property_data)
    print(f"Created validated property ID: {property5['id']}")
else:
    print("Validation errors:")
    for error in errors:
        print(f"  - {error}")

# Example 6: Handle validation errors gracefully
try:
    # This will fail validation
    invalid_property = client.properties.create_property(
        {
            "title": "Invalid Property",
            "client_type": "InvalidType",  # This will cause an error
        }
    )
except Exception as e:
    print(f"Expected error: {e}")

# Example 7: Get field mappings for advanced use
mappings = client.properties.get_field_mappings()

# Show how contract_status options are mapped
if "contract_status" in mappings:
    status_mapping = mappings["contract_status"]
    print(f"\nContract status field (ID: {status_mapping['id']}):")
    print("Option mappings:")
    for option_name, option_id in status_mapping.get("options", {}).items():
        if "-" not in option_name or option_name.startswith("listing"):
            print(f"  '{option_name}' -> ID {option_id}")

# Example 8: Create with address information
property_with_address = client.properties.create_property(
    {
        "title": "Complete Property Example",
        "client_type": "buyer",
        "status": "under contract",
        "purchase_amount": 550000,
        "property_address": "123 Main Street",  # If these fields exist
        "property_city": "Salt Lake City",
        "property_state": "UT",
        "property_zip": "84101",
        "closing_date": "2024-03-15",
        "mls_number": "MLS789012",
    }
)
print(f"Created complete property ID: {property_with_address['id']}")

# Example 9: Refresh field mappings (useful if API fields change)
# This forces a fresh fetch from the API
refreshed_mappings = client.properties.refresh_field_mappings()
print(f"\nRefreshed {len(refreshed_mappings)} field mappings")

# Example 10: For backward compatibility, the API format still works
api_format_property = client.properties.create_property(
    {
        "team_member_id": 26392,
        "time_zone_id": 1,
        "fields": [
            {"id": 926565, "value": "API Format Property"},
            {"id": 926553, "value": 797212},  # buyer
            {"id": 926552, "value": 797206},  # listing-active
        ],
    }
)
print(f"Created with API format, ID: {api_format_property['id']}")
