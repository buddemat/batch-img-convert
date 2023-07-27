# batch-img-convert

**work in progres...**

Batch image conversion script in Python.


## Usage

``` 
batch-img-convert.py [-h] [-c | -f] [-p [1:MAXCPUS]] [-q] [-r] [-s FACTOR] [-t {PNG,JPEG}] [-v] inpath [outpath]
``` 
#### Positional arguments
 
``` 
inpath                               input (root) path for image conversion
outpath                              output path for image conversion (optional)

``` 

#### Option arguments
``` 
-h, --help                           show help message and exit

-c, --continue                       skip existing files, mutually exclusive with --force

-f, --force                          overwrite existing files, mutually exclusive with --continue

-p POOLSIZE, --pool POOLSIZE         poolsize for data parallelism (int in range [1,maxcpus]), half
                                     the number of cpus if "--pool" is specified without argument

-q, --quiet                          suppress output, mutually exclusive with --verbose

-r, --recursive                      whether to traverse subfolders of inpath

-s FACTOR, --scale FACTOR            scale factor to apply

-t {PNG,JPEG}, --target {PNG,JPEG}   target output format(s), multiple possible, default: PNG

-v, --verbose                        verbosity level (incremental, up to 3: -vvv)
``` 


## Repository structure

```
batch-img-convert
├── .gitignore
├── batch-img-convert.py               # Main conversion script
└── README.md                          # This file
```
