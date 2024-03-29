# batch-img-convert

Batch image conversion script in Python.

Reencodes all TIFF files found in the input folder (and optionally its subfolders) to PNG and/or JPG format. Can optionally also scale the images' resolution (either relative or absolute). Supports data parallelism through multiprocessing.


## Usage

``` 
batch-img-convert.py [-h] [-c | -f] [-p [1:MAXCPUS]] [-q] [-r] [-s FACTOR|PX] [-t {PNG,JPG}] [-v] inpath [outpath]
``` 
#### Positional arguments
 
``` 
inpath                             input (root) path for image conversion
outpath                            output path for image conversion (optional)
``` 

#### Option arguments
``` 
-h, --help                         show help message and exit

-c, --continue                     skip existing files, mutually exclusive with --force

-f, --force                        overwrite existing files, mutually exclusive with --continue

-p POOLSIZE, --pool POOLSIZE       poolsize for data parallelism (int in range [1,maxcpus]), half
                                   the number of cpus if "--pool" is specified without parameter

-q, --quiet                        suppress output, mutually exclusive with --verbose

-r, --recursive                    whether to traverse subfolders of inpath

-s FACTOR|PX, --scale FACTOR|PX    scale factor (if INT) or target resolution (if FLOAT)

-t {PNG,JPG}, --target {PNG,JPG}   target output format(s), multiple possible, default: PNG

-v, --verbose                      verbosity level (incremental, up to 3: -vvv)
``` 


## Repository structure

```
batch-img-convert
├── .gitignore
├── batch-img-convert.py               # Main conversion script
├── README.md                          # This file
└── requirements.txt                   # List of package dependencies
```
