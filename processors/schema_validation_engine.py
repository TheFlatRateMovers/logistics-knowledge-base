"""
Schema Validation Engine
Logistics Event & Graph Protocol v1.0

Repository Path:

/processors/schema_validation_engine.py

Purpose:

Runtime validation layer for:

- Events
- Entities
- Ontologies
- Workflows
- Graph Nodes
- Graph Edges

Ensures all operational data
conforms to repository protocol.

"""

import json
import os

from jsonschema import validate
from jsonschema import ValidationError


class SchemaValidationEngine:

    def __init__(

        self,

        schema_directory="."

    ):

        self.schema_directory = (

            schema_directory

        )

    def load_schema(

        self,

        schema_path

    ):

        with open(

            schema_path,

            "r",

            encoding="utf-8"

        ) as file:

            return json.load(file)

    def validate_document(

        self,

        document,

        schema

    ):

        try:

            validate(

                instance=document,

                schema=schema

            )

            return {

                "valid": True,

                "errors": []
            }

        except ValidationError as e:

            return {

                "valid": False,

                "errors": [

                    str(e)

                ]
            }

    def validate_file(

        self,

        document_path,

        schema_path

    ):

        with open(

            document_path,

            "r",

            encoding="utf-8"

        ) as file:

            document = json.load(file)

        schema = self.load_schema(

            schema_path

        )

        return self.validate_document(

            document,

            schema
        )

    def validate_repository(

        self,

        validation_targets

    ):

        results = []

        for target in validation_targets:

            result = self.validate_file(

                target["document"],

                target["schema"]

            )

            results.append({

                "document":

                target["document"],

                "result":

                result
            })

        return results


class ValidationReportGenerator:

    @staticmethod

    def generate_report(results):

        report = {

            "total_documents":

            len(results),

            "valid_documents":

            0,

            "invalid_documents":

            0,

            "errors": []
        }

        for result in results:

            if result["result"]["valid"]:

                report["valid_documents"] += 1

            else:

                report["invalid_documents"] += 1

                report["errors"].append(

                    result

                )

        return report


if __name__ == "__main__":

    print(

        "Schema Validation Engine Loaded"

    )
