#!/bin/bash

#conda activate qiime2-2022.8
cd ${10}

# ***********************Generate ASV and taxonomy annotation***********************
time qiime dada2 denoise-paired \
	--i-demultiplexed-seqs $1 \
	--p-trunc-len-f $2 \
	--p-trunc-len-r $3 \
	--p-trim-left-f $4 \
	--p-trim-left-r $5 \
	--p-min-overlap $6 \
	--o-table table.qza \
	--p-n-threads $7 \
	--o-representative-sequences rep-seqs.qza \
	--o-denoising-stats denoising-stats.qza \
	--verbose

# Classify each read
time qiime feature-classifier classify-sklearn \
	--i-reads rep-seqs.qza \
	--i-classifier $8 \
	--o-classification taxonomy.qza

# *************************Remove chloroplasts and mitochondria*************************	
f=""

if [ $9 -eq 1 ];  
then  
qiime taxa filter-table \
	--i-table table.qza \
	--i-taxonomy taxonomy.qza \
	 --p-exclude mitochondria,chloroplast \
	 --o-filtered-table table-filter.qza

qiime feature-table filter-seqs \
	--i-data rep-seqs.qza \
	--i-table table-filter.qza \
	--o-filtered-data rep-seqs-filter.qza

qiime feature-classifier classify-sklearn \
	--i-classifier $8  \
	--i-reads rep-seqs-filter.qza \
	--o-classification taxonomy-filter.qza \
	--p-n-jobs $7 \
	--verbose

f="-filter"
fi

for i in 1 2 3 4 5 6 7
do 
qiime taxa collapse \
	--i-table table$f.qza \
	--i-taxonomy taxonomy$f.qza \
	--p-level $i \
	--o-collapsed-table table$f-l$i.qza
	
qiime feature-table relative-frequency \
	--i-table table$f-l$i.qza \
	--o-relative-frequency-table relative-table$f-l$i.qza
	
qiime tools export \
	--input-path relative-table$f-l$i.qza \
	--output-path relative-table$f
biom convert --to-tsv -i relative-table$f/feature-table.biom -o relative-table$f-l$i.tsv

rm -rf relative-table$f
rm -rf relative-table$f-l$i.qza
done

# *********************************Diversity analysis***********************************
# Calculate the shannon index

for j in shannon
do
qiime diversity alpha \
	--i-table table$f.qza \
	--p-metric $j \
	--o-alpha-diversity ${j}.qza

qiime tools export \
	--input-path ${j}.qza  \
	--output-path $j

mv $j/*.tsv ./ 
rm -rf $j
done
