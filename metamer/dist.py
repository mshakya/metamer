#! /usr/bin/env

from luigi import IntParameter, Parameter, ListParameter, LocalTarget, Task
import luigi
from luigi.util import requires
from plumbum.cmd import mash, cat, mv
from pathlib import Path
import sys
import os
import itertools
import re
from metamer import sketch, miscs, faqcs


class CalculateDist(Task):
    """luigi class for calculating mash distance between two sketches."""
    sk1 = Parameter()
    sk2 = Parameter()
    threads = IntParameter()  # # of threads to trigger
    out_file = Parameter()  # files are copied and kept

    def requires(self):
        LocalTarget(self.sk1)

    def calc_dist(self):
        """calculate distance sketch"""
        with open(self.out_file, 'a+') as file:
            dir_name = os.path.dirname(self.sk1)
            dist_cmd = ["dist", "-p", self.threads, str(self.sk1),
                        str(self.sk2)]
            dist_info = mash[dist_cmd]()
            dist_info = dist_info.replace(dir_name, "")
            dist_info = dist_info.replace("/", "")
            dist_info = re.sub('\.fastq', '', dist_info)
            dist_info = re.sub('\.gz', '', dist_info)
            file.write(dist_info)

    def run(self):
        """luigi run"""
        self.calc_dist()

    def output(self):
        """output"""
        # return faqcs.RefFile(self.out_file)
        return LocalTarget(self.out_file)


class Alldist(luigi.WrapperTask):
    "Run all Comparisons"
    data_folder = Parameter()  # folder that has sketch files
    threads = IntParameter()  # of threads to trigger
    out_table = Parameter()  # Table file with all comparisons
    mash_tool = Parameter()  # sourmash or mash

    def requires(self):
        """A wrapper for comparing sketches."""
        sk_list = miscs.sk2list(self.data_folder)
        all_pairs = list(itertools.combinations(sk_list, 2))
        for pair in all_pairs:
            yield CalculateDist(sk1=pair[0], sk2=pair[1], threads=self.threads,
                                out_file=self.out_table)
