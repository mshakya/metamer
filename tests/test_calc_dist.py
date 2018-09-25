#!/usr/bin/env python

"""Tests for `meta mash` package."""

import pytest
import os
import sys
import luigi
dir_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.abspath(os.path.join(dir_path, '..'))
bin_path = os.path.join(lib_path, 'bin')
sys.path.append(lib_path)
os.environ["PATH"] += os.pathsep + bin_path
from metamash import calc_dist
from plumbum.cmd import cp


def test_CalculateDist(tmpdir):
    """
    Test if this first luigi class works

    test for creating matrix of mash distances

    """

    luigi.interface.build([calc_dist.CalculateDist(sk1="tests/data/test_SRS104275_1.fastq.msh",
                                                   sk2="tests/data/test_SRS144382_1.fastq.gz.msh",
                                                   threads=2,
                                                   out_file=os.path.join(tmpdir, "test_matrix.txt"))],
                          local_scheduler=True, workers=1)

    file_basenames = [os.path.basename(x) for x in tmpdir.listdir()] 
    assert 'test_matrix.txt' in file_basenames
