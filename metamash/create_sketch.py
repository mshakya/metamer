#! /usr/bin/env

from luigi import Task
from luigi import IntParameter, Parameter
from luigi import LocalTarget
from plumbum.cmd import mash, cat, mv
import sys
import os



class CreateReadSketches(Task):
    """luigi class for creating sketches of fastq reads."""
    read1 = Parameter() # name of read1
    read2 = Parameter() # name of read2
    smp = Parameter() # name of the sample
    kmer = IntParameter() # k-mer size
    threads = IntParameter() # # of threads to trigger
    sketch = IntParameter() # sketch size
    seed = IntParameter() # seed
    min_copy = IntParameter() # minimum occurence of k-mer to be included
    out_dir = Parameter() # directory where all files are copied and kept
    # prefix = Parameter() # prefix of the output sketch


    def output(self):
        """to check if smp.msh is present"""
        LocalTarget(self.smp + ".msh")

    def cat_pair(self):
        """concatenate fastq files"""
        if str(self.read1).split(".")[-1] == "gz":
            cat_file = self.smp + ".fastq.gz"
        elif str(self.read1).split(".")[-1] == "fastq":
            cat_file = self.smp + ".fastq"
        else:
            sys.exit("Your input raw reads not fastq, it needs fastq.gz or fastq extension") 
        cat_cmd = [self.read1, self.read2]
        (cat[cat_cmd] > cat_file)()
        mv[cat_file, self.out_dir]()
        return cat_file

    def sketch_pair(self):
        """create sketch"""
        if self.read2 is None:
            cat_file = self.read1
        else:
            cat_file = self.cat_pair()
        sketch_cmd = ["sketch", "-k", self.kmer, "-p",
                      self.threads, "-s", self.sketch, "-S", self.seed,
                      "-r", "-m", self.min_copy, "-o", os.path.join(self.out_dir, self.smp), 
                      os.path.join(self.out_dir, cat_file)]
        mash[sketch_cmd]()

    def run(self):
        """luigi run"""
        # self.cat_pair()
        self.sketch_pair()


