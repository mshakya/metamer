#! /usr/bin/env

from luigi import Task, WrapperTask
from luigi import IntParameter, Parameter, LocalTarget
from luigi.util import requires
from plumbum.cmd import mash, cat, mv
import sys
import os
import logging
from metamer.miscs import f2dic, fna2dic


class CreateReadSketches(Task):
    """luigi class for creating sketches of fastq reads."""
    kmer = IntParameter()  # k-mer size
    threads = IntParameter()  # of threads to trigger
    sketch = IntParameter()  # sketch size
    seed = IntParameter()  # seed
    min_copy = IntParameter()  # minimum occurence of k-mer to be included
    out_folder = Parameter()  # directory where all files are copied and kept
    mash_tool = Parameter()  # sourmash or mash
    read1 = Parameter()
    read2 = Parameter()
    smp = Parameter()

    def output(self):
        """to check if msh is present"""
        return LocalTarget(os.path.join(self.out_folder, ".mash",
                                        self.smp + ".msh"))

    def sketch_pair(self):
        """create sketch"""
        logger = logging.getLogger('luigi-interface')  # setup logger
        if os.path.exists(os.path.join(self.out_folder, ".mash")) is False:
            os.makedirs(os.path.join(self.out_folder, ".mash"))

        if self.mash_tool == "mash":
            sketch_cmd = ["sketch", "-k", self.kmer, "-p", self.threads,
                          "-s", self.sketch, "-S", self.seed,
                          "-r",
                          "-o", os.path.join(self.out_folder, ".mash", self.smp + ".msh"),
                          os.path.join(self.out_folder, self.read1),
                          os.path.join(self.out_folder, self.read2)]
        logger.info(mash[sketch_cmd]())
        mash[sketch_cmd]()

    def run(self):
        """luigi run"""
        # self.cat_pair()
        self.sketch_pair()


class CreateFastaSketches(Task):
    """luigi class for creating sketches of fastq reads."""
    kmer = IntParameter()  # k-mer size
    threads = IntParameter()  # of threads to trigger
    sketch = IntParameter()  # sketch size
    seed = IntParameter()  # seed
    min_copy = IntParameter()  # minimum occurence of k-mer to be included
    mash_tool = Parameter()  # sourmash or mash
    fasta = Parameter()
    smp = Parameter()
    out_folder = Parameter()

    def output(self):
        """to check if msh is present"""
        return LocalTarget(os.path.join(self.out_folder, ".mash",
                                        self.smp + ".msh"))

    def sketch_pair(self):
        """create sketch"""
        logger = logging.getLogger('luigi-interface')  # setup logger
        if os.path.exists(os.path.join(self.out_folder, ".mash")) is False:
            os.makedirs(os.path.join(self.out_folder, ".mash"))

        if self.mash_tool == "mash":
            sketch_cmd = ["sketch", "-k", self.kmer, "-p", self.threads,
                          "-s", self.sketch, "-S", self.seed,
                          "-o", os.path.join(self.out_folder, ".mash", self.smp + ".msh"),
                          self.fasta]
        logger.info(mash[sketch_cmd]())
        mash[sketch_cmd]()

    def run(self):
        """luigi run"""
        # self.cat_pair()
        self.sketch_pair()


class AllSketches(WrapperTask):
    """ perform sketches on all samples"""
    in_folder = Parameter()
    kmer = IntParameter()  # k-mer size
    threads = IntParameter()  # of threads to trigger
    sketch = IntParameter()  # sketch size
    seed = IntParameter()  # seed
    min_copy = IntParameter()  # minimum occurence of k-mer to be included
    out_folder = Parameter()  # directory where all files are copied and kept
    mash_tool = Parameter()  # sourmash or mash

    def requires(self):
        """A wrapper for running sketches."""
        fq_dic = f2dic(self.in_folder)
        fna_dic = fna2dic(self.in_folder)
        if os.path.exists(self.out_folder) is False:
            os.mkdir(os.path.join(self.out_folder))
        for samp, fastq in fq_dic.items():
            read1 = os.path.join(".qcs", samp, samp + ".1.trimmed.fastq")
            read2 = os.path.join(".qcs", samp, samp + ".2.trimmed.fastq")
            yield CreateReadSketches(smp=samp,
                                     kmer=self.kmer,
                                     threads=self.threads,
                                     sketch=self.sketch,
                                     seed=self.seed,
                                     min_copy=self.min_copy,
                                     out_folder=self.out_folder,
                                     mash_tool="mash",
                                     read1=read1,
                                     read2=read2)
        if len(fna_dic) > 0:
            print("urshula")
            print(fna_dic)
            for samp, fna in fna_dic.items():
                print("urshula")
                print(samp)
                print(fna)
                yield CreateFastaSketches(smp=samp,
                                          kmer=self.kmer,
                                          threads=self.threads,
                                          sketch=self.sketch,
                                          seed=self.seed,
                                          min_copy=self.min_copy,
                                          out_folder=self.out_folder,
                                          mash_tool="mash",
                                          fasta=fna)
