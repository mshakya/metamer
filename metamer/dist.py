#! /usr/bin/env

from luigi import IntParameter, Parameter, ListParameter, LocalTarget, Task
from luigi import WrapperTask
from luigi.util import requires
from plumbum.cmd import mash, cat, mv
from pathlib import Path
import sys
import os
import itertools
import re
from metamash import sketch


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
            dist_info = re.sub('\.fastq','', dist_info)
            dist_info = re.sub('\.gz','', dist_info)
            file.write(dist_info)

    def run(self):
        """luigi run"""
        self.calc_dist()

    def output(self):
        """output"""
        LocalTarget(self.out_file)


class Alldist(WrapperTask):
    data_folder = Parameter()
    threads = IntParameter()  # of threads to trigger
    out_table = Parameter()  # Table file with all comparisons
    mash_tool = Parameter()  # sourmash or mash

    def requires(self):
        """A wrapper for running sketches."""
        sk_list = sk2list(self.data_folder)
        if os.path.exists(self.out_dir) is False:
            os.mkdir(os.path.join(self.out_dir))
        all_pairs = list(itertools.combinations(sk_list, 2))
        for pair in all_pairs:
            yield CalculateDist(sk1=pair[0], sk2=pair[1], threads=self.threads,
                                out_file=self.out_table)