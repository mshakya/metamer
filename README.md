# MetaMer
[![Build Status](https://travis-ci.org/mshakya/metamer.svg?branch=master)](https://travis-ci.org/mshakya/metamer)
[![codecov](https://codecov.io/gh/mshakya/metamer/branch/master/graph/badge.svg)](https://codecov.io/gh/mshakya/metamer)

MetaMer is a workflow to cluster shotgun sequencing samples based on shared k-mers. 

# 0.0 INSTALLATION

```
PYTHON VERSION >= 3.6
```
## 0.1 DEPENDENCIES

### 0.1.2 PYTHON DEPENDENCIES
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

### 0.1.3 THIRD PARTY DEPENDENCIES
```
mash >= 2.1.1
faqcs
```
MetaMer can be installed by following instructions below:

First install conda, if you dont have it installed. See instructions on how to install miniconda [here](https://docs.conda.io/en/latest/miniconda.html). Install miniconda that supports Python 3.

After the installation, first create a conda environment and then install third party tools.

Third party tool dependencies can be installed using `conda`.

```
conda create -n metamer_env
conda install --yes -c bioconda mash=2.1.1 -n metamer_env
conda install --yes -c bioconda faqcs -n metamer_env

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

metamer requires a `luigi` config file. An example comfig file can be found in this repo. Make a copy of `luigi.cfg` and edit it with information pertinent to your run.

After having a well annotated config file, metamer can be run by simply typing

```
/path/to/bin/metamer -c /path/to/luigi.cfg
```

# 1.1 INPUT
    All inputs are specified in a config file. An example file named `luigi.cfg` can be found included in the repo.

    metamer takes raw read paired fastq files as input. Paired reads must have names with suffixes *R1.fastq and *R2.fastq indicating the forward and reverse pairs. fastqs can also be compressed and files can have suffixes like *R1.fastq.gz. An example folder can be found in 'tests/data/fqs' folder of this repository.

# 1.2 OUTPUT

metamer outputs `clusters.txt` in the output folder. Its a csv file, that has name of the cluster in first column and sample names that belong to the cluster.

metamer also outputs a distance matrix of mash distances (`mash_dist.txt`) in coordinate form and square form (`dist.txt`).

# LICENSE
