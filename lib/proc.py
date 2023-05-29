#!/usr/bin/env python3


import os
import argparse


def seq_process(input_file, trunc_f_number, trunc_r_number, trim_f_number, trim_r_number, overlap_number, threads_number, classifier_file, filter_number, output_path):
    cmd = "bash lib/proc_bioinfo.sh %s %s %s %s %s %s %s %s %s %s" % \
          (input_file, trunc_f_number, trunc_r_number, trim_f_number, trim_r_number, overlap_number, threads_number, classifier_file, filter_number, output_path)

    os.system(cmd)


if __name__ == "__main__":
    os.system("conda activate qiime2-2022.8")
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, help="The paired-end sequence qza file for paired merging")
    parser.add_argument('-c_f', '--trunc_f', type=int, help="Forward sequence 3' end truncation position using Dada2")
    parser.add_argument('-c_r', '--trunc_r', type=int, help="Reverse sequence 3' end truncation position using Dada2")
    parser.add_argument('-m_f', '--trim_f', type=int, help="Forward sequence 5' end truncation position using Dada2")
    parser.add_argument('-m_r', '--trim_r', type=int, help="Reverse sequence 5' end truncation position using Dada2")
    parser.add_argument('-p', '--overlap', type=int, default=12, help="Dada2 method parameter: length of overlap")
    parser.add_argument('-t', '--threads_n', type=int, default=1, help="Calculation and number of CPUs used")
    parser.add_argument('-r', '--classifier', type=str, default=1, help="A trained Bayesian classifier path")
    parser.add_argument('-f', '--filter', type=int, default=1, help="Value 0 represent not removed mitochondria and chloroplasts")
    parser.add_argument('-o', '--output', type=str, help="Output path")

    args = parser.parse_args()

    if not os.path.exists(args.output):
        os.mkdir(args.output)

    seq_process(args.input, args.trunc_f, args.trunc_r, args.trim_f, args.trim_r, args.overlap, args.threads_n, args.classifier, args.filter, args.output)
