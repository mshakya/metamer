#! /usr/bin/env

from luigi import Task, WrapperTask
from luigi import IntParameter, Parameter, LocalTarget
from luigi.util import requires
from plumbum.cmd import mash, cat, mv
import sys
import os
import logging
from metamer.miscs import f2dic


class CreateReadSketches(Task):
    """luigi class for creating sketches of fastq reads."""
    kmer = IntParameter()  # k-mer size
    threads = IntParameter()  # of threads to trigger
    sketch = IntParameter()  # sketch size
    seed = IntParameter()  # seed
    min_copy = IntParameter()  # minimum occurence of k-mer to be included
    out_dir = Parameter()  # directory where all files are copied and kept
    mash_tool = Parameter()  # sourmash or mash
    read1 = Parameter()
    read2 = Parameter()
    smp = Parameter()

    def output(self):
        """to check if msh is present"""
        return LocalTarget(os.path.join(self.out_dir, self.smp + ".msh"))

    def sketch_pair(self):
        """create sketch"""
        logger = logging.getLogger('luigi-interface')  # setup logger
        if self.mash_tool == "mash":
            sketch_cmd = ["sketch", "-k", self.kmer, "-p", self.threads,
                          "-s", self.sketch, "-S", self.seed,
                          "-r",
                          "-o", os.path.join(self.out_dir, self.smp + ".msh"),
                          os.path.join(self.out_dir, self.read1),
                          os.path.join(self.out_dir, self.read2)]
        logger.info(mash[sketch_cmd]())
        mash[sketch_cmd]()

    def run(self):
        """luigi run"""
        # self.cat_pair()
        self.sketch_pair()


class AllSketches(WrapperTask):
    """ perform sketches on all samples"""
    data_folder = Parameter()
    kmer = IntParameter()  # k-mer size
    threads = IntParameter()  # of threads to trigger
    sketch = IntParameter()  # sketch size
    seed = IntParameter()  # seed
    min_copy = IntParameter()  # minimum occurence of k-mer to be included
    out_dir = Parameter()  # directory where all files are copied and kept
    mash_tool = Parameter()  # sourmash or mash

    def requires(self):
        """A wrapper for running sketches."""
        fq_dic = f2dic(self.data_folder)
        if os.path.exists(self.out_dir) is False:
            os.mkdir(os.path.join(self.out_dir))
        for samp, fastq in fq_dic.items():
            yield CreateReadSketches(smp=samp,
                                     kmer=self.kmer,
                                     threads=self.threads,
                                     sketch=self.sketch,
                                     seed=self.seed,
                                     min_copy=self.min_copy,
                                     out_dir=self.out_dir,
                                     mash_tool="mash",
                                     read1=fastq[0],
                                     read2=fastq[1])