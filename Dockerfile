# This is the Dockefile to build PiReT (mshakya/PiReT)
# Base Docker Image
FROM continuumio/miniconda3

# Maintainer
MAINTAINER Migun Shakya, migun@lanl.gov

# Update the system
RUN apt-get -y update
RUN apt-get -y install build-essential git-all wget
RUN apt-get clean

# install all piret dependencies
RUN conda install -c bioconda mash=2.1.1-0
RUN conda install -c bioconda faqcs
RUN conda install -c bioconda sourmash=2.0.1-0