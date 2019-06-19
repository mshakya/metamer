# This is the Dockefile to build metamer (mshakya/metamer)
# Base Docker Image
FROM continuumio/miniconda3

# Update the system
RUN apt-get -y update
RUN apt-get -y install build-essential git-all wget
RUN apt-get clean

# install all metamer dependencies
RUN conda install -c bioconda mash
RUN conda install -c bioconda faqcs
