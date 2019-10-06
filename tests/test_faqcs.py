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
from metamer import faqcs


def test_faqcs():
    """
    Test if faqc produces a file
    """
    if os.path.exists("tests/qc_results") is False:
        os.makedirs("tests/qc_results")
    luigi.interface.build([faqcs.RunAllQC(fq_folder="tests/data/fqs",
                                          out_dir="tests/qc_results",
                                          num_cpus=1,
                                          faqc_min_L=50,
                                          n_cutoff=4)],
                          local_scheduler=True, workers=1)
    file_exist = os.path.exists("tests/qc_results/.qcs/SRR059451_/SRR059451_.stats.txt")
    shutil.rmtree("tests/qc_results")
    assert file_exist is True
