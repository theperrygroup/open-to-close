# Migration Guide: Dynamic Field Mapping Update

## Overview

The Open to Close API wrapper has been updated to include dynamic field mapping, making it much easier to create and manage properties. This guide will help you migrate from the previous version.

## What's Changed

### Before (Hardcoded Field IDs)
The library used hardcoded field IDs which could become outdated:
```python
# Old way - hardcoded field mappings
property = client.properties.create_property({
    "contract_title": "My Property",
    "client_type": "Buyer",  # Had to match exact case
    "status": "Active"       # Limited to hardcoded options
})
```

### After (Dynamic Field Discovery)
The library now fetches field definitions directly from the API:
```python
# New way - dynamic field mappings
property = client.properties.create_property({
    "title": "My Property",      # Simpler field names supported
    "client_type": "buyer",      # Case-insensitive
    "status": "under contract"   # All API options supported
})
```

## Key Improvements

### 1. Automatic Field Discovery
- Field definitions are fetched from the API on first use
- Cached for performance
- Can be refreshed when API changes

### 2. Simplified Field Names
You can now use simplified field names:
- `title` → `contract_title`
- `client_type` → `contract_client_type`
- `status` → `contract_status`

### 3. Case-Insensitive Options
Choice field values are now case-insensitive:
- `"buyer"`, `"Buyer"`, `"BUYER"` all work
- `"under contract"`, `"Under Contract"` both work

### 4. Better Error Messages
```python
# If you use an invalid option
ValidationError: Unknown option 'invalid' for field 'contract_status'. 
Valid options: closed, contract terminated, listing - pre-mls, listing- active, under contract
```

## Migration Steps

### Step 1: Update Your Code (Optional)
Your existing code will continue to work, but you can simplify it:

```python
# Old way (still works)
property = client.properties.create_property({
    "contract_title": "Test Property",
    "contract_client_type": "Buyer",
    "contract_status": "Active"  # Note: "Active" alone is not valid
})

# New way (recommended)
property = client.properties.create_property({
    "title": "Test Property",
    "client_type": "buyer",
    "status": "listing- active"  # Use valid API options
})
```

### Step 2: Use Field Discovery
Discover available fields and their options:

```python
# List all available fields
fields = client.list_available_fields()
for field in fields[:5]:
    print(f"{field['name']} ({field['type']}): {field.get('options', 'N/A')}")

# Get detailed field mappings
mappings = client.properties.get_field_mappings()
print(mappings["contract_status"]["options"])
```

### Step 3: Validate Before Creating
Use the new validation helper:

```python
# Validate property data
property_data = {
    "title": "Test Property",
    "client_type": "buyer",
    "status": "closed"
}

is_valid, errors = client.validate_property_data(property_data)
if not is_valid:
    for error in errors:
        print(f"Error: {error}")
```

## Important Notes

### Valid Status Options
The valid contract status options from the API are:
- `"listing - pre-mls"`
- `"listing- active"` (note the space)
- `"listing - under contract"`
- `"listing - withdrawn-cancelled"`
- `"under contract"`
- `"closed"`
- `"contract terminated"`

**Note:** `"active"` by itself is not a valid option. Use `"listing- active"` instead.

### Field Caching
Field mappings are cached on first use. To refresh:
```python
# Force refresh if API fields change
client.properties.refresh_field_mappings()
```

### Backward Compatibility
All existing code continues to work:
- Original field names (`contract_title`, etc.) still work
- API format with field arrays still works
- Hardcoded field IDs still work

## New Helper Methods

### `list_available_fields()`
Returns a list of all available fields with metadata:
```python
fields = client.list_available_fields()
# Returns: [{"name": "contract_title", "id": 926565, "type": "text", "required": True}, ...]
```

### `validate_property_data()`
Validates property data before submission:
```python
is_valid, errors = client.validate_property_data(data)
# Returns: (True/False, ["error1", "error2", ...])
```

### `get_field_mappings()`
Get raw field mappings for advanced use:
```python
mappings = client.properties.get_field_mappings()
# Returns: {"field_name": {"id": 123, "type": "text", "options": {...}}, ...}
```

## Examples

See `examples/updated_api_examples.py` for comprehensive examples of the new features.

## Support

If you encounter any issues with the migration:
1. Check that your field values match valid API options
2. Use `validate_property_data()` to check your data
3. Refresh field mappings if you suspect API changes

The update is designed to be fully backward compatible, so your existing code should continue to work without changes. 