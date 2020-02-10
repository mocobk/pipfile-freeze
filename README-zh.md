# pipfile-freeze
这是一个将 Pipfile/Pipfile.lock 转换为 requirments.txt 的命令行工具

[![](https://img.shields.io/pypi/v/pipfile-freeze.svg)](https://pypi.org/project/pipfile-freeze)
[![](https://img.shields.io/pypi/pyversions/pipfile-freeze.svg)](https://pypi.org/project/pipfile-freeze)

## Required Python version

`>=2.7, >=3.4`

## 能做什么?

该工具是基于[requirementslib] [1]开发，提供了一个简单的命令行工具，可以将 Pipenv 管理的依赖文件转换为通用的 requirements.txt 文件。 

Pipenv 可以很好地管理虚拟环境和依赖包，但在项目部署过程中不具优势。 原因在于 pip 比 pipenv 安装依赖要快得多，因为后者还需要发送额外的请求给 PyPI 进行哈希检查。另外在正式部署中安装 Pipenv 可能也会显得冗余，尤其是采用 docker 方式去部署。这种情况下我们一般只需提供一份 requirements.txt 文件来告诉持续集成工具或生产服务器应安装哪些依赖包和版本。

## 安装

```bash
$ pip install pipfile-freeze
```
安装完成后在你的终端就可以使用 `pipfile` 这个命令了


## 举例:
```
直接输出依赖到终端:
$ pipfile freeze

输出依赖到文件, 仅使用 -o 参数的话，默认保存为 './requirements.txt':
$ pipfile freeze -o
$ pipfile freeze -o /path/requirements.txt

指定项目根目录来查找 Pipfile, 默认在当前目录下查找
$ pipfile freeze -p myproject

更复杂的例子
$ pipfile freeze -p myproject --hashes -d -o /path/requirements.txt
```

假如你的 Pipfile 文件是这样子的:
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

转换后输出 requirements.txt :

```
--index-url http://pypi.tuna.tsinghua.edu.cn/simple
--trusted-host pypi.tuna.tsinghua.edu.cn
--extra-index-url https://pypi.org/simple

apscheduler
ilogger==0.1
pywinusb; sys_platform == 'win32'
requests
```

## 用法:

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

这个工具是在 [pipfile-requirements][2] 的基础上改进的，感谢 [@frostming][2] 的开源贡献。


[1]: https://github.com/sarugaku/requirementslib
[2]: https://github.com/frostming/pipfile-requirements