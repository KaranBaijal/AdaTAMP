from jsonschema import validate, ValidationError

# Define your action schema
action_schema = {
    "type": "object",
    "properties": {
        "character": {"type": "string"},
        "action": {"type": "string"},
        "object": {"type": "string"},
        "id": {"type": "integer"}
    },
    "required": ["character", "action", "object", "id"],
    "additionalProperties": False
}

# Define the response schema
response_format = {
    "name": "action_sequence",  # Name is mandatory
    "schema": {
        "type": "array",
        "items": action_schema
    }
}

# Example valid data
valid_data = [
    {"character": "char0", "action": "Walk", "object": "sofa", "id": 1},
    {"character": "char0", "action": "Sit", "object": "sofa", "id": 2}
]

# Example invalid data (missing 'id' field)
invalid_data = [
    {"character": "char0", "action": "Walk", "object": "sofa"}
]

# Validate function
def validate_response(data):
    try:
        validate(instance=data, schema=response_format["schema"])
        print("Validation successful.")
    except ValidationError as e:
        print("Validation failed:", e.message)

# Run validation for both valid and invalid data
print("Validating valid data...")
validate_response(valid_data)

print("\nValidating invalid data...")
validate_response(invalid_data)