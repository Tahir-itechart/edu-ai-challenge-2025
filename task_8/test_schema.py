import unittest

from schema import (
    BooleanValidator,
    NumberValidator,
    Schema,
    StringValidator,
    ValidationError,
    ArrayValidator,
    ObjectValidator,
)


class TestStringValidator(unittest.TestCase):
    def test_valid_string(self):
        validator = Schema.string()
        self.assertIsNone(validator.validate("hello"))
        self.assertIsNone(validator.validate(""))

    def test_invalid_string(self):
        validator = Schema.string()
        with self.assertRaisesRegex(ValidationError, "Value must be a string"):
            validator.validate(123)
        with self.assertRaisesRegex(ValidationError, "Value must be a string"):
            validator.validate(True)
        with self.assertRaisesRegex(ValidationError, "Value must be a string"):
            validator.validate(None)

    def test_min_length(self):
        validator = Schema.string().min_length(5)
        self.assertIsNone(validator.validate("hello"))
        self.assertIsNone(validator.validate("world123"))
        with self.assertRaisesRegex(
            ValidationError, "String must be at least 5 characters long"
        ):
            validator.validate("four")

    def test_max_length(self):
        validator = Schema.string().max_length(5)
        self.assertIsNone(validator.validate("hello"))
        self.assertIsNone(validator.validate("four"))
        with self.assertRaisesRegex(
            ValidationError, "String must be at most 5 characters long"
        ):
            validator.validate("world123")

    def test_pattern(self):
        validator = Schema.string().pattern(r"^\d{5}$")
        self.assertIsNone(validator.validate("12345"))
        with self.assertRaisesRegex(
            ValidationError, "String does not match pattern"
        ):
            validator.validate("1234")
        with self.assertRaisesRegex(
            ValidationError, "String does not match pattern"
        ):
            validator.validate("abcde")

    def test_optional_string(self):
        validator = Schema.string().optional()
        self.assertIsNone(validator.validate(None))
        self.assertIsNone(validator.validate("hello"))

    def test_custom_message(self):
        validator = Schema.string().with_message("Custom error message")
        with self.assertRaisesRegex(ValidationError, "Custom error message"):
            validator.validate(123)

    def test_chaining(self):
        validator = (
            Schema.string()
            .min_length(3)
            .max_length(10)
            .pattern(r"^[a-zA-Z]+$")
            .with_message("Must be 3-10 letters")
        )
        self.assertIsNone(validator.validate("valid"))
        with self.assertRaisesRegex(ValidationError, "Must be 3-10 letters"):
            validator.validate("123")  # Fails pattern
        validator = Schema.string().min_length(3).with_message("Too short")
        with self.assertRaisesRegex(ValidationError, "Too short"):
            validator.validate("hi")  # Fails min_length

    def test_empty_string_edge_cases(self):
        # Test empty string with min_length
        validator = Schema.string().min_length(1)
        with self.assertRaisesRegex(ValidationError, "String must be at least 1 characters long"):
            validator.validate("")
        
        # Test empty string with max_length
        validator = Schema.string().max_length(0)
        self.assertIsNone(validator.validate(""))


