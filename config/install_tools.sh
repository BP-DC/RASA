#!/bin/bash

# Install qiime2
conda update conda
conda install wget

wget https://data.qiime2.org/distro/core/qiime2-2022.8-py38-linux-conda.yml

# Create an environment for qiime2
conda env create -n qiime2-2022.8 --file qiime2-2022.8-py38-linux-conda.yml

rm qiime2-2022.8-py38-linux-conda.yml

# Enter the qiime2 environment 
conda activate qiime2-2022.8

# Check qiime2 whether work normally
qiime2 --help

# Exit the newly created qiime2 environment
conda deactivate

# Install Python packages
conda install xlrd

echo "======================================================================="

# Create an environment for downstream analysis
conda create -n downstream

# Enter the Downstream environment
conda activate downstream

# Install R packages
conda install r-base==4.2.2
conda install r-ggplot2
conda install r-ade4
conda install r-dplyr
conda install r-showtext
conda install r-stringr
conda install r-cluster
conda install r-clusterSim
conda install r-do

# Install Python packages
conda install pandas

# Exit the newly created downstream environment
conda deactivate

