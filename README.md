# MetaMer
[![Build Status](https://travis-ci.org/mshakya/metamer.svg?branch=master)](https://travis-ci.org/mshakya/metamer)
[![codecov](https://codecov.io/gh/mshakya/metamer/branch/master/graph/badge.svg)](https://codecov.io/gh/mshakya/metamer)

MetaMer is a workflow to cluster shotgun sequencing samples based on shared k-mers. 

# INSTALLATION
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



# LICENSE



