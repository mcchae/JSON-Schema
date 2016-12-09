#!/usr/bin/env python
# coding=utf-8

import sys
from apitools.datagenerator import DataGenerator
from jsonschema import validate
from jsonschema.exceptions import ValidationError

generator = DataGenerator()

user_schema = {
    "type": "object",
    "properties": {
        "cellphone": {
            "type": "string",
            "pattern": "^[01]{3}-[0-9]{4}-[0-9]{4}$"
        },
        "age": {
            "type": "integer",
            "required": True,
            "minimum": 0,
            "maximum": 150
        },
        "name": {
            "type": "string",
            "required": True
        },
        "address": {
            "type": "string",
            "maxLength": 50
        }
    }
}

while True:
    r = generator.random_value(user_schema)
    try:
        validate(r, user_schema)
        break
    except ValidationError as ve:
        sys.stderr.write(str(ve) + "\n")
print(r)