#!/bin/bash

# **************************Data input*****************************
# Import paired-end sequencing data and remove primers

cd $4

qiime tools import \
	--type 'SampleData[PairedEndSequencesWithQuality]' \
	--input-path $1 \
	--output-path paired-demux.qza \
	--input-format PairedEndFastqManifestPhred33V2

qiime cutadapt trim-paired \
	--i-demultiplexed-sequences paired-demux.qza \
	--p-front-f $2 \
	--p-front-r $3 \
	--o-trimmed-sequences paired-end-demux.qza \
	--verbose \
	&> primer_trimming.log

qiime demux summarize \
	--i-data paired-end-demux.qza \
	--o-visualization demux.qzv
