#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

"""
Unit Test for HTAN JSON Reader.
"""
from hsim import json_reader

def test_load():
    fname = os.path.join(os.path.dirname(__file__), "test_data/sim.json")
    reader = json_reader.HtanJsonReader(fname)
    json_doc = reader.get_doc()

    assert reader.get_num_atlases() == 2
    assert reader.get_attribute_index("ScRNA-seqLevel1", "bts:HTANParentBiospecimenID") == 3

    assert len(reader.get_error_list()) == 0
