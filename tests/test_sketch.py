#!/usr/bin/env python

"""Tests for `meta mash` package."""

import pytest
import os
import sys
import luigi
import shutil
from luigi.interface import build
from pathlib import Path
dir_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.abspath(os.path.join(dir_path, '..'))
bin_path = os.path.join(lib_path, 'bin')
sys.path.append(lib_path)
os.environ["PATH"] += os.pathsep + bin_path
from metamash import sketch
from plumbum.cmd import cp


def test_CreateReadSketches():
    """
    Test if this first luigi class works

    test for creating sketches

    """

    build([sketch.AllSketches(data_folder="tests/data/fqs",
                              kmer=31, threads=2, sketch=100,
                              seed=2500, min_copy=2, out_dir="tests/sk_test",
                              mash_tool="mash")],
                          local_scheduler=True, workers=1)
    file_exist = os.path.exists("tests/sk_test/SRR059451_.msh")
    shutil.rmtree("tests/sk_test")
    assert file_exist is True
