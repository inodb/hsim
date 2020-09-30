from pathlib import Path
import json
import random

"""
Utility Functions for Processing the HTAN JSON-D Schema
"""


class SchemaObject:
    STRING = "string"
    NUMERIC = "numeric"
    LIST = "list"

    def __init__(self, id, display_name, comment, inferred_data_type, option_list):
        self.id = id
        self.display_name = display_name
        self.comment = comment
        self.inferred_data_type = inferred_data_type
        self.option_list = option_list


def load_htan_schema():
    """Load the HTAN JSON-D Schema into Dictionary."""
    txt = Path("schema/HTAN.jsonld").read_text()
    schema = json.loads(txt)
    schema_dict = {}
    for x in schema["@graph"]:
        id = x["@id"]
        schema_dict[id] = x
    return schema_dict


def extract_object_details(schema_dict, target_id):
    """Extract Schema Details Regarding the Specified Object."""

    target = schema_dict[target_id]
    target_id = target["@id"]
    display_name = target["sms:displayName"].strip()
    comment = target["rdfs:comment"].strip()
    option_list = []
    if "schema:rangeIncludes" in target:
        value_list = target["schema:rangeIncludes"]
        for value_ref in value_list:
            ref_id = value_ref["@id"]
            value = schema_dict[ref_id]
            option_list.append(value["sms:displayName"])
    inferred_data_type = infer_data_type(option_list, comment)
    schema_object = SchemaObject(
        target_id, display_name, comment, inferred_data_type, option_list
    )
    return schema_object


def infer_data_type(option_list, comment):
    """
    Infer data type.
    This is not perfect, as we do not currently store data type
    in the JSON-D.  For now, we just look for the word 'numeric'
    or 'number' in the comment, and assume that these are of
    type numeric;  otherwise, we assume string.
    """
    inferred_data_type = SchemaObject.LIST
    if len(option_list) == 0:
        comment_lower = str(comment).lower()
        check1 = "number" in comment_lower
        check2 = "numeric" in comment_lower
        if check1 or check2:
            inferred_data_type = SchemaObject.NUMERIC
        else:
            inferred_data_type = SchemaObject.STRING
    return inferred_data_type


def extract_template(schema_dict, target_id):
    """Extract Template of all Fields."""
    template = schema_dict[target_id]
    dependency_list = template["sms:requiresDependency"]
    object_list = []
    for dependency_ref in dependency_list:
        ref_id = dependency_ref["@id"]
        if ref_id != "bts:component":
            object_details = extract_object_details(schema_dict, ref_id)
            object_list.append(object_details)
    return object_list


def generate_simulated_data(schema_object, htan_id, parent_id=None):
    """Generate Simulated Data for the Specified Template."""
    inferred_data_type = schema_object.inferred_data_type
    if inferred_data_type == SchemaObject.NUMERIC:
        return random.randint(0, 100)
    elif inferred_data_type == SchemaObject.STRING:
        # Use HTAN ID in these cases
        # print (schema_object.id)
        if schema_object.id == "bts:HTANParticipantID":
            return htan_id
        elif schema_object.id == "bts:HTANBiospecimenID":
            return htan_id
        elif schema_object.id == "bts:HTANParentBiospecimenID":
            return htan_id
        elif schema_object.id == "bts:HTANParentID":
            return parent_id
        else:
            return "lorem_ipsum_%d" % random.randint(0, 100000)
    else:
        random_index = random.randint(0, len(schema_object.option_list) - 1)
        return schema_object.option_list[random_index]


def get_front_end_schema(schema_dict, target_id):
    """Get Front-End Schema Object for the Specified Template."""
    object_list = extract_template(schema_dict, target_id)
    field_list = []
    for schema_object in object_list:
        field = {}
        field["id"] = schema_object.id
        field["display_name"] = schema_object.display_name
        field["description"] = schema_object.comment
        field_list.append(field)
    return field_list


def get_front_end_simulated_values(schema_dict, target_id, htan_id, parent_id=None):
    """Get Front-End Simulated Data for the Specified Template."""
    object_list = extract_template(schema_dict, target_id)
    value_list = []
    for schema_object in object_list:
        value_list.append(generate_simulated_data(schema_object, htan_id, parent_id))
    return value_list


def get_label(schema_dict, target_id):
    """Get Label of the Specified Template."""
    schema_object = schema_dict[target_id]
    return schema_object["rdfs:label"]
