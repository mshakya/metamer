#!/usr/bin/env python

"""Tests for `meta mash` package."""

import pytest
import os
import sys
import luigi
import shutil
dir_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.abspath(os.path.join(dir_path, '..'))
bin_path = os.path.join(lib_path, 'bin')
sys.path.append(lib_path)
os.environ["PATH"] += os.pathsep + bin_path
from metamer import sketch, dist, faqcs

def test_CalculateDist(tmpdir):
    """
    Test if this first luigi class works

    test for creating matrix of mash distances

    """

    luigi.interface.build([faqcs.RunAllQC(in_folder="tests/data/fqs",
                                          out_folder="tests/dist_test",
                                          num_cpus=1,
                                          faqc_min_L=50,
                                          n_cutoff=4),
                          sketch.AllSketches(in_folder="tests/data/fqs",
                          kmer=31, threads=1, sketch=100,
                          seed=2500, min_copy=2, out_folder="tests/dist_test",
                          mash_tool="mash")], local_scheduler=True, workers=1)
    luigi.interface.build([dist.Alldist(threads=1,
                                       out_folder="tests/dist_test",
                                       mash_tool="mash")],
                                      local_scheduler=True, workers=1)

    file_exist = os.path.exists("tests/dist_test/mash_dist.txt")
    # shutil.rmtree("tests/dist_test")
    assert file_exist is True
