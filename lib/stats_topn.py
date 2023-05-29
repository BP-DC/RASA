#!/usr/bin/env python3
# Extract the relative abundance of top n

import pandas as pd
import sys


def extract_topn(input_data, level, top_n, output_path):

	level = level + '__'
	asv_tax = input_data[input_data['#OTU ID'].str.contains(level)]
	asv_tax = asv_tax.rename(columns={'#OTU ID': f'Top {top_n} genus'})
	asv_tax = asv_tax.set_index(f'Top {top_n} genus')
	asv_tax.index = asv_tax.index.str.split(level).str[-1]
	asv_tax = asv_tax[asv_tax.index != "uncultured"]
	
	for i in asv_tax.columns:
		temp = asv_tax[[i]]
		temp = temp.sort_values(by=i, ascending=False)
		temp = temp[0:top_n]
		temp = temp.applymap(lambda x:'%.3f'%(x*100))
		output = temp.reset_index()
		output = output.replace('_', ' ', regex=True)
		output.to_csv(f'{output_path}/{i}_top{top_n}.csv', index=False, encoding='gbk')


if __name__ == "__main__":
	input_file = pd.read_csv(sys.argv[1], sep='\t', header=1)
	extract_topn(input_file, sys.argv[2], int(sys.argv[3]), sys.argv[4])
