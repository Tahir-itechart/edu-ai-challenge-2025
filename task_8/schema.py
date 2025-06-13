import re
from typing import Any, Callable, Dict, Generic, List, Optional, Tuple, TypeVar


class ValidationError(Exception):
    """Custom exception for validation errors."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


# Type alias for validation rules: (validation_function, error_message)
Rule = Tuple[Callable[[Any], bool], str]

# Generic type variable for type-safe validators
T = TypeVar("T")


class Validator(Generic[T]):
    """
    Base class for all validators.

    Provides the core logic for chaining validation rules and executing them.
    This class implements the foundation for a fluent validation API.

    Usage example:
    --------------
    # This class is not meant to be used directly.
    # Instead, use one of the subclasses like StringValidator, NumberValidator, etc.
    """

    def __init__(self, type_check: Callable[[Any], bool], default_type_error: str):
        """
        Initialize the validator with a type check function and default error message.
        
        Args:
            type_check: Function that returns True if the value is of the correct type
            default_type_error: Error message to show when type check fails
        """
        # Store all validation rules as (function, error_message) tuples
        self._rules: List[Rule] = [(type_check, default_type_error)]
        # Track whether this validator accepts None values
        self._is_optional = False

    def optional(self) -> "Validator[Optional[T]]":
        """
        Marks the value as optional. If the value is None, no validation will be performed.
        This allows for nullable fields in object schemas.

        Returns:
        --------
            Validator: The current validator instance for chaining.
        """
        self._is_optional = True
        return self

    def with_message(self, message: str) -> "Validator[T]":
        """
        Sets a custom error message for the last added validation rule.
        This allows for more user-friendly error messages.

        Args:
        -----
            message (str): The custom error message.

        Returns:
        --------
            Validator: The current validator instance for chaining.
        """
        # Replace the error message of the most recently added rule
        if self._rules:
            validator, _ = self._rules[-1]
            self._rules[-1] = (validator, message)
        return self

    def validate(self, value: Any):
        """
        Validates the given value against all the registered rules.
        Executes each validation rule in order and raises ValidationError on first failure.

        Args:
        -----
            value (Any): The value to validate.

        Raises:
        -------
            ValidationError: If the value fails any of the validation rules.
        """
        # Skip validation if value is None and validator is optional
        if self._is_optional and value is None:
            return

        # Execute each validation rule in sequence
        for rule, message in self._rules:
            if not rule(value):
                raise ValidationError(message)


class ArrayValidator(Validator[List[T]]):
    """
    Validator for list values.
    Validates that the value is a list and that each item passes the item validator.
    
    Usage example:
    --------------
    >>> validator = Schema.array(Schema.string().min_length(3))
    >>> validator.validate(["apple", "banana"])  # Passes
    >>> validator.validate(["ok"])  # Fails
    """

    def __init__(self, item_validator: Validator[T]):
        """
        Initialize array validator with an item validator.
        
        Args:
            item_validator: Validator to apply to each item in the array
        """
        super().__init__(lambda v: isinstance(v, list), "Value must be an array")
        # Store the validator to apply to each array item
        self._item_validator = item_validator

    def validate(self, value: Any):
        """
        Validate that value is an array and each item passes item validation.
        
        Args:
            value: The value to validate
            
        Raises:
            ValidationError: If value is not an array or any item fails validation
        """
        # First check if it's a valid array type
        super().validate(value)
        
        # Skip item validation if value is None and validator is optional
        if self._is_optional and value is None:
            return

        # Validate each item in the array
        for item in value:
            try:
                self._item_validator.validate(item)
            except ValidationError as e:
                # Wrap item validation errors with context
                raise ValidationError(f"Invalid item in array: {e.message}") from e


class ObjectValidator(Validator[Dict]):
    """
    Validator for dictionary objects.
    Validates object structure, required fields, and field values.
    
    Usage example:
    --------------
    >>> address_schema = Schema.object({
    ...     "street": Schema.string(),
    ...     "city": Schema.string(),
    ... })
    >>> validator = Schema.object({
    ...     "name": Schema.string().min_length(2),
    ...     "age": Schema.number().optional(),
    ...     "address": address_schema
    ... }).allow_unknown() # Allow extra fields
    >>> data = {
    ...     "name": "John",
    ...     "age": 30,
    ...     "address": {"street": "123 Main St", "city": "Anytown"},
    ...     "extra_field": "some_value"
    ... }
    >>> validator.validate(data)  # Passes
    """

    def __init__(self, schema: Dict[str, Validator[Any]]):
        """
        Initialize object validator with a schema definition.
        
        Args:
            schema: Dictionary mapping field names to their validators
        """
        super().__init__(lambda v: isinstance(v, dict), "Value must be an object")
        # Store the schema definition for field validation
        self._schema = schema
        self._unknown_keys_allowed = False

    def allow_unknown(self) -> "ObjectValidator":
        """
        Allows the object to have keys that are not defined in the schema.
        By default, unknown keys will raise a validation error.

        Returns:
            ObjectValidator: The current validator instance for chaining.
        """
        self._unknown_keys_allowed = True
        return self

    def validate(self, value: Any):
        """
        Validate object structure and all field values.
        
        Args:
            value: The value to validate
            
        Raises:
            ValidationError: If object structure or any field is invalid
        """
        # First check if it's a valid object type
        super().validate(value)
        
        # Skip field validation if value is None and validator is optional
        if self._is_optional and value is None:
            return

        # Check for unexpected keys not defined in schema
        if not self._unknown_keys_allowed:
            for key in value:
                if key not in self._schema:
                    raise ValidationError(f"Unexpected key '{key}' in object")

        # Check for missing required keys and validate present keys
        for key, validator in self._schema.items():
            # Check if required key is missing
            if key not in value and not validator._is_optional:
                raise ValidationError(f"Missing key '{key}' in object")

            # Validate the field value if present
            if key in value:
                try:
                    validator.validate(value[key])
                except ValidationError as e:
                    # Wrap field validation errors with context
                    raise ValidationError(
                        f"Invalid value for key '{key}': {e.message}"
                    ) from e


class StringValidator(Validator[str]):
    """
    Validator for string values.
    Provides methods for common string validation rules like length and pattern matching.

    Usage example:
    --------------
    >>> validator = Schema.string().min_length(3).max_length(10)
    >>> validator.validate("hello")  # Passes
    >>> validator.validate("hi")  # Fails
    """

    def __init__(self):
        """Initialize string validator with basic type check."""
        super().__init__(lambda v: isinstance(v, str), "Value must be a string")

    def min_length(self, length: int) -> "StringValidator":
        """
        Adds a minimum length validation rule.
        Ensures the string has at least the specified number of characters.

        Args:
        -----
            length (int): The minimum allowed length for the string.

        Returns:
        --------
            StringValidator: The current validator instance for chaining.
        """
        # Add length check rule to the validation chain
        self._rules.append(
            (
                lambda v: len(v) >= length,
                f"String must be at least {length} characters long",
            )
        )
        return self

    def max_length(self, length: int) -> "StringValidator":
        """
        Adds a maximum length validation rule.
        Ensures the string has at most the specified number of characters.

        Args:
        -----
            length (int): The maximum allowed length for the string.

        Returns:
        --------
            StringValidator: The current validator instance for chaining.
        """
        # Add length check rule to the validation chain
        self._rules.append(
            (
                lambda v: len(v) <= length,
                f"String must be at most {length} characters long",
            )
        )
        return self

    def pattern(self, regex: str) -> "StringValidator":
        """
        Adds a regex pattern validation rule.
        Ensures the string matches the specified regular expression pattern.

        Args:
        -----
            regex (str): The regex pattern to match against the string.

        Returns:
        --------
            StringValidator: The current validator instance for chaining.
        """
        # Add regex pattern check rule to the validation chain
        self._rules.append(
            (
                lambda v: re.match(regex, v) is not None,
                f"String does not match pattern {regex}",
            )
        )
        return self


class NumberValidator(Validator[int | float]):
    """
    Validator for numeric values (integers or floats).
    Excludes boolean values even though bool is a subclass of int in Python.

    Usage example:
    --------------
    >>> validator = Schema.number()
    >>> validator.validate(123)  # Passes
    >>> validator.validate(123.45) # Passes
    >>> validator.validate("not a number")  # Fails
    """

    def __init__(self):
        """
        Initialize number validator with type check that excludes booleans.
        Note: In Python, bool is a subclass of int, so we explicitly exclude it.
        """
        super().__init__(
            # Check for int/float but exclude bool (which is a subclass of int)
            lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
            "Value must be a number",
        )

    def min_value(
        self, minimum: int | float, exclusive: bool = False
    ) -> "NumberValidator":
        """
        Adds a minimum value validation rule.
        Ensures the number is greater than (or equal to) the specified minimum.

        Args:
            minimum (int | float): The minimum allowed value.
            exclusive (bool): If True, the value must be strictly greater than the minimum.

        Returns:
            NumberValidator: The current validator instance for chaining.
        """
        if exclusive:
            self._rules.append(
                (
                    lambda v: v > minimum,
                    f"Number must be greater than {minimum}",
                )
            )
        else:
            self._rules.append(
                (
                    lambda v: v >= minimum,
                    f"Number must be at least {minimum}",
                )
            )
        return self

    def max_value(
        self, maximum: int | float, exclusive: bool = False
    ) -> "NumberValidator":
        """
        Adds a maximum value validation rule.
        Ensures the number is less than (or equal to) the specified maximum.

        Args:
            maximum (int | float): The maximum allowed value.
            exclusive (bool): If True, the value must be strictly less than the maximum.

        Returns:
            NumberValidator: The current validator instance for chaining.
        """
        if exclusive:
            self._rules.append(
                (
                    lambda v: v < maximum,
                    f"Number must be less than {maximum}",
                )
            )
        else:
            self._rules.append(
                (
                    lambda v: v <= maximum,
                    f"Number must be at most {maximum}",
                )
            )
        return self

    def positive(self) -> "NumberValidator":
        """
        Adds a positive number validation rule (must be > 0).
        This is a convenience method for `min_value(0, exclusive=True)`.

        Returns:
            NumberValidator: The current validator instance for chaining.
        """
        return self.min_value(0, exclusive=True).with_message("Number must be positive")

    def non_negative(self) -> "NumberValidator":
        """
        Adds a non-negative number validation rule (must be >= 0).
        This is a convenience method for `min_value(0)`.

        Returns:
            NumberValidator: The current validator instance for chaining.
        """
        return self.min_value(0).with_message("Number must be non-negative")


class BooleanValidator(Validator[bool]):
    """
    Validator for boolean values.
    Accepts only True and False values.

    Usage example:
    --------------
    >>> validator = Schema.boolean()
    >>> validator.validate(True)  # Passes
    >>> validator.validate(False) # Passes
    >>> validator.validate("not a boolean")  # Fails
    """

    def __init__(self):
        """Initialize boolean validator with basic type check."""
        super().__init__(lambda v: isinstance(v, bool), "Value must be a boolean")


class Schema:
    """
    A factory class for creating different types of validators.
    Provides a clean, fluent API for building validation schemas.

    Usage example:
    --------------
    >>> string_validator = Schema.string().min_length(3)
    >>> number_validator = Schema.number().optional()
    >>> bool_validator = Schema.boolean()
    """

    @staticmethod
    def string() -> StringValidator:
        """
        Creates a new StringValidator for validating string values.
        
        Returns:
            StringValidator: A new string validator instance
        """
        return StringValidator()

    @staticmethod
    def number() -> NumberValidator:
        """
        Creates a new NumberValidator for validating numeric values.
        
        Returns:
            NumberValidator: A new number validator instance
        """
        return NumberValidator()

    @staticmethod
    def boolean() -> BooleanValidator:
        """
        Creates a new BooleanValidator for validating boolean values.
        
        Returns:
            BooleanValidator: A new boolean validator instance
        """
        return BooleanValidator()

    @staticmethod
    def array(item_validator: Validator[T]) -> ArrayValidator[T]:
        """
        Creates a new ArrayValidator for validating list values.
        
        Args:
            item_validator: Validator to apply to each item in the array
            
        Returns:
            ArrayValidator: A new array validator instance
        """
        return ArrayValidator(item_validator)

    @staticmethod
    def object(schema: Dict[str, Validator[Any]]) -> ObjectValidator:
        """
        Creates a new ObjectValidator for validating dictionary objects.
        
        Args:
            schema: Dictionary mapping field names to their validators
            
        Returns:
            ObjectValidator: A new object validator instance
        """
        return ObjectValidator(schema) 