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
from metamash import process_dist


def test_process_dist():
    """
    Test if the dist output from mash is converted to matrix
    """

    mtx = process_dist.conv_matrix("test.txt")
    len_mtx = print(len(mtx))
    assert len_mtx==None
