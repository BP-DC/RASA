#!/usr/bin/env python3

# Created by DCC


import os
import argparse


def make_manifest(rawdata_path, output_path, list_file, connector, nail):
    cmd = "python lib/prep_manifest.py %s %s %s %s %s" % \
          (rawdata_path, output_path, list_file, connector, nail)
    os.system(cmd)


def import_file(manifest_file, primer_forward, primer_reverse, output_path):
    cmd = "bash lib/prep_preprocess.sh %s %s %s %s" % \
          (manifest_file, primer_forward, primer_reverse, output_path)
    os.system(cmd)


if __name__ == "__main__":
    os.system("conda activate qiime2-2022.8")
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--data', type=str, help="Raw data path")
    parser.add_argument('-l', '--list', type=str, default=1, help="Sample list")
    parser.add_argument('-m', '--manifest', type=str, help="Manifest file")
    parser.add_argument('-c', '--connector', type=str, default=None, help="The string between the ID and R1 label of the .fastq.gz file name")
    parser.add_argument('-n', '--nail', type=int, default=0, help="Number 1 represents the forward sequence is raw data of R2 labels")
    parser.add_argument('-f', '--forward', type=str, help="Forward primer sequence")
    parser.add_argument('-r', '--reverse', type=str, help="Reverse primer sequence")
    parser.add_argument('-o', '--output', type=str, help="Output path")

    args = parser.parse_args()

    if not os.path.exists(args.output):
        os.mkdir(args.output)

    if args.data and args.list and args.forward and args.reverse:
        make_manifest(args.data, args.output, args.list, args.connector, args.nail)
        import_file(args.output + '/' + 'manifest.tsv', args.forward, args.reverse, args.output)

    if args.data and args.list and not args.forward and not args.reverse:
        make_manifest(args.data, args.output, args.list, args.connector, args.nail)

    if args.manifest and args.forward and args.reverse:
        import_file(args.manifest, args.forward, args.reverse, args.output)
