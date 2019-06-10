#! /usr/bin/env

from luigi import Task
from luigi import IntParameter, Parameter
from luigi import LocalTarget
from plumbum.cmd import mash, cat, mv
import pandas as pd


def parse_meta(in_meta):
    """parse the input tsv file and extract dictionary"""
    meta_df = pd.read_csv(in_meta, sep="\t")
    meta_dict = {k: list(v) for k, v in meta_df.groupby("Sample")["reads"]}
    return meta_dict

