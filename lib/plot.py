#!/usr/bin/env python3


import os
import argparse


def plot_top10(input_file, output_path):
    cmd = "Rscript lib/plot_top10.R %s %s" % \
          (input_file, output_path)
    os.system(cmd)


def plot_type(input_file, output_path, genus_list):
    cmd = "Rscript lib/plot_enterotype.R %s %s %s" % \
          (input_file, output_path, genus_list)
    os.system(cmd)


if __name__ == "__main__":
    os.system("conda activate downstream")

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, help="The table of relative abundance on genus level")
    parser.add_argument('-s', '--select', type=str, required=True, help="The type of figure for plotting")
    parser.add_argument('-g', '--genus', type=str, default=0, help="The specified genus name to draw a boxplot after cluster")
    parser.add_argument('-o', '--output', type=str, help="Output path")

    args = parser.parse_args()

    if not os.path.exists(args.output):
        os.mkdir(args.output)

    if args.select == "top10":
        plot_top10(args.input, args.output)

    if args.select == "enterotype":
        plot_type(args.input, args.output, args.genus)
