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
from metamer import sketch, dist

def test_CalculateDist(tmpdir):
    """
    Test if this first luigi class works

    test for creating matrix of mash distances

    """

    luigi.interface.build([sketch.AllSketches(data_folder="tests/data/fqs",
                           kmer=31, threads=2, sketch=100,
                           seed=2500, min_copy=2, out_dir="tests/sk_test",
                           mash_tool="mash")],
                          local_scheduler=True, workers=1)
    luigi.interface.build([dist.Alldist(data_folder="tests/sk_test", threads=2,
                                        out_table="tests/test_table.txt", mash_tool="mash")],
                          local_scheduler=True, workers=1)

    file_basenames = [os.path.basename(x) for x in tmpdir.listdir()] 
    print(file_basenames)
    file_exist = os.path.exists("tests/test_table.txt")
    shutil.rmtree("tests/sk_test")
    assert file_exist is True
