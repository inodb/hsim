#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from . import schema_util
from . import id_util
from pathlib import Path

"""
This is the entry point for the command-line interface (CLI) application.
"""
import click

# Change the options to below to suit the actual options for your task (or
# tasks).
@click.group()
def cli():
    """Generate Simulated HTAN Data"""
    pass


@cli.command()
def generate():
    """Generate Simulated HTAN Data"""

    # The Atlases for which we will generate simulated data
    target_atlas_list = get_atlas_list()

    # The Data Templates for which we will generate simulated data
    template_list = get_template_list()

    # Load the HTAN JSON-LD Schema
    schema_dict = schema_util.load_htan_schema()

    atlas_list = []
    for target_atlas in target_atlas_list:
        atlas_list.append(
            generate_simulated_atlas(
                target_atlas[0], target_atlas[1], schema_dict, template_list
            )
        )

    data_set = {}
    data_set["atlases"] = atlas_list

    # Generate the root schema node
    generate_schemas_node(schema_dict, template_list, data_set)

    json_dump = json.dumps(data_set, indent=4)
    print(json_dump)


def get_atlas_list():
    target_atlas_list = []
    target_atlas_list.append(["HTA1", "HTAPP Pilot Project"])
    target_atlas_list.append(["HTA2", "PCAPP Pilot Project"])
    return target_atlas_list


def get_template_list():
    template_list = []
    template_list.append(["bts:Demographics", "clinical"])
    template_list.append(["bts:Diagnosis", "clinical"])
    template_list.append(["bts:FollowUp", "clinical"])
    template_list.append(["bts:Exposure", "clinical"])
    template_list.append(["bts:FollowUp", "clinical"])
    template_list.append(["bts:Therapy", "clinical"])
    template_list.append(["bts:ScRNA-seqAssay", "assay"])
    return template_list


def generate_schemas_node(schema_dict, template_list, data_set):
    schema_list = []
    for template in template_list:
        current_schema = {}
        current_schema["data_schema"] = schema_util.get_label(schema_dict, template[0])
        current_schema["attributes"] = schema_util.get_front_end_schema(
            schema_dict, template[0]
        )
        schema_list.append(current_schema)
    data_set["schemas"] = schema_list


def generate_simulated_atlas(atlas_id, atlas_name, schema_dict, template_list):
    atlas = {}
    atlas["htan_id"] = atlas_id
    atlas["htan_name"] = atlas_name

    NUM_PARTICIPANTS = 10
    NUM_SAMPLES_PER_PARTICIPANT = 6

    id_set = id_util.generate_id_set(
        atlas_id, NUM_PARTICIPANTS, NUM_SAMPLES_PER_PARTICIPANT
    )

    for template in template_list:
        template_label = schema_util.get_label(schema_dict, template[0])
        template_type = template[1]
        if template_type == "clinical":
            atlas[template_label] = get_dummy_clinical_files(
                id_set, schema_dict, template[0], template[1]
            )
        else:
            atlas[template_label] = get_dummy_assay_files(
                id_set, schema_dict, template[0], template[1]
            )
    return atlas


def get_dummy_clinical_files(id_set, schema_dict, template_id, template_type):
    participant_id_list = id_util.extract_participant_id_list(id_set)
    record_list = []
    for participant_id in participant_id_list:
        current_record = {}
        current_record["values"] = schema_util.get_front_end_simulated_values(
            schema_dict, template_id, participant_id
        )
        record_list.append(current_record)
    data = {}
    data["data_schema"] = template_id
    data["data_link"] = "https://www.synapse.org/#!Synapse:synXXXX/tables/YYYYY"
    data["record_list"] = record_list
    return data


def get_dummy_assay_files(id_set, schema_dict, template_id, template_type):
    sample_id_list = id_util.extract_sample_id_list(id_set)
    record_list = []
    for sample_id in sample_id_list:
        current_record = {}
        current_record["values"] = schema_util.get_front_end_simulated_values(
            schema_dict, template_id, sample_id
        )
        record_list.append(current_record)
    data = {}
    data["data_schema"] = template_id
    data["data_link"] = "https://www.synapse.org/#!Synapse:synXXXX/tables/YYYYY"
    data["record_list"] = record_list
    return data