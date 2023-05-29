#!/usr/bin/env python3


import os
import argparse


def extract_specific(input_file, ref_file, level_number, output_path):
    cmd = "python lib/stats_specific.py %s %s %s %s" % \
          (input_file, ref_file, level_number, output_path)
    os.system(cmd)


def extract_topn(input_file, level_str, top_n_number, output_path):
    cmd = "python lib/stats_topn.py %s %s %s %s" % \
          (input_file, level_str, top_n_number, output_path)
    os.system(cmd)


if __name__ == "__main__":
    os.system("conda activate qiime2-2022.8")
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--select', type=str, help="Select the function of taxonomic abundance")
    parser.add_argument('-i', '--input', type=str, help="Relative abundance tsv file")
    parser.add_argument('-l', '--level', type=str, help="The level of relative abundance file")
    parser.add_argument('-r', '--ref_file', type=str, help="The specific name of bacteria")
    parser.add_argument('-t', '--top_n', type=int, help="The number of extracting bacteria by relative abundance")
    parser.add_argument('-o', '--output', type=str, help="Output path")

    args = parser.parse_args()

    if not os.path.exists(args.output):
        os.mkdir(args.output)

    if args.select == "specific":
        extract_specific(args.input, args.ref_file, args.level, args.output)

    if args.select == "topn":
        extract_topn(args.input, args.level, args.top_n, args.output)
