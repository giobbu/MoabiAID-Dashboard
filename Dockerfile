# Python support can be specified down to the minor or micro version
# (e.g. 3.6 or 3.6.3).
# OS Support also exists for jessie & stretch (slim and full).
# See https://hub.docker.com/r/library/python/ for all supported Python
# tags from Docker Hub.

FROM continuumio/miniconda3

LABEL Name=mobiaid Version=0.0.1
EXPOSE 3000

WORKDIR /app
ADD . /app

# Set shell to bash
SHELL ["/bin/bash", "-c"]

# Install gcc
RUN apt update
RUN apt -y install gcc

# Using miniconda 
RUN conda env create -f environment.yml
RUN echo "source activate mobiaid" > ~/.bashrc
ENV PATH /opt/conda/envs/mobiaid/bin:$PATH
