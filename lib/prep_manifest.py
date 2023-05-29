# Make a manifest of data for qiime2
# Created by DCC
# 2023/2/27

import pandas as pd
import os
import sys


def create_manifest2(input_path, nail):

    forward2 = []
    reverse2 = []
    sample2 = []

    name = os.listdir(input_path)
    judge_num(name)

    if nail == 0:
        forward_nail = '1'
        reverse_nail = '2'
    else:
        forward_nail = '2'
        reverse_nail = '1'

    file_forward = [file for file in name if file.endswith(f"{forward_nail}.fastq.gz")]
    for i in file_forward:
        sample2, forward2, reverse2 = joint(sample2, forward2, reverse2, i, input_path, forward_nail, reverse_nail)

    return sample2, forward2, reverse2


def create_manifest1(input_path, metadata_file, connector, nail):

    forward1 = []
    reverse1 = []
    sample1 = []

    if nail == 0:
        forward_nail = '1'
        reverse_nail = '2'
    else:
        forward_nail = '2'
        reverse_nail = '1'

    ref = pd.read_excel(metadata_file)
    ref = ref.set_index('Data_ID')

    for rawdata_id in ref.index:
        forward_path = input_path + '/' + f'{rawdata_id}' + f'{connector}' + f'{forward_nail}.fastq.gz'
        reverse_path = input_path + '/' + f'{rawdata_id}' + f'{connector}' + f'{reverse_nail}.fastq.gz'
        if os.path.exists(forward_path) and os.path.exists(reverse_path):
            forward1.append(forward_path)
            reverse1.append(reverse_path)
            sample1.append(ref.loc[rawdata_id, 'Sample_ID'])
        elif not os.path.exists(forward_path) and os.path.exists(reverse_path):
            print(f"Warning! {forward_path} file does not exist")
        elif not os.path.exists(reverse_path) and os.path.exists(forward_path):
            print(f"Warning! {reverse_path} file do not exist")
        else:
            print(f"Warning! {forward_path} and {reverse_path} files do not exist")

    return sample1, forward1, reverse1


def judge_num(n):

    file_fastq_r1 = [file for file in n if file.endswith("1.fastq.gz")]
    file_fastq_r2 = [file for file in n if file.endswith("2.fastq.gz")]

    if len(file_fastq_r1) == len(file_fastq_r2):
        print("The number of forward and reverse sequences matches!")
    else:
        raise Exception("The number of forward and reverse sequences does not matches!")


def joint(sample_list, forward_list, reverse_list, string, path, forward_nail, reverse_nail):

    if f'_R{forward_nail}.fastq.gz' in string:
        connector = '_R'
        sample_list, forward_list, reverse_list = \
            judge_exist(sample_list, forward_list, reverse_list, string, path, forward_nail, reverse_nail, connector)
    elif f'-R{forward_nail}.fastq.gz' in string:
        connector = '-R'
        sample_list, forward_list, reverse_list = \
            judge_exist(sample_list, forward_list, reverse_list, string, path, forward_nail, reverse_nail, connector)
    elif f'_{forward_nail}.fastq.gz' in string:
        connector = '_'
        sample_list, forward_list, reverse_list = \
            judge_exist(sample_list, forward_list, reverse_list, string, path, forward_nail, reverse_nail, connector)
    elif f'-{forward_nail}.fastq.gz' in string:
        connector = '-'
        sample_list, forward_list, reverse_list = \
            judge_exist(sample_list, forward_list, reverse_list, string, path, forward_nail, reverse_nail, connector)
    else:
        raise Exception("Data naming format of sequences is error")

    return sample_list, forward_list, reverse_list


def judge_exist(sample_list, forward_list, reverse_list, string, input_path, forward_nail, reverse_nail, connector):
    t_forward = connector + forward_nail
    t_reverse = connector + reverse_nail
    label = str.split(string, f"{t_forward}.fastq.gz")[0]
    string_pair = label + f"{t_reverse}.fastq.gz"
    sample_list.append(label)

    if os.path.exists(input_path):
        forward_path = input_path + '/' + string
        forward_list.append(forward_path)
        reverse_path = input_path + '/' + string_pair
        reverse_list.append(reverse_path)
    else:
        reverse_path = input_path + '/' + string_pair
        print(f"warning! Missing {reverse_path} file")

    return sample_list, forward_list, reverse_list


if __name__ == '__main__':

    if sys.argv[3] == '1':
        sample, forward, reverse = create_manifest2(sys.argv[1], sys.argv[5])
    else:
        sample, forward, reverse = create_manifest1(sys.argv[1], sys.argv[3], sys.argv[4], sys.argv[5])

    dic = {"sample-id": sample, "forward-absolute-filepath": forward, "reverse-absolute-filepath": reverse}
    dic = pd.DataFrame(dic)
    output_file = sys.argv[2] + '/' + 'manifest.tsv'
    dic.to_csv(output_file, sep='\t', index=False)
