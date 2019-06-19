#! /usr/bin/env python


import os
import sys
import luigi
import glob
import re
from luigi import ExternalTask
from luigi import LocalTarget
from luigi import Parameter, DictParameter, ListParameter, IntParameter
from luigi.util import inherits, requires
from itertools import chain
from plumbum.cmd import FaQCs, cat
import pandas as pd
import logging
from metamer.miscs import f2dic


class RefFile(ExternalTask):
    """An ExternalTask like this."""

    path = Parameter()

    def output(self):
        """Check."""
        return LocalTarget(os.path.abspath(self.path))


class PairedRunQC(luigi.Task):
    """Running FaQCs."""

    fastqs = ListParameter()
    sample = Parameter()
    num_cpus = IntParameter()
    qc_outdir = Parameter()
    faqc_min_L = IntParameter()
    n_cutoff = IntParameter()

    def requires(self):
        """Require pair of fastq."""
        if isinstance(self.fastqs, (list, tuple)):
            for fqs in self.fastqs:
                fqs_list = fqs.split(",")
                for f_q in fqs_list:
                    return RefFile(f_q)
        elif isinstance(self.fastqs, str):
            return RefFile(self.fastqs.split(":")[0])

    def output(self):
        """QC output."""
        out_file = self.qc_outdir + "/" + self.sample + ".stats.txt"
        return LocalTarget(out_file)

    def run(self):
        """Run the FaQC script."""
        faqc_options = ["-min_L", self.faqc_min_L,
                        "-n", self.n_cutoff,
                        "-t", self.num_cpus,
                        "-prefix", self.sample,
                        "-d", os.path.abspath(self.qc_outdir),
                        "-1", self.fastqs[0],
                        "-2", self.fastqs[1]]
        faqc_cmd = FaQCs[faqc_options]
        logger = logging.getLogger('luigi-interface')
        logger.info(faqc_cmd)
        faqc_cmd()


class RunAllQC(luigi.WrapperTask):
    """Run all QC."""

    fq_folder = Parameter()
    workdir = Parameter()
    num_cpus = IntParameter()
    faqc_min_L = IntParameter()
    n_cutoff = IntParameter()

    def requires(self):
        """A wrapper for running the QC."""
        fq_list = []
        fq_dic = {}
        regexp1 = re.compile(r'.*R[1-2]\.fastq')
        regexp2 = re.compile(r'.*R[1-2]\.fastq\.gz')
        for file in [os.path.abspath(os.path.join(self.fq_folder, x)) for x in os.listdir(self.fq_folder)]:
            if file.lower().endswith(".fastq") is True or str(file).lower().endswith(".fastq.gz") is True:
                fq_list.append(file)
        for file in fq_list:
            if any([regexp1.match(f) for f in fq_list]) is True:
                samp_name = re.search('.*_', file).group(0).split("/")[-1]
                fq_dic.setdefault(samp_name, []).append(str(file))
            elif any([regexp2.match(f) for f in fq_list]) is True:
                samp_name = re.search('.*_', file).group(0).split("/")[-1]
                fq_dic.setdefault(samp_name, []).append(str(file))
            else:
                sys.exit("fastq file name should end with R[1-2].fastq or R[1-2].fastq.gz")
        for samp, fastq in fq_dic.items():
            fastq_sort = sorted(fastq)  # sort, so that R1 comes before R2
            trim_dir = os.path.join(self.workdir, "qcs", samp)
            if os.path.isdir(trim_dir) is False:
                os.makedirs(trim_dir)
            yield PairedRunQC(fastqs=fastq_sort,  # list of fastq files
                              sample=samp,
                              num_cpus=self.num_cpus,
                              qc_outdir=trim_dir,
                              faqc_min_L=self.faqc_min_L,
                              n_cutoff=self.n_cutoff)
