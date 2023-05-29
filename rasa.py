#!/usr/bin/env python3
# -*- coding: utf-8 -*
# Author: Changchang Ding

import sys
import argparse
import os

DESCRIPTION = """
===========================================================

    16s rDNA amplicon sequencing analysis (RASA)

===========================================================
"""

VERSION = "Version 1.0"

if __name__ == '__main__':
    dir_name, file_name = os.path.split(os.path.abspath(sys.argv[0]))
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('-v', '--version', action='version', version=VERSION)
    subparsers = parser.add_subparsers(dest='command', help='sub-command help')

# Add a 16s rDNA sequence preprocess module
    parser_prep = subparsers.add_parser("prep", help='Make a manifest of raw data')
    parser_prep.add_argument('-d', '--data', type=str, help="Raw data path")
    parser_prep.add_argument('-l', '--list', type=str, default=1, help="Sample list")
    parser_prep.add_argument('-m', '--manifest', type=str, help="Manifest file")
    parser_prep.add_argument('-c', '--connector', type=str, default=None, help="The string between the ID and R1 label of the .fastq.gz file name")
    parser_prep.add_argument('-n', '--nail', type=int, default=0, help="Number 1 represents the forward sequence is raw data of R2 labels")
    parser_prep.add_argument('-f', '--forward', type=str, help="Forward primer sequence")
    parser_prep.add_argument('-r', '--reverse', type=str, help="Reverse primer sequence")
    parser_prep.add_argument('-o', '--output', type=str, help="Output path")

# Add a 16s rDNA sequence process module
    parser_proc = subparsers.add_parser("proc", help='Bioinformatics analysis of DNA sequences using qiime2')
    parser_proc.add_argument('-i', '--input', type=str, help="The paired-end sequence qza file for paired merging")
    parser_proc.add_argument('-c_f', '--trunc_f', type=int, help="Forward sequence 3' end truncation position using Dada2")
    parser_proc.add_argument('-c_r', '--trunc_r', type=int, help="Reverse sequence 3' end truncation position using Dada2")
    parser_proc.add_argument('-m_f', '--trim_f', type=int, help="Forward sequence 5' end truncation position using Dada2")
    parser_proc.add_argument('-m_r', '--trim_r', type=int, help="Reverse sequence 5' end truncation position using Dada2")
    parser_proc.add_argument('-p', '--overlap', type=int, default=12, help="Dada2 method parameter: length of overlap")
    parser_proc.add_argument('-t', '--threads_n', type=int, default=1, help="Calculation and number of CPUs used")
    parser_proc.add_argument('-r', '--classifier', type=str, default=1, help="A trained Bayesian classifier path")
    parser_proc.add_argument('-f', '--filter', type=int, default=1, help="Value 0 represent not removed mitochondria and chloroplasts")
    parser_proc.add_argument('-o', '--output', type=str, help="Output path")

# Add a relative abundance extraction module
    parser_stats = subparsers.add_parser("stats", help="Extract specific and top n bacteria")
    parser_stats.add_argument('-s', '--select', type=str, help="Select the function of taxonomic abundance")
    parser_stats.add_argument('-i', '--input', type=str, help="Relative abundance tsv file")
    parser_stats.add_argument('-l', '--level', type=str, help="The level of relative abundance file")
    parser_stats.add_argument('-r', '--ref_file', type=str, help="The specific name of bacteria")
    parser_stats.add_argument('-t', '--top_n', type=int, help="The number of extracting bacteria by relative abundance")
    parser_stats.add_argument('-o', '--output', type=str, help="Output path")

# Add a plotting module
    parser_plot = subparsers.add_parser("plot", help="Plot top 10 genus and enterotype analysis result")
    parser_plot.add_argument('-i', '--input', type=str, help="The table of relative abundance on genus level")
    parser_plot.add_argument('-s', '--select', type=str, required=True, help="The type of figure for plotting")
    parser_plot.add_argument('-g', '--genus', type=str, default=0, help="The specified genus name to draw a boxplot after cluster")
    parser_plot.add_argument('-o', '--output', type=str, help="Output path")

    if len(sys.argv[1:]) == 0:
        parser.print_help()
        exit()

    args = vars(parser.parse_args())
    command = "%s %s/lib/%s.py " % (sys.executable, dir_name, args["command"])
    command += ' '.join(sys.argv[2:])
    os.system(command)
    exit()
