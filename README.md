# pipfile-freeze
CLI tool to convert Pipfile/Pipfile.lock to requirments.txt

[![](https://img.shields.io/pypi/v/pipfile-freeze.svg)](https://pypi.org/project/pipfile-freeze)
[![](https://img.shields.io/pypi/pyversions/pipfile-freeze.svg)](https://pypi.org/project/pipfile-freeze)

## Required Python version

`>=2.7, >=3.4`

## What does it do?

The tool is built on top of [requirementslib][1] to provide a simple CLI to
convert the Pipenv-managed files to requirements.txt.

Pipenv is a great tool for managing virtualenvs and dependencies, but it may be not that useful in deployment.
Pip installation is much faster than Pipenv manipulation, since the latter needs extra requests to PyPI for hash checking.
Installing a Pipenv in deployment may be overkilled. We just need a requirements.txt to tell CI or production server
which packages and versions should be installed.


## Installation

```bash
$ pip install pipfile-freeze
```

An executable named `pipfile` will be ready for use in the bin path.


## Examples:
```
Output requirements directly to the console:
$ pipfile freeze

Output requirements to the file, default './requirements.txt' with -o:
$ pipfile freeze -o
$ pipfile freeze -o /path/requirements.txt

Specify a project root path
$ pipfile freeze -p myproject

Complex example
$ pipfile freeze -p myproject --hashes -d -o /path/requirements.txt
```

If your Pipfile like this:
```toml
[[source]]
name = "tuna"
url = "http://pypi.tuna.tsinghua.edu.cn/simple"
verify_ssl = true

[[source]]
name = "pypi"
url = "https://pypi.org/simple"
verify_ssl = true

[dev-packages]

[packages]
requests = "*"
ilogger = "==0.1"
apscheduler = "*"
pywinusb = {version = "1.1", sys_platform = "== 'win32'"}

[requires]
python_version = "3.7"
```

Here is the output (requirements.txt):

```
--index-url http://pypi.tuna.tsinghua.edu.cn/simple
--trusted-host pypi.tuna.tsinghua.edu.cn
--extra-index-url https://pypi.org/simple

apscheduler
ilogger==0.1
pywinusb; sys_platform == 'win32'
requests
```

## Usage:

```
$ pipfile freeze --help
usage: pipfile freeze [-h] [-p PROJECT] [--hashes] [-d] [-o [file]] [file]

positional arguments:
  file                  The file path to convert, support both Pipfile and
                        Pipfile.lock. If it isn't given, will try Pipfile.lock
                        first then Pipfile.

optional arguments:
  -h, --help            show this help message and exit
  -p PROJECT, --project PROJECT
                        Specify another project root
  --hashes              whether to include the hashes
  -d, --dev             whether to choose both develop and default packages
  -o [file], --outfile [file]
                        Output requirements to the file
                        
```

## License

[MIT](/LICENSE)

This tool is improved based on the [pipfile-requirements][2] tool, thanks to [@frostming][2] for his contribution.

[1]: https://github.com/sarugaku/requirementslib
[2]: https://github.com/frostming/pipfile-requirements