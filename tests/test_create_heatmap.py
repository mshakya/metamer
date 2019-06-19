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
from metamer import create_heatmap, dist


def test_create_heatmap():
    """
    Test if the dist output from mash is converted to matrix
    """

    mtx = dist.conv_matrix("test.txt")
    print(mtx)
    create_heatmap.create_heatmap(mtx, x=["A", "B"], y=["C", "D"], title="test",
    							  out_file="foo.png")

    hmap = create_sns_heatmap("test.txt")
    hmap.savefig("foo.png")

    assert os.path.exists("foo.png") is True
