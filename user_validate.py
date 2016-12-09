#!/usr/bin/env python
# coding=utf-8

import sys
from jsonschema import validate
from jsonschema.exceptions import ValidationError

schema = {
    "type": "object",
    "properties": {
        "cellphone": {
            "type": "string",
            "pattern": "^[01]{3}-[0-9]{4}-[0-9]{4}$"
        },
        "age": {
            "type": "integer",
            "minimum": 0,
            "maximum": 150
        },
        "name": {
            "type": "string"
        },
        "address": {
            "type": "string",
            "maxLength": 50
        }
    },
    "required": [
        "age",
        "name"
    ]
}

data = [
    {
        "name": "홍길동",
        "cellphone": "010-1345-7764",
        "address": "​이상국 행복리 234",
        "age": 33
    },
    {
        "name": "홍길동",
        "age": 33
    },
    {
        "name": "홍길동",
        "address": "​이상국 행복리 234",
    },
    {
        "name": "홍길동",
        "cellphone": "012-1345-7764",
        "age": 33
    }
]

print("Validating the input data using jsonschema:")
for idx, item in enumerate(data):
    try:
        validate(item, schema)
        sys.stdout.write("Record #{}: OK\n".format(idx))
    except ValidationError as ve:
        sys.stderr.write("Record #{}: ERROR\n".format(idx))
        sys.stderr.write(str(ve) + "\n")
