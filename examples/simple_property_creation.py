#!/usr/bin/env python3
"""
Simple Property Creation Examples

This script demonstrates how easy it is to create properties with the
simplified Open To Close API wrapper, including the new preserve_text_values
feature for UI-friendly text display.
"""

from open_to_close import PropertiesAPI


def main() -> None:
    """Demonstrate simplified property creation."""

    print("🏠 Open To Close - Simplified Property Creation (v2.6.0)")
    print("=" * 60)

    client = PropertiesAPI()

    # Example 1: Just a title (simplest possible)
    print("\n1. Creating property with just a title:")
    property1 = client.create_property("🏡 Beautiful Family Home")
    print(f"   ✅ Created Property ID: {property1['id']}")

    # Example 2: Buyer property with details
    print("\n2. Creating buyer property with details:")
    property2 = client.create_property(
        {
            "title": "🏰 Luxury Estate with Pool",
            "client_type": "Buyer",
            "status": "Active",
            "purchase_amount": 650000,
        }
    )
    print(f"   ✅ Created Property ID: {property2['id']}")

    # Example 3: Seller property
    print("\n3. Creating seller property:")
    property3 = client.create_property(
        {
            "title": "🏢 Downtown Condo for Sale",
            "client_type": "Seller",
            "status": "Pre-MLS",
            "purchase_amount": 425000,
        }
    )
    print(f"   ✅ Created Property ID: {property3['id']}")

    # Example 4: NEW - UI-Friendly Text Values (v2.6.0)
    print("\n4. 🆕 Creating property with UI-friendly text values:")
    print("   (Text values preserved for proper UI display)")
    property4 = client.create_property(
        {
            "title": "🏘️ Modern Townhouse",
            "client_type": "Buyer",  # Preserved as "Buyer" in UI
            "status": "Under Contract",  # Preserved as "Under Contract" in UI
            "purchase_amount": 475000,
        },
        preserve_text_values=True,  # 🆕 NEW parameter
    )
    print(f"   ✅ Created Property ID: {property4['id']}")
    print("   📋 UI will show 'Buyer' and 'Under Contract' (not numeric IDs)")

    # Example 5: Comparison of modes
    print("\n5. 🔍 Comparison: Default vs. UI-Friendly modes:")

    print("   Creating with default mode (converts to IDs)...")
    default_prop = client.create_property(
        {
            "title": "Comparison Test - Default Mode",
            "client_type": "buyer",
            "status": "active",
        }
    )
    print(f"   ✅ Default Property ID: {default_prop['id']}")

    print("   Creating with UI-friendly mode (preserves text)...")
    preserve_prop = client.create_property(
        {
            "title": "Comparison Test - UI Mode",
            "client_type": "Buyer",  # Title case for UI recognition
            "status": "Under Contract",  # Title case for UI recognition
        },
        preserve_text_values=True,
    )
    print(f"   ✅ UI-Friendly Property ID: {preserve_prop['id']}")

    print(f"\n🎉 Successfully created 5 properties!")
    print(
        f"📚 See docs/api/properties.md for detailed preserve_text_values documentation"
    )
    print(f"💡 Remember: Use proper title case with preserve_text_values=True")


if __name__ == "__main__":
    main()