class TestNumberValidator(unittest.TestCase):
    def test_valid_number(self):
        validator = Schema.number()
        self.assertIsNone(validator.validate(123))
        self.assertIsNone(validator.validate(123.45))
        self.assertIsNone(validator.validate(0))
        self.assertIsNone(validator.validate(-5))

    def test_invalid_number(self):
        validator = Schema.number()
        with self.assertRaisesRegex(ValidationError, "Value must be a number"):
            validator.validate("not a number")
        with self.assertRaisesRegex(ValidationError, "Value must be a number"):
            validator.validate(True)  # This should now work correctly
        with self.assertRaisesRegex(ValidationError, "Value must be a number"):
            validator.validate(False)  # This should now work correctly
        with self.assertRaisesRegex(ValidationError, "Value must be a number"):
            validator.validate(None)

    def test_optional_number(self):
        validator = Schema.number().optional()
        self.assertIsNone(validator.validate(None))
        self.assertIsNone(validator.validate(123))

    def test_custom_message(self):
        validator = Schema.number().with_message("Not a valid number")
        with self.assertRaisesRegex(ValidationError, "Not a valid number"):
            validator.validate("invalid")

    def test_min_value(self):
        validator = Schema.number().min_value(10)
        self.assertIsNone(validator.validate(10))
        self.assertIsNone(validator.validate(15))
        with self.assertRaisesRegex(ValidationError, "Number must be at least 10"):
            validator.validate(5)

    def test_max_value(self):
        validator = Schema.number().max_value(100)
        self.assertIsNone(validator.validate(100))
        self.assertIsNone(validator.validate(50))
        with self.assertRaisesRegex(ValidationError, "Number must be at most 100"):
            validator.validate(150)

    def test_min_value_exclusive(self):
        validator = Schema.number().min_value(10, exclusive=True)
        self.assertIsNone(validator.validate(11))
        with self.assertRaisesRegex(ValidationError, "Number must be greater than 10"):
            validator.validate(10)

    def test_max_value_exclusive(self):
        validator = Schema.number().max_value(100, exclusive=True)
        self.assertIsNone(validator.validate(99))
        with self.assertRaisesRegex(ValidationError, "Number must be less than 100"):
            validator.validate(100)

    def test_positive(self):
        validator = Schema.number().positive()
        self.assertIsNone(validator.validate(1))
        self.assertIsNone(validator.validate(0.1))
        with self.assertRaisesRegex(ValidationError, "Number must be positive"):
            validator.validate(0)
        with self.assertRaisesRegex(ValidationError, "Number must be positive"):
            validator.validate(-1)

    def test_non_negative(self):
        validator = Schema.number().non_negative()
        self.assertIsNone(validator.validate(0))
        self.assertIsNone(validator.validate(1))
        with self.assertRaisesRegex(ValidationError, "Number must be non-negative"):
            validator.validate(-1)

    def test_number_chaining(self):
        validator = Schema.number().min_value(0).max_value(100).positive()
        self.assertIsNone(validator.validate(50))
        with self.assertRaisesRegex(ValidationError, "Number must be positive"):
            validator.validate(0)  # Fails positive check


class TestBooleanValidator(unittest.TestCase):
    def test_valid_boolean(self):
        validator = Schema.boolean()
        self.assertIsNone(validator.validate(True))
        self.assertIsNone(validator.validate(False))

    def test_invalid_boolean(self):
        validator = Schema.boolean()
        with self.assertRaisesRegex(ValidationError, "Value must be a boolean"):
            validator.validate("not a boolean")
        with self.assertRaisesRegex(ValidationError, "Value must be a boolean"):
            validator.validate(123)
        with self.assertRaisesRegex(ValidationError, "Value must be a boolean"):
            validator.validate(None)
        with self.assertRaisesRegex(ValidationError, "Value must be a boolean"):
            validator.validate(1)  # Test that 1 is not considered a boolean
        with self.assertRaisesRegex(ValidationError, "Value must be a boolean"):
            validator.validate(0)  # Test that 0 is not considered a boolean

    def test_optional_boolean(self):
        validator = Schema.boolean().optional()
        self.assertIsNone(validator.validate(None))
        self.assertIsNone(validator.validate(True))

    def test_custom_message(self):
        validator = Schema.boolean().with_message("Must be a boolean")
        with self.assertRaisesRegex(ValidationError, "Must be a boolean"):
            validator.validate("invalid")


class TestArrayValidator(unittest.TestCase):
    def test_valid_array(self):
        validator = Schema.array(Schema.string())
        self.assertIsNone(validator.validate(["a", "b", "c"]))
        self.assertIsNone(validator.validate([]))  # Empty array should be valid

    def test_invalid_array_type(self):
        validator = Schema.array(Schema.string())
        with self.assertRaisesRegex(ValidationError, "Value must be an array"):
            validator.validate("not an array")
        with self.assertRaisesRegex(ValidationError, "Value must be an array"):
            validator.validate(123)

    def test_invalid_item_type(self):
        validator = Schema.array(Schema.string())
        with self.assertRaisesRegex(
            ValidationError, "Invalid item in array: Value must be a string"
        ):
            validator.validate(["a", 123, "c"])

    def test_optional_array(self):
        validator = Schema.array(Schema.string()).optional()
        self.assertIsNone(validator.validate(None))

    def test_array_of_objects(self):
        object_schema = Schema.object({"name": Schema.string()})
        validator = Schema.array(object_schema)
        self.assertIsNone(validator.validate([{"name": "John"}, {"name": "Jane"}]))
        with self.assertRaisesRegex(ValidationError, "Invalid item in array"):
            validator.validate([{"name": "John"}, {"name": 123}])

    def test_nested_arrays(self):
        validator = Schema.array(Schema.array(Schema.string()))
        self.assertIsNone(validator.validate([["a", "b"], ["c", "d"]]))
        with self.assertRaisesRegex(ValidationError, "Invalid item in array"):
            validator.validate([["a", "b"], "not an array"])

    def test_array_with_constraints(self):
        validator = Schema.array(Schema.string().min_length(3))
        self.assertIsNone(validator.validate(["hello", "world"]))
        with self.assertRaisesRegex(ValidationError, "Invalid item in array"):
            validator.validate(["hello", "hi"])


