#!/usr/bin/env python3
"""
Example usage of the Python Validation Library.

This script demonstrates how to use the validation library for various data types
and complex nested structures.
"""

from schema import Schema, ValidationError


def example_basic_validators():
    """Demonstrate basic validator usage."""
    print("=== Basic Validators ===")
    
    # String validation
    print("\n1. String Validation:")
    name_validator = Schema.string().min_length(2).max_length(50)
    
    try:
        name_validator.validate("John Doe")
        print("✓ 'John Doe' is valid")
    except ValidationError as e:
        print(f"✗ Error: {e.message}")
    
    try:
        name_validator.validate("J")  # Too short
        print("✓ 'J' is valid")
    except ValidationError as e:
        print(f"✗ Error: {e.message}")
    
    # Number validation
    print("\n2. Number Validation:")
    age_validator = Schema.number().min_value(0).max_value(150)
    
    try:
        age_validator.validate(25)
        print("✓ Age 25 is valid")
    except ValidationError as e:
        print(f"✗ Error: {e.message}")
    
    try:
        age_validator.validate(-5)  # Negative age
        print("✓ Age -5 is valid")
    except ValidationError as e:
        print(f"✗ Error: {e.message}")
    
    # Boolean validation
    print("\n3. Boolean Validation:")
    active_validator = Schema.boolean()
    
    try:
        active_validator.validate(True)
        print("✓ True is valid")
    except ValidationError as e:
        print(f"✗ Error: {e.message}")
    
    try:
        active_validator.validate(1)  # Not a boolean
        print("✓ 1 is valid")
    except ValidationError as e:
        print(f"✗ Error: {e.message}")


def example_complex_validators():
    """Demonstrate complex validator usage."""
    print("\n=== Complex Validators ===")
    
    # Array validation
    print("\n1. Array Validation:")
    tags_validator = Schema.array(Schema.string().min_length(2))
    
    try:
        tags_validator.validate(["python", "validation", "library"])
        print("✓ Tags array is valid")
    except ValidationError as e:
        print(f"✗ Error: {e.message}")
    
    try:
        tags_validator.validate(["python", "a"])  # "a" is too short
        print("✓ Tags array with short tag is valid")
    except ValidationError as e:
        print(f"✗ Error: {e.message}")
    
    # Object validation
    print("\n2. Object Validation:")
    user_validator = Schema.object({
        "name": Schema.string().min_length(2),
        "email": Schema.string().pattern(r"^[^\s@]+@[^\s@]+\.[^\s@]+$"),
        "age": Schema.number().min_value(0).optional(),
        "is_active": Schema.boolean()
    })
    
    valid_user = {
        "name": "Alice Smith",
        "email": "alice@example.com",
        "age": 30,
        "is_active": True
    }
    
    try:
        user_validator.validate(valid_user)
        print("✓ User object is valid")
    except ValidationError as e:
        print(f"✗ Error: {e.message}")
    
    invalid_user = {
        "name": "Bob",
        "email": "invalid-email",  # Invalid email format
        "is_active": True
    }
    
    try:
        user_validator.validate(invalid_user)
        print("✓ Invalid user object is valid")
    except ValidationError as e:
        print(f"✗ Error: {e.message}")


def example_nested_structure():
    """Demonstrate nested structure validation."""
    print("\n=== Nested Structure Validation ===")
    
    # Define nested schema
    address_schema = Schema.object({
        "street": Schema.string().min_length(5),
        "city": Schema.string().min_length(2),
        "postal_code": Schema.string().pattern(r"^\d{5}$"),
        "country": Schema.string().min_length(2)
    })
    
    contact_schema = Schema.object({
        "type": Schema.string(),
        "value": Schema.string().min_length(3)
    })
    
    user_profile_schema = Schema.object({
        "id": Schema.string(),
        "personal_info": Schema.object({
            "first_name": Schema.string().min_length(2),
            "last_name": Schema.string().min_length(2),
            "age": Schema.number().min_value(0).max_value(150)
        }),
        "address": address_schema.optional(),
        "contacts": Schema.array(contact_schema),
        "preferences": Schema.object({
            "newsletter": Schema.boolean(),
            "theme": Schema.string().optional()
        }).optional()
    })
    
    # Valid nested data
    valid_profile = {
        "id": "user123",
        "personal_info": {
            "first_name": "John",
            "last_name": "Doe",
            "age": 28
        },
        "address": {
            "street": "123 Main Street",
            "city": "Anytown",
            "postal_code": "12345",
            "country": "US"
        },
        "contacts": [
            {"type": "email", "value": "john@example.com"},
            {"type": "phone", "value": "555-1234"}
        ],
        "preferences": {
            "newsletter": True,
            "theme": "dark"
        }
    }
    
    try:
        user_profile_schema.validate(valid_profile)
        print("✓ Complex nested profile is valid")
    except ValidationError as e:
        print(f"✗ Error: {e.message}")
    
    # Invalid nested data (missing required field)
    invalid_profile = {
        "id": "user456",
        "personal_info": {
            "first_name": "Jane",
            # Missing last_name
            "age": 25
        },
        "contacts": []
    }
    
    try:
        user_profile_schema.validate(invalid_profile)
        print("✓ Invalid nested profile is valid")
    except ValidationError as e:
        print(f"✗ Error: {e.message}")


def example_custom_messages():
    """Demonstrate custom error messages."""
    print("\n=== Custom Error Messages ===")
    
    password_validator = (
        Schema.string()
        .min_length(8)
        .with_message("Password must be at least 8 characters long")
    )
    
    try:
        password_validator.validate("short")
        print("✓ Short password is valid")
    except ValidationError as e:
        print(f"✗ Custom Error: {e.message}")
    
    email_validator = (
        Schema.string()
        .pattern(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
        .with_message("Please provide a valid email address")
    )
    
    try:
        email_validator.validate("not-an-email")
        print("✓ Invalid email is valid")
    except ValidationError as e:
        print(f"✗ Custom Error: {e.message}")


if __name__ == "__main__":
    print("Python Validation Library - Examples")
    print("=" * 50)
    
    example_basic_validators()
    example_complex_validators()
    example_nested_structure()
    example_custom_messages()
    
    print("\n" + "=" * 50)
    print("Examples completed!") 