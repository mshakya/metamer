# MetaMer
[![Build Status](https://travis-ci.org/mshakya/metamer.svg?branch=master)](https://travis-ci.org/mshakya/metamer)
[![codecov](https://codecov.io/gh/mshakya/metamer/branch/master/graph/badge.svg)](https://codecov.io/gh/mshakya/metamer)

MetaMer is a workflow to cluster shotgun sequencing samples based on shared k-mers. 


# 0.0.0 DEPENDENCIES
```
PYTHON VERSION >= 3.6
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
conda create -n metamer_env
conda install --yes -c bioconda mash=2.1.1 -n metamer_env
conda install --yes -c bioconda faqcs -n metamer_env
source activate metamer_env
```

Then clone the `metamer` repository.

```
git clone https://github.com/mshakya/metamer.git

```

Then change directory to `metamer` and install.

```
cd metamer
python setup.py install
```

If the installation is succesful, you should be able to type `metamer -h` and get a help message on how to use the tool.

```
metamer -h
```

# 1.0 HOW TO RUN METAMER?

metamer requires a `luigi` config file. An example config file can be found [here](https://raw.githubusercontent.com/mshakya/metamer/master/luigi.cfg). 
Make a copy of `luigi.cfg` and edit it with information pertinent to your analysis.

After having a well annotated config file, metamer can be run by simply typing

```
/path/to/bin/metamer -c /path/to/luigi.cfg
```

## 1.1.0 A STEP BY STEP GUIDE FOR RUNNING METAMER

### 1.1.1 Setup the config file.

Set what tool to use for generating MinHash distance in `mash_tool`. Right now, `metamer` only have one option and that is to use `mash`. Also, set the path to output folder in `out_dir`. All the outputs and intermediate files will be written in this folder.

```
[DEFAULT]

mash_tool = mash
# directory where all files are copied and kept
out_dir = tests/test_run
fq_folder = tests/data/fqs

```

These are the parameters specific to `luigi`.

```

[core]
log_level:DEBUG
# default-scheduler-port:8080
scheduler_url:http://localhost:8082/

```

Following parameters are running for Quality control using FaQCs.


```
[RunAllQC]
# of CPUs to run the script 
num_cpus = 2
#  Trimmed read should have to be at least this minimum length
faqc_min_L = 50
# Trimmed read has greater than or equal to this number of continuous base "N" will be discarded.
n_cutoff = 10

```

Following parameters are specific for mash

```

[AllSketches]
fq_folder = tests/data/fqs
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

Fo
```
[Alldist]
# folder that has sketch files
data_folder = tests/test_run
# of threads to trigger
threads = 2

```


An example config file that can be directly used is included in the repo.




metamer takes raw read paired fastq files as input. Paired reads must have names with suffixes *R1.fastq and *R2.fastq indicating the forward and reverse pairs. fastqs can also be compressed and files can have suffixes like *R1.fastq.gz. An example folder can be found in 'tests/data/fqs' folder of this repository.

# 1.2 OUTPUT

metamer outputs `clusters.txt` in the output folder. Its a csv file, that has name of the cluster in first column and sample names that belong to the cluster.

metamer also outputs a distance matrix of mash distances (`mash_dist.txt`) in coordinate form and square form (`dist.txt`).

# LICENSE
