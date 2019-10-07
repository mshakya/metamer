# metamer
[![Build Status](https://travis-ci.org/mshakya/metamer.svg?branch=master)](https://travis-ci.org/mshakya/metamer)
[![codecov](https://codecov.io/gh/mshakya/metamer/branch/master/graph/badge.svg)](https://codecov.io/gh/mshakya/metamer)

`metamer`` is a workflow to cluster sequencing samples (paired raw fastq reads or assemblies) based on shared k-mers. It currently uses mash to compute distance between samples. It is useful for binning metagenomes or any sequencing samples into cluster based on their similarity.


# 0.0.0 DEPENDENCIES
```
PYTHON VERSION >= 3.6.6
```

### 0.1.1 PYTHON DEPENDENCIES
```
numpy >= 1.15.1
scipy >= 1.3.0,
luigi >= 2.7.5,
plumbum >= 1.6.6,
pandas >= 0.23.4,
pathlib >= 1.0.1,
matplotlib >= 3.1.0,
Seaborn >= 0.9.0
```

### 0.1.2 THIRD PARTY DEPENDENCIES
```
mash >= 2.1.1
faqcs
```

# 1.0.0 INSTALLATION
MetaMer can be installed by following instructions below:


First install conda, if you dont have it installed. See instructions on how to install miniconda [here](https://docs.conda.io/en/latest/miniconda.html). Install miniconda that supports Python 3.


## 1.0.1 Create a conda environment and install dependencies.

After the installation, first create a conda environment and then install third party tools.

Third party tool dependencies can be installed using `conda`.

```
conda config --add channels defaults
conda config --add channels bioconda
conda config --add channels conda-forge
conda create --yes -n metamer_env python=3.6.6
conda create -n metamer_env
conda install --yes -c bioconda mash=2.1.1 -n metamer_env
conda install --yes -c bioconda faqcs -n metamer_env
source activate metamer_env
```

Then clone the `metamer` repository.

```
git clone https://github.com/LANL-Bioinformatics/metamer
```

Then change directory to `metamer` and install.

```
cd metamer
python setup.py install
```

If the installation was succesful, you should be able to type `metamer -h` and get a help message on how to use the tool.

```
metamer -h
```

And, you can run a quick test using

```
cd metamer
metamer -c luigi.cfg
```


# 2.0.0 HOW TO RUN METAMER?

`metamer` 


`metamer` requires a `luigi` config file. An example config file can be found [here](https://raw.githubusercontent.com/mshakya/metamer/master/luigi.cfg).
Make a copy of `luigi.cfg` and edit it with information pertinent to your analysis.

After having a well annotated config file, metamer can be run by simply typing

```
/path/to/bin/metamer -c /path/to/luigi.cfg
```

## 1.1.0 A STEP BY STEP GUIDE FOR RUNNING METAMER

### 1.1.1 Setup the config file.

Set what tool to use for generating MinHash distance in `mash_tool`. Right now, `metamer` only have one option and that is to use `mash`. Also, set the path to output folder in `out_folder`. All the outputs and intermediate files will be written in this folder. 


```
[DEFAULT]
mash_tool = mash
# directory where all files are copied and kept
out_folder = tests/test_run
# folder with input data (paired raw reads and fasta genomes)
in_folder = tests/data/fqs

```

These are the parameters specific to `luigi`. Change log level to `DEBUG` if reporting an error.


```
[core]
log_level:ERROR
scheduler_url:http://localhost:8082/
```

Following parameters are running for Quality control using FaQCs. Please update the parameters if needed.


```
[RunAllQC]
# of CPUs to run the script 
num_cpus = 2
#  Trimmed read should have to be at least this minimum length
faqc_min_L = 50
# Trimmed read has greater than or equal to this number of continuous base "N" will be discarded.
n_cutoff = 10
```

Following parameters are specific for `mash`. Parameters for kmer and sketches could have the most effect.

```
[AllSketches]
in_folder = tests/data/fqs
# k-mer size
kmer = 21
# threads
threads = 2
# sketch size
sketch = 1000
seed = 439
# minimum occurence of k-mer to be included
min_copy = 1
```

Only need to set threads parameter for generating distance.

```
[Alldist]
# of threads to trigger
threads = 2
```

Set the parameter for threshold to call clusters. Maximum distance betwen two points to be part of a same cluster.

```
[ClusterSamples]
# maximum cophenetic distance between two points in a cluster
threshold = 0.3
```

For this step by step guide, we will use a small dataset that is packaged with this repo, so all the config file parameters are already set in the `luigi.cfg` file that is included in the repo.

### 1.1.2 Copy all input datasets to a folder

`metamer` can process paired fastq raw reads and assembled fasta files from one folder. Paried raw reads must have names that end in `*_R1.fastq` and `*_R2.fastq` to identify them as part of one sample. These raw reads can also be compressed in gz format, and have names that end in `*R1.fastq.gz` and `*R2.fastq.gz`. Assembled fasta files must have `*.fna` or if compressed `*.fna.gz`. Do not forget to specify the full path to the input folder in the config file.

The provided test datasets in `tests/data/fqs` is as follows:

```

-rw-r--r--@ 1 usr st 1.2M Sep  3 14:36 GCA_000009205.2_ASM920v2_genomic.fna.gz
-rw-r--r--  1 usr st 4.0M Sep  3 14:36 GCA_000085225.1_ASM8522v1_genomic.fna
-rw-r--r--  1 usr st 1.1M Sep  3 14:36 GCA_003482325.1_ASM348232v1_genomic.fna.gz
-rw-r--r--  1 usr st 7.9K Jun 10 16:33 SRR059450_h100_R1.fastq.gz
-rw-r--r--  1 usr st 8.1K Jun 10 16:33 SRR059450_h100_R2.fastq.gz
-rw-r--r--  1 usr st 7.4K Jun 10 16:33 SRR059451_R1.fastq.gz
-rw-r--r--  1 usr st 7.4K Jun 10 16:33 SRR059451_R2.fastq.gz
-rw-r--r--  1 usr st 1.9K Jun 10 16:33 SRR059453_R1.fastq.gz
-rw-r--r--  1 usr st 1.8K Jun 10 16:33 SRR059453_R2.fastq.gz
-rw-r--r--  1 usr st 9.7K Jun 10 16:33 SRR059454_R1.fastq.gz
-rw-r--r--  1 usr st 9.7K Jun 10 16:33 SRR059454_R2.fastq.gz
-rw-r--r--  1 usr st 9.6K Jun 10 16:33 SRR059455_R1.fastq.gz
-rw-r--r--  1 usr st 9.5K Jun 10 16:33 SRR059455_R2.fastq.gz
-rw-r--r--  1 usr st 9.2K Jun 10 16:33 SRR059456_R1.fastq.gz
-rw-r--r--  1 usr st 9.3K Jun 10 16:33 SRR059456_R2.fastq.gz
-rw-r--r--  1 usr st 9.0K Jun 10 16:33 SRR059457_R1.fastq.gz
-rw-r--r--  1 usr st 9.1K Jun 10 16:33 SRR059457_R2.fastq.gz
-rw-r--r--  1 usr st 7.3K Jun 10 16:33 SRR059458_R1.fastq.gz
-rw-r--r--  1 usr st 7.3K Jun 10 16:33 SRR059458_R2.fastq.gz
-rw-r--r--  1 usr st 7.6K Jun 10 16:33 SRR059459_R1.fastq.gz
-rw-r--r--  1 usr st 7.6K Jun 10 16:33 SRR059459_R2.fastq.gz

```

### 1.1.2 Run metamer

`metamer` should be in the path if the user followed the instuction for installations outlined in the above sections. If thats the case, one can run `metamer` directly:

```

metamer -c luigi.cfg

```

For this tutorial, `cd` into the github repo

```
cd metamer
```
and run

```
metamer luigi.cfg
```

All the parameters in `luigi.cfg` has already been set for this run. Also,if metamer is not in the path, users can directly call the `metamer` from the `bin` folder using:

```
bin/metamer luigi.cfg
```


### 1.1.3 OUTPUTS


`metamer` outputs multiple files. The most important one being `clusters.txt`. It's a csv file that has name of the cluster in first column and sample names that belong to the cluster. An example `clusters.txt` file.


```

8,['SRR059455_.1.trimmed']
9,['SRR059456_.1.trimmed']
1,['GCA_000009205.2_ASM920v2_genomic.fna']
10,['SRR059451_.1.trimmed']
11,['SRR059457_.1.trimmed']
2,['GCA_000085225.1_ASM8522v1_genomic.fna']
12,['SRR059459_.1.trimmed']
3,['SRR059453_.1.trimmed']
4,['SRR059450_h100_.1.trimmed']
5,['GCA_003482325.1_ASM348232v1_genomic.fna']
6,['SRR059458_.1.trimmed']
7,['SRR059454_.1.trimmed']


```

metamer also outputs a distance matrix of mash distances (`mash_dist.txt`) in coordinate form and square form (`dist.txt`).

