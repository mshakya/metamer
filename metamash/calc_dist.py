#! /usr/bin/env

from luigi import Task
from luigi import IntParameter, Parameter
from luigi import LocalTarget
from plumbum.cmd import mash, cat, mv
from pathlib import Path
import sys
import os
import itertools



class CalculateDist(Task):
    """luigi class for calculating mash distance between two sketches."""
    sk_dir = Parameter() # Folder that has .msh files
    threads = IntParameter() # # of threads to trigger
    out_file = Parameter() # files are copied and kept


    def calc_dist(self):
        """create sketch"""
        skch_files = [x for x in Path(self.sk_dir).glob('**/*') if x.suffix == ".msh"]
        with open(self.out_file, 'w') as file:
            for skch in itertools.combinations(skch_files, 2):
                print(skch)
                dist_cmd = ["dist", "-p", self.threads, str(skch[0]),
                             str(skch[1])]
                dist_info = mash[dist_cmd]()
                file.write(dist_info)

    def run(self):
        """luigi run"""
        self.calc_dist()

    def output(self):
        """output"""
        LocalTarget(self.out_file)
