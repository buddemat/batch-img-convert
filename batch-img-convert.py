#!/usr/bin/env python3
'''
batch-img-convert.py

date: 07-2023
maintainer: Matthias Budde
'''
import sys
import argparse
import pprint
from pathlib import Path
from multiprocessing import Pool, cpu_count
import tqdm
from PIL import Image

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
    parser.add_argument('-s', '--scale',
                        type=float,
                        help='scale factor to apply.',
                        default=None)
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
    opts_dict['outpath'] = opts_dict['inpath'] / 'converted'
    try:
        opts_dict['outpath'].mkdir(parents=False, exist_ok=False)
    except FileExistsError as err:
        sys.exit(f'Error: The target folder already exists! {err} Exiting...')

    if args.quiet:
        opts_dict['verbosity'] = -1
    else:
        opts_dict['verbosity'] = opts_dict.pop('verbose')
    opts_dict.pop('quiet')
    return opts_dict


def convert_img(file):
    '''Load file convert it.'''
    with Image.open(file) as img:
        if opts['verbosity'] >= 3:
            print(f'Reading "{img.filename}"...')
        file_new = file.relative_to(opts['inpath'])
        file_new = opts['outpath'] / file_new.with_suffix('.png')
        # create folders if they don't exist
        file_new.parent.mkdir(parents=True, exist_ok=True)
        if opts['verbosity'] >= 3:
            print(f'Writing "{file_new}"...')
        if opts['scale']:
            factor = 1 / opts['scale']
            img = img.resize((int(img.width // factor), int(img.height // factor)))
        img.save(file_new, 'PNG')
        return file_new

if __name__ == '__main__':
    opts = get_args()

    # info
    if opts['verbosity'] >= 2:
        print(f'Running "{Path(__file__).resolve()}"...\n')
        print(pprint.pprint(opts, indent=4))
        print('')
    if opts['verbosity'] >= 1:
        print(f'Input path is "{opts["inpath"].resolve()}".')
        print(f'Output path is "{opts["outpath"].resolve()}".')
        print('')


    # parallel processing
    # TODO: expand beyond tiffs
    if opts['recursive']:
        p = opts['inpath'].rglob('*.tif')
    else:
        p = opts['inpath'].glob('*.tif')
    fileslist = [f for f in p if f.is_file()]
    filenum = len(fileslist)

    if filenum < 1:
        print('No files found, exiting...')
        sys.exit()

    if opts['verbosity'] >= 1:
        print(f'Found {filenum} .tif files. Converting to .png...')

    with Pool(opts['poolsize']) as p:
        r = list(tqdm.tqdm(p.imap(convert_img, fileslist), total=filenum))
