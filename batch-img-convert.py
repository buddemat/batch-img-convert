#!/usr/bin/env python3
'''
batch-img-convert.py

date: 07-2023
maintainer: Matthias Budde
'''
import sys
import argparse
from pprint import pprint
from pathlib import Path
from multiprocessing import Pool, cpu_count
import tqdm
from PIL import Image
from PIL.Image import Resampling

def test_scale_type(arg):
    '''Test whether scale argument is valid (float or int) for use in argparse argument.'''
    try:
        arg = int(arg)
        if arg <= 160:
            msg = 'Target resolution is too small, must be at least 160.'
            raise argparse.ArgumentTypeError(msg)
        return arg
    except ValueError:
        pass
    try: 
        arg = float(arg)
        if not 0.1 <= arg <= 4.0:
            msg = 'Scale factor too large, must be between 0.1 and 4.0.'
            raise argparse.ArgumentTypeError(msg)
        return arg
    except ValueError as err:
        raise argparse.ArgumentTypeError(err)


def get_args():
    '''Parse command line arguments.'''
    cpucount = cpu_count()
    parser = argparse.ArgumentParser()
    verbosity_argument_group = parser.add_mutually_exclusive_group()
    resume_argument_group = parser.add_mutually_exclusive_group()
    parser.add_argument('inpath', help='input path for image conversion', default='.')
    parser.add_argument('outpath', help='output path for image conversion (optional)', nargs='?')
    resume_argument_group.add_argument('-c', '--continue',
                                       help='skip existing files, mutually exclusive with --force',
                                       action='store_true')
    resume_argument_group.add_argument('-f', '--force',
                                       help='overwrite existing files, mutually exclusive \
                                             with --continue',
                                       action='store_true',
                                       dest='overwrite')
    parser.add_argument('-p', '--pool',
                        type=int,
                        help='poolsize for data parallelism (int in range [1,maxcpus]), \
                              half the number of cpus if "--pool" is specified without \
                              following argument',
                        const=cpucount//2,
                        default=1,
                        choices=range(1,cpucount+1),
                        nargs='?',
                        metavar='1:MAXCPUS',
                        dest='poolsize')
    verbosity_argument_group.add_argument('-q', '--quiet',
                                          help='suppress output, mutually exclusive with --verbose',
                                          action='store_const',
                                          default=0,
                                          const=-1,
                                          dest='verbosity')
    parser.add_argument('-r', '--recursive',
                        help='whether to traverse subfolders of inpath',
                        action='store_true')
    parser.add_argument('-s', '--scale',
                        type=test_scale_type,
                        metavar='FACTOR|PIXELS',
                        help='scale factor (if float) or target resolution (if int) to apply',
                        default=None)
    parser.add_argument('-t', '--target',
                        #metavar='TYPE',
                        help='target output format(s), default: PNG',
                        choices=['PNG','JPEG'],
                        # do not set 'default', as 'append' will always include default value
                        default=None,
                        action='append',
                        dest='outtypes')
    verbosity_argument_group.add_argument('-v', '--verbose',
                                          help='verbosity level (incremental, up to 3: -vvv)',
                                          action='count',
                                          default=0,
                                          dest='verbosity')
    args = parser.parse_args()

    # process args into dict
    opts_dict = args.__dict__.copy()
    opts_dict['cpucount'] = cpucount

    # check output formats
    if opts_dict['outtypes'] is None:
        opts_dict['outtypes'] = ['PNG']

    # replace strings with paths
    opts_dict['inpath'] = Path(args.inpath).resolve()
    if not args.outpath:
        opts_dict['outpath'] = opts_dict['inpath'] / 'converted'
    else:
        opts_dict['outpath'] = Path(args.outpath).resolve()

    # check if scaling is meant to be relative or absolute
    if isinstance(opts_dict['scale'], int):
        if opts_dict['verbosity'] >= 2:
            print('As --scale parameter is of type int, interpreting as absolute resolution value (keeping aspect ratio).')
        opts_dict['scaleabs'] = opts_dict.pop('scale')
    elif isinstance(opts_dict['scale'], float):
        if opts_dict['verbosity'] >= 2:
            print('As --scale parameter is of type float, interpreting as relative scale factor.')
        opts_dict['scalefactor'] = opts_dict.pop('scale')
    return opts_dict


def convert_img(file):
    '''Load file, convert it.'''
    # build target file path
    file_new = file.relative_to(opts['inpath'])
    file_new = opts['outpath'] / file_new.with_suffix('')

    # if check if target files already exist
    formats_to_encode =  opts['outtypes'].copy()
    if opts['continue']:
        for target_format in opts['outtypes']:
            check_file = file_new.with_suffix(f'.{target_format.lower()}')
            if check_file.is_file():
                if opts['verbosity'] >= 3:
                    print(f'"{check_file}" already exists, skipping...')
                formats_to_encode.remove(target_format)

    if formats_to_encode:
        with Image.open(file) as img:
            if opts['verbosity'] >= 3:
                print(f'Reading "{img.filename}"...')

            # conversion
            if opts.get('scaleabs'):
                if img.width > img.height:
                    wdth = opts['scaleabs']
                    hght = int(opts['scaleabs'] // (img.width/img.height))
                else:
                    wdth = int(opts['scaleabs'] // (img.height/img.width))
                    hght = opts['scaleabs']
            elif opts.get('scalefactor'):
                wdth = int(img.width // (1/opts['scalefactor']))
                hght = int(img.height // (1/opts['scalefactor']))
            if opts.get('scaleabs') or opts.get('scalefactor'):
                if opts['verbosity'] >= 3:
                    print(f'Scaling to {wdth} x {hght} (width x height)')
                img = img.resize((wdth, hght), Resampling.LANCZOS)

            # create folders if they don't exist
            file_new.parent.mkdir(parents=True, exist_ok=True)

            for target_format in formats_to_encode:
                file_new = file_new.with_suffix(f'.{target_format.lower()}')
                if opts['verbosity'] >= 3:
                    print(f'Writing "{file_new}"...')
                img.save(file_new, target_format)
        return file
    return None

if __name__ == '__main__':
    opts = get_args()

    # info
    if opts['verbosity'] >= 2:
        opts['scriptpath']= Path(__file__).resolve()
        pprint(opts, indent=4)
        print('')
    elif opts['verbosity'] >= 1:
        print(f'Input path is "{opts["inpath"]}".')
        print(f'Output path is "{opts["outpath"]}".')
        print('')

    # prepare
    if opts['recursive']:
        p = opts['inpath'].rglob('*.tif')
    else:
        p = opts['inpath'].glob('*.tif')
    fileslist = [f for f in p if f.is_file()]
    filenum = len(fileslist)

    if filenum < 1:
        sys.exit(f'Error: No suitable files found in "{opts["inpath"]}". Use --recursive to include subfolders. Exiting...')

    if not opts['continue']:
        try:
            opts['outpath'].mkdir(parents=False, exist_ok=opts['overwrite'])
        except FileExistsError as err:
            sys.exit(f'Error: The target folder already exists! Use --force to overwrite. {err}. Exiting...')


    # parallel processing
    # TODO: expand beyond tiffs

    if opts['verbosity'] >= 1:
        print(f'Found {filenum} TIF files. Converting to {", ".join(opts["outtypes"])} ' \
              f'using {opts["poolsize"]} cores...')

    with Pool(opts['poolsize']) as p:
        if opts['verbosity'] >= 0:
            r = list(tqdm.tqdm(p.imap(convert_img, fileslist), total=filenum))
        else:
            r = p.map(convert_img, fileslist)
