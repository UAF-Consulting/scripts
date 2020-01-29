#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
import gzip
import argparse
import apache_log_parser

def parse_args():
    parser = argparse.ArgumentParser(description='Parse Apache logs into TSV files')
    parser.add_argument('file', help='File to parse', nargs='+')
    parser.add_argument('tsv', help='TSV file to write to')
    parser.add_argument('format', help='Apache log format string')
    return parser.parse_args()

def read_file(path):
    data = []
    if path[-3:] == ".gz":
        with gzip.open(path, 'rt') as f:
            for line in f:
                data.append(line)
    else:
        with open(path, 'rt') as f:
            for line in f:
                data.append(line)

    return data

def parse_data(data, log_format):
    line_parser = apache_log_parser.make_parser(log_format)
    parsed_data = []
    for line in data:
        try:
            line_data = line_parser(line)
        except ValueError:
            print("ValueError: ", line)
        except:
            print("Error: ", line)

        parsed_data.append(line_data)

    return parsed_data

def write_tsv(data, headers, output_file):
    writer = csv.DictWriter(output_file, fieldnames=headers, delimiter='\t')
    if output_file.tell() == 0:
        writer.writeheader()

    for line in data:
        writer.writerow(line)

def main():
    args = parse_args()
    output = open(args.tsv, 'w')
    log_format = args.format

    for log in args.file:
        data = read_file(log)
        parsed = parse_data(data, log_format)
        headers = [*parsed[0].keys()]
        write_tsv(parsed, headers, output)

    output.close()


if __name__ == "__main__":
    main()
