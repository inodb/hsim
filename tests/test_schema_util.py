#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit Test for schema_util.
"""
from hsim import schema_util
import random

def test_load_schema():
    schema_dict = schema_util.load_htan_schema()
    assert len(schema_dict) == 4423


def test_extract_object_details_1():
    schema_dict = schema_util.load_htan_schema()
    schema_object = schema_util.extract_object_details(schema_dict, "bts:Gender")
    assert schema_object.display_name == "Gender"
    assert schema_object.comment.startswith(
        "Text designations that identify gender."
    )
    assert len(schema_object.option_list) == 5


def test_extract_object_details_2():
    schema_dict = schema_util.load_htan_schema()
    schema_object = schema_util.extract_object_details(schema_dict, "bts:Race")
    assert schema_object.display_name == "Race"
    assert schema_object.comment.startswith(
        "An arbitrary classification of a taxonomic group"
    )
    assert len(schema_object.option_list) == 9


def test_extract_template_1():
    schema_dict = schema_util.load_htan_schema()
    object_list = schema_util.extract_template(schema_dict, "bts:Demographics")
    assert len(object_list) == 12
    assert object_list[1].display_name == "HTAN Participant ID"
    assert object_list[1].inferred_data_type == "string"
    assert object_list[2].display_name == "Ethnicity"
    assert object_list[2].inferred_data_type == "list"
    assert object_list[3].display_name == "Gender"
    assert object_list[6].display_name == "Days to Birth"
    assert object_list[6].inferred_data_type == "numeric"

def test_infer_data_type():
    inferred_data_type = schema_util.infer_data_type([], "Number indicating...")
    assert inferred_data_type == schema_util.SchemaObject.NUMERIC
    inferred_data_type = schema_util.infer_data_type([], "Numeric indicator of...")
    assert inferred_data_type == schema_util.SchemaObject.NUMERIC
    inferred_data_type = schema_util.infer_data_type([], "Age of patient")
    assert inferred_data_type == schema_util.SchemaObject.STRING

def test_generate_simulated_data():
    random.seed(0)
    schema_dict = schema_util.load_htan_schema()
    schema_list = schema_util.extract_template(schema_dict, "bts:Demographics")

    patient_id = schema_util.generate_simulated_data(schema_list[1], "HTA1_0")
    ethnicity = schema_util.generate_simulated_data(schema_list[2], "HTA1_0")
    gender = schema_util.generate_simulated_data(schema_list[3], "HTA1_0")
    days_to_birth = schema_util.generate_simulated_data(schema_list[6], "HTA1_0")

    assert patient_id == "HTA1_0"
    assert ethnicity == "not reported"
    assert gender == "unspecified"
    assert days_to_birth == 5

def test_get_front_end_schema():
    schema_dict = schema_util.load_htan_schema()
    fields = schema_util.get_front_end_schema(schema_dict, "bts:Demographics", "HTA1_0")
    assert len(fields) == 12
    assert fields[1]["display_name"] == "HTAN Participant ID"
    assert fields[1]["description"].startswith("HTAN ID associated with")

def test_get_front_end_schema():
    random.seed(0)
    schema_dict = schema_util.load_htan_schema()
    values = schema_util.get_front_end_simulated_values(schema_dict, "bts:Demographics", "HTA1_0")
    assert len(values) == 12
    assert values[1] == "HTA1_0"
    assert values[2] == "not reported"
    assert values[3] == "female"