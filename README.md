# batch-img-convert

**work in progres...**

Batch image conversion script in Python.


## Usage

``` 
batch-img-convert.py [-h] [-p [1:MAXCPUS]] [-q] [-r] [-s FACTOR] [-t {PNG,JPEG}] [-v] inpath
``` 
#### Positional arguments
 
``` 
  inpath                input (root) path for image conversion
``` 

#### Optional arguments
``` 
  -h, --help            show help message and exit
  -r, --recursive       whether to traverse subfolders of inpath
  -p POOLSIZE, --pool POOLSIZE
                        poolsize for data parallelism (int in range [1,maxcpus]), half the number of cpus if "--pool"
                        is specified without argument
  -s FACTOR, --scale FACTOR
                        scale factor to apply
  -t {PNG,JPEG}, --target {PNG,JPEG}
                        target output format(s), default: PNG
  -v, --verbose         verbosity level (incremental, up to 3: -vvv)
  -q, --quiet           suppress output, mutually exclusive with --verbose
``` 


## Repository structure

```
batch-img-convert
├── .gitignore
├── batch-img-convert.py               # Main conversion script.
└── README.md                          # This file.
```
