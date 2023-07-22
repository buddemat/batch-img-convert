#!/usr/bin/env python3
'''
batch-img-convert.py

date: 07-2023
maintainer: Matthias Budde
'''
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
argument_group = parser.add_mutually_exclusive_group()
parser.add_argument('inpath', help='input path for image conversion', default='.')
parser.add_argument('-r', '--recursive', help='traverse subfolders of inpath',
                           action='store_true')
argument_group.add_argument('-v', '--verbose', help='verbosity level (can be specified multiple times)',
                           action='count', default=0)
argument_group.add_argument('-q', '--quiet', help='suppress output, mutually exclusive with --verbose',
                           action='store_true')
args = parser.parse_args()

# process args
inpath = Path(args.inpath)
# TODO: check if outpath exists? Or do that on creation?
outpath = inpath / 'converted'

if args.quiet:
    verbosity = -1
else:
    verbosity = args.verbose

# Temporary code 
if verbosity >= 2:
    print(f'Running "{Path(__file__).resolve()}"...\n')
if verbosity >= 1:
    print(f'Input path is "{inpath.resolve()}".')
    print(f'Output path is "{outpath.resolve()}".')


