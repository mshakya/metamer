#! /usr/bin/env

from luigi import IntParameter, Parameter, ListParameter, LocalTarget, Task
from luigi.util import requires
from plumbum.cmd import mash, cat, mv
from pathlib import Path
import sys
import os
import itertools
import re
from metamash import create_sketch


# @requires(create_sketch.CreateReadSketches)
class CalculateDist(Task):
    """luigi class for calculating mash distance between two sketches."""
    sk1 = Parameter()
    sk2 = Parameter()
    # sk_dir = Parameter() # Folder that has .msh files
    threads = IntParameter() # # of threads to trigger
    out_file = Parameter() # files are copied and kept


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
