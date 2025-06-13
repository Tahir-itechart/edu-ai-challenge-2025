# Python Validation Library

A simple and robust validation library for Python, providing a fluent API for validating primitive and complex data types.

## Features

- **Fluent API**: Chain validation rules together for clean, readable code.
- **Type-Safe**: Supports primitive types (`string`, `number`, `boolean`) and complex types (`array`, `object`).
- **Flexible**: Validate nested objects and lists, mark fields as optional, and allow unknown keys.
- **Customizable**: Add custom error messages for any validation rule.
- **No Dependencies**: Pure Python with no external packages required.

## Installation

No installation is needed. Simply copy `schema.py` into your project.

## Quick Start

Here's a quick example of how to validate a user data structure:

```python
from schema import Schema, ValidationError

# 1. Define your validation schema
user_schema = Schema.object({
    "name": Schema.string().min_length(2),
    "email": Schema.string().pattern(r"^[^\s@]+@[^\s@]+\.[^\s@]+$"),
    "age": Schema.number().min_value(18).optional(),
    "tags": Schema.array(Schema.string().min_length(2))
})

# 2. Create some data to validate
user_data = {
    "name": "John Doe",
    "email": "john@example.com",
    "tags": ["developer", "python"]
}

# 3. Validate the data
try:
    user_schema.validate(user_data)
    print("✅ Validation successful!")
except ValidationError as e:
    print(f"❌ Validation failed: {e.message}")
```

## API Overview

### Creating Validators
- `Schema.string()`: Creates a string validator.
- `Schema.number()`: Creates a number validator.
- `Schema.boolean()`: Creates a boolean validator.
- `Schema.array(item_validator)`: Creates an array validator.
- `Schema.object(schema_definition)`: Creates an object validator.

### Common Methods
- `.optional()`: Marks a field as optional (can be `None`).
- `.with_message("...")`: Sets a custom error message for the preceding rule.

### StringValidator Methods
- `.min_length(num)`: Sets a minimum string length.
- `.max_length(num)`: Sets a maximum string length.
- `.pattern(regex)`: Requires the string to match a regex pattern.

### NumberValidator Methods
- `.min_value(num, exclusive=False)`: Sets a minimum numeric value.
- `.max_value(num, exclusive=False)`: Sets a maximum numeric value.
- `.positive()`: Requires the number to be > 0.
- `.non_negative()`: Requires the number to be >= 0.

### ObjectValidator Methods
- `.allow_unknown()`: Allows the object to contain keys not defined in the schema.

## Complete Example

This example demonstrates nesting, optional fields, custom messages, and allowing unknown keys.

```python
from schema import Schema, ValidationError

# Define a schema for an address
address_schema = Schema.object({
    "street": Schema.string(),
    "city": Schema.string(),
    "postal_code": Schema.string().pattern(r"^\d{5}$").with_message("Postal code must be 5 digits")
})

# Define a schema for a user profile
# Allow extra fields in the root object
user_schema = Schema.object({
    "id": Schema.string(),
    "name": Schema.string().min_length(2),
    "age": Schema.number().positive().optional(),
    "is_active": Schema.boolean(),
    "address": address_schema.optional(),
    "tags": Schema.array(Schema.string())
}).allow_unknown()

# Data to validate (contains an extra field 'last_login')
user_data = {
    "id": "user-123",
    "name": "Jane Doe",

    # 'age' is optional and missing, which is valid
    "is_active": True,
    "address": {
        "street": "123 Main St",
        "city": "Anytown",
        "postal_code": "12345"
    },
    "tags": ["admin", "editor"],
    "last_login": "2024-01-01T12:00:00Z" # This extra field is allowed
}

# --- Validation ---
try:
    user_schema.validate(user_data)
    print("✅ Complex user data is valid!")
except ValidationError as e:
    print(f"❌ Validation failed: {e.message}")

# Example of invalid data
invalid_data = {
    "id": "user-456",
    "name": "J", # Too short
    "is_active": True,
    "address": {"street": "456 Oak Ave", "city": "Otherville", "postal_code": "abc"}, # Invalid postal code
    "tags": ["user", ""] # Contains empty tag
}

try:
    user_schema.validate(invalid_data)
except ValidationError as e:
    print(f"\n❌ Validation failed as expected: {e.message}")
    # Expected output: Invalid value for key 'name': String must be at least 2 characters long
```

## Running Tests

To run the comprehensive test suite, navigate to the `task_8` directory and use the following command:

```bash
python3 -m unittest test_schema.py -v
```

This will execute all 42 tests, which cover 100% of the core library code.

## Running the Example Script

The `example.py` script provides a live demonstration of the library's features.

```bash
python3 example.py
``` 