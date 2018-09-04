#! /usr/bin/env

from luigi import Task
from luigi import IntParameter, Parameter
from luigi import LocalTarget
from plumbum.cmd import mash, cat, mv
import pandas as pd


def parse_meta(self):
    """parse the input tsv file and extract dictionary"""
    meta_df = pd.read_csv(self.in_meta, sep="\t")
    meta_dict = {k: list(v) for k,v in meta_df.groupby("Sample")["reads"]}
    return meta_dict

# class ParseMetaData(Task):
#     """luigi class for parsing metadata."""
#     in_meta = Parameter()





#     def run(self):
#         """luigi run"""
#         self.cat_pair()
#         self.sketch_pair()
