#!/usr/bin/env python3
"""
Preserve Text Values Examples (v2.6.0)

This script demonstrates the new preserve_text_values parameter for creating
properties with UI-friendly text values that display properly in Open to Close.

The preserve_text_values parameter solves the issue of numeric IDs being displayed
in the UI instead of human-readable text.
"""

from typing import Any, Dict

from open_to_close import PropertiesAPI


def demonstrate_preserve_text_values() -> None:
    """Demonstrate the preserve_text_values feature with comprehensive examples."""

    print("🆕 Open To Close - preserve_text_values Feature (v2.6.0)")
    print("=" * 65)
    print("Solving the UI display issue: Text values instead of numeric IDs")
    print()

    client = PropertiesAPI()

    # Section 1: The Problem and Solution
    print("🔍 SECTION 1: Understanding the Problem")
    print("-" * 45)

    print("\n❌ Problem: Default behavior converts text to numeric IDs")
    default_property = client.create_property(
        {
            "title": "Traditional Property Creation",
            "client_type": "buyer",  # Becomes 797212
            "status": "under contract",  # Becomes 797209
        }
    )
    print(f"   Created Property ID: {default_property['id']}")
    print("   Result: UI shows '797212' and '797209' instead of readable text")

    print("\n✅ Solution: preserve_text_values keeps human-readable text")
    ui_friendly_property = client.create_property(
        {
            "title": "UI-Friendly Property Creation",
            "client_type": "Buyer",  # Stays as "Buyer"
            "status": "Under Contract",  # Stays as "Under Contract"
        },
        preserve_text_values=True,
    )
    print(f"   Created Property ID: {ui_friendly_property['id']}")
    print("   Result: UI shows 'Buyer' and 'Under Contract' (readable!)")

    # Section 2: Title Case Requirements
    print("\n\n📝 SECTION 2: Title Case Requirements for UI Recognition")
    print("-" * 58)

    # Create buyer property example
    print("\n1. Buyer Properties:")
    buyer_data = {
        "title": "Beautiful Single Family Home",
        "client_type": "Buyer",
        "status": "Under Contract",
        "purchase_amount": 450000,
    }
    print(f"   Title Case Values: {buyer_data['client_type']}, {buyer_data['status']}")
    buyer_property = client.create_property(buyer_data, preserve_text_values=True)
    print(f"   ✅ Created Property ID: {buyer_property['id']}")
    print("   🎯 UI will recognize and preselect these values correctly")

    # Create seller property example
    print("\n2. Seller Properties:")
    seller_data = {
        "title": "Luxury Downtown Condo",
        "client_type": "Seller",
        "status": "Listing- Active",
        "purchase_amount": 625000,
    }
    print(
        f"   Title Case Values: {seller_data['client_type']}, {seller_data['status']}"
    )
    seller_property = client.create_property(seller_data, preserve_text_values=True)
    print(f"   ✅ Created Property ID: {seller_property['id']}")
    print("   🎯 UI will recognize and preselect these values correctly")

    # Create dual agency example
    print("\n3. Dual Agency:")
    dual_data = {
        "title": "Investment Property Opportunity",
        "client_type": "Dual",
        "status": "Closed",
        "purchase_amount": 375000,
    }
    print(f"   Title Case Values: {dual_data['client_type']}, {dual_data['status']}")
    dual_property = client.create_property(dual_data, preserve_text_values=True)
    print(f"   ✅ Created Property ID: {dual_property['id']}")
    print("   🎯 UI will recognize and preselect these values correctly")

    # Section 3: Common Title Case Values Reference
    print("\n\n📚 SECTION 3: Common Title Case Values Reference")
    print("-" * 52)

    print("\n✅ Client Types (Exact case required):")
    client_types = ["Buyer", "Seller", "Dual"]
    for client_type in client_types:
        print(f"   • '{client_type}'")

    print("\n✅ Common Status Values (Exact case required):")
    status_values = [
        "Under Contract",
        "Listing- Active",
        "Closed",
        "Contract Terminated",
        "Listing - Pre-MLS",
    ]
    for status in status_values:
        print(f"   • '{status}'")

    print("\n✅ Property Types (Exact case required):")
    property_types = [
        "Single Family Residential",
        "Condo",
        "Townhouse",
        "Multi-Family Dwelling",
        "Vacant Land",
    ]
    for prop_type in property_types:
        print(f"   • '{prop_type}'")

    # Section 4: Real-World Integration Example
    print("\n\n🏗️ SECTION 4: Real-World Integration Example")
    print("-" * 48)

    print("\nIntegrating with external systems (CRM, MLS, etc.):")

    # Simulate external data with proper formatting
    external_property_data = {
        "address": "123 Oak Street",
        "city": "Springfield",
        "state": "IL",
        "client_relationship": "buyer",  # From external system (lowercase)
        "current_status": "under contract",  # From external system (lowercase)
        "price": 425000,
    }

    print(f"External data: {external_property_data}")

    # Transform for Open to Close with proper title case
    otc_data = {
        "title": f"{external_property_data['address']}, {external_property_data['city']}, {external_property_data['state']}",
        "client_type": str(
            external_property_data["client_relationship"]
        ).title(),  # Convert to "Buyer"
        "status": "Under Contract",  # Map to proper Open to Close status
        "purchase_amount": external_property_data["price"],
        "property_address": external_property_data["address"],
        "property_city": external_property_data["city"],
        "property_state": external_property_data["state"],
    }

    integration_property = client.create_property(otc_data, preserve_text_values=True)

    print(f"\n✅ Integration Property ID: {integration_property['id']}")
    print("🎯 Properly formatted for UI recognition!")

    # Section 5: Testing UI Recognition
    print("\n\n🧪 SECTION 5: Testing UI Recognition")
    print("-" * 41)

    test_property = client.create_property(
        {
            "title": "UI Recognition Test Property",
            "client_type": "Buyer",
            "status": "Under Contract",
        },
        preserve_text_values=True,
    )

    print(f"\n🧪 Test Property Created: ID {test_property['id']}")
    print("\n📋 Manual UI Test Steps:")
    print("1. Open this property in the Open to Close web interface")
    print("2. Check the client type dropdown - should show 'Buyer' selected")
    print("3. Check the status dropdown - should show 'Under Contract' selected")
    print("4. If dropdowns show correct selections → ✅ Success!")
    print("5. If dropdowns show wrong/empty selections → ❌ Check title case")

    # Section 6: Summary and Best Practices
    print("\n\n📖 SECTION 6: Summary and Best Practices")
    print("-" * 46)

    print("\n🎯 When to use preserve_text_values=True:")
    print("   • When UI display and recognition matters")
    print("   • For properties that will be viewed/edited in Open to Close UI")
    print("   • When integrating with external systems")
    print("   • For better user experience and data consistency")

    print("\n🎯 When to use default behavior (preserve_text_values=False):")
    print("   • API-only integrations without UI interaction")
    print("   • Backwards compatibility with existing code")
    print("   • When you prefer numeric IDs for your workflow")

    print("\n💡 Best Practices:")
    print("   • Always use proper title case with preserve_text_values=True")
    print("   • Test UI recognition after creating properties")
    print("   • Document the title case requirements for your team")
    print("   • Consider creating helper functions for consistent formatting")

    print("\n✨ Helper Function Example:")
    print(
        """
    def create_ui_friendly_property(title, client_type, status, **kwargs):
        \"\"\"Create property with proper title case for UI recognition.\"\"\"
        # Ensure proper title case
        formatted_data = {
            'title': title,
            'client_type': client_type.title() if client_type.lower() in ['buyer', 'seller', 'dual'] else client_type,
            'status': format_status_for_ui(status),  # Custom status formatter
            **kwargs
        }
        return client.properties.create_property(formatted_data, preserve_text_values=True)
    """
    )

    print(f"\n🎉 preserve_text_values demonstration complete!")
    print(f"📚 See docs/api/properties.md for detailed documentation")


def format_status_for_ui(status: str) -> str:
    """Helper function to format status values for UI recognition."""
    status_mapping = {
        "under contract": "Under Contract",
        "active": "Listing- Active",
        "closed": "Closed",
        "pre-mls": "Listing - Pre-MLS",
        "terminated": "Contract Terminated",
    }
    return status_mapping.get(status.lower(), status)


if __name__ == "__main__":
    demonstrate_preserve_text_values()
