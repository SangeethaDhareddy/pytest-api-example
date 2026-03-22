pet = {
    "type": "object",
    "required": ["id", "name", "type", "status"],
    "properties": {
        "id": {
            "type": "integer"
        },
        "name": {
            "type": "string"
        },
        "type": {
            "type": "string",
            "enum": ["cat", "dog", "fish"]
        },
        "status": {
            "type": "string",
            "enum": ["available", "sold", "pending"]
        },
    },
    "additionalProperties": False
}

order = {
    "type": "object",
    "required": ["id", "pet_id"],
    "properties": {
        "id": {
            "type": "string"
        },
        "pet_id": {
            "type": "integer"
        }
    },
    "additionalProperties": False
}

message_response = {
    "type": "object",
    "required": ["message"],
    "properties": {
        "message": {
            "type": "string"
        }
    },
    "additionalProperties": False
}