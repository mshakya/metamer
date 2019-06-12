#! /usr/bin/env python


import os
import re


def f2dic(fq_folder):
    "list of fastq in a folder to dictionary"
    fq_list = []
    fq_dic = {}
    regexp1 = re.compile(r'.*R[1-2]\.fastq')
    regexp2 = re.compile(r'.*R[1-2]\.fastq\.gz')
    for file in [os.path.abspath(os.path.join(fq_folder, x)) for x in os.listdir(fq_folder)]:
        if file.lower().endswith(".fastq") is True or str(file).lower().endswith(".fastq.gz") is True:
            fq_list.append(file)
    fq_list.sort() # sort so that first element in the list is R1
    for file in fq_list:
        if any([regexp1.match(f) for f in fq_list]) is True:
            samp_name = re.search('.*_', file).group(0).split("/")[-1]
            fq_dic.setdefault(samp_name, []).append(str(file))
        elif any([regexp2.match(f) for f in fq_list]) is True:
            samp_name = re.search('.*_', file).group(0).split("/")[-1]
            fq_dic.setdefault(samp_name, []).append(str(file))
        else:
            sys.exit("fastq file name should end with R[1-2].fastq or R[1-2].fastq.gz")
    return fq_dic