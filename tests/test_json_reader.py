#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

"""
Unit Test for HTAN JSON Reader.
"""
from hsim import json_reader
from hsim import cli


def test_load():
    template_list = []
    template_list.append(["bts:ScRNA-seqLevel1", cli.ASSAY_TYPE])

    fname = os.path.join(os.path.dirname(__file__), "test_data/sim.json")
    reader = json_reader.HtanJsonReader(fname, template_list)
    json_doc = reader.get_doc()

    assert reader.get_num_atlases() == 1
    assert (
        reader.get_attribute_index("ScRNA-seqLevel1", "bts:HTANParentBiospecimenID")
        == 3
    )

    assert len(reader.get_error_list()) == 0


def test_broken_links():
    template_list = []
    template_list.append(["bts:ScRNA-seqLevel1", cli.ASSAY_TYPE])

    fname = os.path.join(os.path.dirname(__file__), "test_data/sim_broken_links.json")
    reader = json_reader.HtanJsonReader(fname, template_list)
    assert len(reader.get_error_list()) == 1
    assert (
        reader.get_error_list()[0]
        == "Within ScRNA-seqLevel1, we have bts:HTANParentBiospecimenID:HTA0_0_10000, "
        "but this ID does not exist within the Biospecimen list."
    )
