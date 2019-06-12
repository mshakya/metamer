#!/usr/bin/env python

"""Tests for `meta mash` package."""

import pytest
import os
import sys
import luigi
from pathlib import Path
dir_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.abspath(os.path.join(dir_path, '..'))
bin_path = os.path.join(lib_path, 'bin')
sys.path.append(lib_path)
os.environ["PATH"] += os.pathsep + bin_path
from metamash import sketch
from plumbum.cmd import cp


def test_CreateReadSketches(tmpdir):
    """
    Test if this first luigi class works

    test for creating sketches

    """
    d_foler = "tests/data/"
    cp_read1 = [read1, tmpdir + "/read1.fastq"]
    cp_read2 = [read2, tmpdir + "/read2.fastq"]
    cp[cp_read1]()
    cp[cp_read2]()
    cp_read3 = [read3, tmpdir + "/read3.fastq"]
    cp_read4 = [read4, tmpdir + "/read4.fastq"]
    cp[cp_read3]()
    cp[cp_read4]()

    luigi.interface.build([create_sketch.CreateReadSketches(data_folder="tests/data/fqs",
                                                            kmer=31,
                                                            threads=2,
                                                            sketch=100,
                                                            seed=2500,
                                                            min_copy=2,
                                                            out_dir=Path(tmpdir))],
                          local_scheduler=True, workers=1)
    # luigi.interface.build([create_sketch.CreateReadSketches(read1=os.path.join(tmpdir, "read3.fastq"),
    #                                                         read2=os.path.join(tmpdir, "read4.fastq"),
    #                                                         smp="test2",
    #                                                         kmer=31,
    #                                                         threads=2,
    #                                                         sketch=1000,
    #                                                         seed=2500,
    #                                                         min_copy=2,
    #                                                         out_dir=Path(tmpdir))],
    #                       local_scheduler=True, workers=1)
    # luigi.interface.build([create_sketch.CreateReadSketches(read1=os.path.join(tmpdir, "read3.fastq"),
    #                                                         read2=None,
    #                                                         smp="test3",
    #                                                         kmer=31,
    #                                                         threads=2,
    #                                                         sketch=1000,
    #                                                         seed=2500,
    #                                                         min_copy=2,
    #                                                         out_dir=Path(tmpdir))],
                        #   local_scheduler=True, workers=1)
    file_basenames = [os.path.basename(x) for x in tmpdir.listdir()] 
    assert 'test1_k31_ss100_sd2500.msh' in file_basenames
    assert 'test2_k31_ss1000_sd2500.msh' in file_basenames
    assert 'test3_k31_ss1000_sd2500.msh' in file_basenames
