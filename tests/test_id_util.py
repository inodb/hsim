"""
Unit Test for schema_util.
"""
from hsim import id_util


def test_generate_htan_patient_ids():
    id_list = id_util.generate_htan_participant_ids("HTA1", 10)
    assert id_list[0] == "HTA1_0"


def test_generate_htan_sample_ids():
    id_list = id_util.generate_sample_ids("HTA1_0", 10)
    assert id_list[0] == "HTA1_0_0"
    assert id_list[1] == "HTA1_0_1"


def test_generate_id_set():
    id_table = id_util.generate_id_set("HTA1", 2, 4)

    # Verify initial participant
    assert id_table[0][0] == "PARTICIPANT"
    assert id_table[0][1] == "HTA1_0"

    # Verify that we have a basic hierarchy
    # of participant --> sample --> sub sample
    # ['SAMPLE', 'HTA1_0_0', 'HTA1_0']
    # ['SAMPLE', 'HTA1_0_1', 'HTA1_0_0']
    assert id_table[1][0] == "SAMPLE"
    assert id_table[1][1] == "HTA1_0_0"
    assert id_table[1][2] == "HTA1_0"

    assert id_table[2][0] == "SAMPLE"
    assert id_table[2][1] == "HTA1_0_1"
    assert id_table[2][2] == "HTA1_0_0"

    participant_id_list = id_util.extract_participant_id_list(id_table)
    assert len(participant_id_list) == 2

    sample_id_list = id_util.extract_sample_id_list(id_table)
    assert len(sample_id_list) == 8

    parent_id = id_util.extract_parent_id(id_table, "HTA1_0_1")
    assert parent_id == "HTA1_0_0"
