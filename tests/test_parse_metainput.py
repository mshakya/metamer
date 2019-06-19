#!/usr/bin/env python

"""Tests for `meta mash` package."""

import pytest
import os
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.abspath(os.path.join(dir_path, '..'))
bin_path = os.path.join(lib_path, 'bin')
sys.path.append(lib_path)
os.environ["PATH"] += os.pathsep + bin_path
from metamer import parse_metainput


def test_parse_meta():
    """
    Test if parse_meta correctly parses the input file
    """

    m_d = parse_metainput.parse_meta("tests/data/test_input.tab")
    print(m_d)
    truth_dict = {'A': ['test_SRS104275_1.fastq', 'test_SRS104275_2.fastq'],
                  'B': ['test_SRS144382_1.fastq.gz', 'test_SRS144382_2.fastq.gz'],
                  'C': ['test_SRS149938_1.fastq', 'test_SRS149938_2.fastq']}
    assert truth_dict == m_d
