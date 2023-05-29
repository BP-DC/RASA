#!/usr/bin/env python3
# Extract the relative abundance of specific phylum, family, genus and species bacterial names
import pandas as pd
import sys


def extract_specific(data, ref, level, output_path):

	level_temp = level + '__'

	asv_tax = data[data['#OTU ID'].str.contains(level_temp)]
	asv_tax = asv_tax.set_index('#OTU ID')
	asv_tax.index = asv_tax.index.str.split(level_temp).str[-1]

	result = pd.DataFrame(columns=asv_tax.columns)

	for n in range(len(ref['Name'])):

		if any(asv_tax.index == ref.loc[n, 'Name']):
			filter_data = asv_tax[asv_tax.index == ref.loc[n, 'Name']]
		else:
			filter_data = \
				pd.DataFrame(data=[['0'] * len(asv_tax.columns)], index=[ref.loc[n, 'Name']], columns=asv_tax.columns)

		result = pd.concat([result, filter_data], axis=0)

	result = result.applymap(lambda x: float(x))
	result = result.applymap(lambda x: '%.3f' % (x * 100))

	result.to_csv(f'{output_path}/specific_tax_level{level}.csv')


if __name__ == "__main__":
	input_data = pd.read_csv(sys.argv[1], sep='\t', header=1)
	ref_path = sys.argv[2]

	if ref_path.endswith(".xls"):
		ref_data = pd.read_excel(ref_path)
	elif ref_path.endswith(".csv"):
		ref_data = pd.read_csv(ref_path)
	else:
		raise Exception("Error! The format of the reference data is invalid. Please enter data in .csv or .xls format!")

	extract_specific(input_data, ref_data, sys.argv[3], sys.argv[4])