class TestObjectValidator(unittest.TestCase):
    def test_valid_object(self):
        validator = Schema.object(
            {
                "name": Schema.string(),
                "age": Schema.number(),
            }
        )
        self.assertIsNone(validator.validate({"name": "John", "age": 30}))

    def test_invalid_object_type(self):
        validator = Schema.object({})
        with self.assertRaisesRegex(ValidationError, "Value must be an object"):
            validator.validate("not an object")
        with self.assertRaisesRegex(ValidationError, "Value must be an object"):
            validator.validate([])

    def test_missing_key(self):
        validator = Schema.object({"name": Schema.string(), "age": Schema.number()})
        with self.assertRaisesRegex(ValidationError, "Missing key 'age' in object"):
            validator.validate({"name": "John"})

    def test_unexpected_key(self):
        validator = Schema.object({"name": Schema.string()})
        with self.assertRaisesRegex(ValidationError, "Unexpected key 'age' in object"):
            validator.validate({"name": "John", "age": 30})

    def test_invalid_value(self):
        validator = Schema.object({"name": Schema.string()})
        with self.assertRaisesRegex(
            ValidationError, "Invalid value for key 'name': Value must be a string"
        ):
            validator.validate({"name": 123})

    def test_optional_field(self):
        validator = Schema.object(
            {
                "name": Schema.string(),
                "age": Schema.number().optional(),
            }
        )
        self.assertIsNone(validator.validate({"name": "John"}))
        self.assertIsNone(validator.validate({"name": "John", "age": 30}))

    def test_nested_object(self):
        address_schema = Schema.object(
            {
                "street": Schema.string(),
                "city": Schema.string(),
            }
        )
        validator = Schema.object(
            {
                "name": Schema.string(),
                "address": address_schema,
            }
        )
        self.assertIsNone(
            validator.validate(
                {"name": "John", "address": {"street": "123 Main St", "city": "Anytown"}}
            )
        )
        with self.assertRaisesRegex(
            ValidationError,
            "Invalid value for key 'address': Missing key 'city' in object",
        ):
            validator.validate({"name": "John", "address": {"street": "123 Main St"}})

    def test_optional_object(self):
        validator = Schema.object({"name": Schema.string()}).optional()
        self.assertIsNone(validator.validate(None))

    def test_empty_object(self):
        validator = Schema.object({})
        self.assertIsNone(validator.validate({}))
        with self.assertRaisesRegex(ValidationError, "Unexpected key 'name' in object"):
            validator.validate({"name": "John"})

    def test_complex_nested_structure(self):
        # Test a complex nested structure
        user_schema = Schema.object({
            "id": Schema.string(),
            "profile": Schema.object({
                "name": Schema.string().min_length(2),
                "contacts": Schema.array(Schema.object({
                    "type": Schema.string(),
                    "value": Schema.string()
                }))
            }),
            "settings": Schema.object({
                "notifications": Schema.boolean(),
                "theme": Schema.string().optional()
            }).optional()
        })
        
        valid_data = {
            "id": "123",
            "profile": {
                "name": "John Doe",
                "contacts": [
                    {"type": "email", "value": "john@example.com"},
                    {"type": "phone", "value": "555-1234"}
                ]
            }
        }
        self.assertIsNone(user_schema.validate(valid_data))

    def test_allow_unknown_keys(self):
        validator = Schema.object({"name": Schema.string()}).allow_unknown()
        self.assertIsNone(validator.validate({"name": "John", "age": 30}))


class TestValidationError(unittest.TestCase):
    def test_validation_error_message(self):
        error = ValidationError("Test message")
        self.assertEqual(error.message, "Test message")
        self.assertEqual(str(error), "Test message")


if __name__ == "__main__":
    unittest.main() 