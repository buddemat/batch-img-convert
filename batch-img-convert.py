#!/usr/bin/env python3
'''
batch-img-convert.py

date: 07-2023
maintainer: Matthias Budde
'''
import sys
import argparse
from pathlib import Path
from multiprocessing import Pool, cpu_count
import tqdm


def get_args():
    '''Parse command line arguments.'''
    cpucount = cpu_count()
    parser = argparse.ArgumentParser()
    argument_group = parser.add_mutually_exclusive_group()
    parser.add_argument('inpath', help='input path for image conversion', default='.')
    parser.add_argument('-r', '--recursive',
                        help='traverse subfolders of inpath',
                        action='store_true')
    parser.add_argument('-p', '--pool',
                        type=int,
                        help='poolsize for data parallelism. \
                              if option string is present without argument, then half \
                              the number of cpus are used.',
                        const=cpucount//2,
                        default=1,
                        nargs='?')
    argument_group.add_argument('-v', '--verbose',
                                help='verbosity level (can be specified multiple times)',
                                action='count',
                                default=0)
    argument_group.add_argument('-q', '--quiet',
                                help='suppress output, mutually exclusive with --verbose',
                                action='store_true')
    args = parser.parse_args()

    # process args into dict
    opts_dict = args.__dict__
    opts_dict['poolsize'] = opts_dict.pop('pool') # "rename" entry
    opts_dict['cpucount'] = cpucount

    # replace strings with paths
    opts_dict['inpath'] = Path(args.inpath)
    # TODO: check if outpath exists? Or do that later on creation?
    opts_dict['outpath'] = opts_dict['inpath'] / 'converted'

    if args.quiet:
        opts_dict['verbosity'] = -1
    else:
        opts_dict['verbosity'] = opts_dict.pop('verbose')
    opts_dict.pop('quiet')
    return opts_dict


def convert_img(file):
    '''Load file convert it.'''
    with open(file, 'r', encoding='utf-8') as f:
        # TODO: do I need to open it?
        if opts['verbosity'] >= 2:
            print(file)
        return False


if __name__ == '__main__':
    opts = get_args()

    # temporary code
    if opts['verbosity'] >= 2:
        print(f'Running "{Path(__file__).resolve()}"...\n')
    if opts['verbosity'] >= 1:
        print(f'Input path is "{opts["inpath"].resolve()}".')
        print(f'Output path is "{opts["outpath"].resolve()}".')
    print('')


    # parallel processing
    if opts['recursive']:
        p = opts['inpath'].rglob('*.tif') # TODO: expand beyonf tiffs
    else:
        p = opts['inpath'].glob('*.tif') # TODO: expand beyonf tiffs
    fileslist = [f for f in p if f.is_file()]
    filenum = len(fileslist)

    if filenum < 1:
        print('No files found, exiting...')
        sys.exit()

    with Pool(opts['poolsize']) as p:
        r = list(tqdm.tqdm(p.imap(convert_img, fileslist), total=filenum))
