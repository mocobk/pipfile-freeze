# -*- coding: utf-8 -*-
# @File : pipfile_freeze.py
# @Author : mocobk
# @Email : mailmzb@qq.com

import argparse
import io
import itertools
import json
import os
import sys
import warnings
from urllib.parse import urlparse

from requirementslib import Lockfile, Requirement, Pipfile
from vistir.compat import Path
from vistir.misc import dedup, to_text

if sys.version_info[:2] == (2, 7):
    class FileNotFoundError(OSError):
        pass


def _parse_args_or_exit(parser):
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    return parser.parse_args()


def parse_args():
    usage = """Examples:
   Output requirements directly to the console:
   $ pipfile freeze

   Output requirements to the file, default './requirements.txt' with -o:
   $ pipfile freeze -o
   $ pipfile freeze -o filename
   
   More help:
   $ pipfile freeze -h
    """
    parser = argparse.ArgumentParser(
        prog='pipfile',
        description=usage,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(metavar='command')
    sub_parser = subparsers.add_parser('freeze', help='Convert Pipfile* to requirements format')

    sub_parser.add_argument(
        "-p", "--project", default=".", type=Path, help="Specify another project root"
    )
    sub_parser.add_argument(
        "--hashes",
        default=False,
        action="store_true",
        help="whether to include the hashes",
    )
    sub_parser.add_argument(
        "-d",
        "--dev",
        default=False,
        action="store_true",
        help="whether to choose both develop and default packages",
    )
    sub_parser.add_argument(
        "-o",
        "--outfile",
        nargs="?",
        default=None,
        const='./requirements.txt',
        metavar='file',
        help="Output requirements to the file"
    )
    sub_parser.add_argument(
        "file",
        nargs="?",
        default=None,
        help="The file path to convert, support both Pipfile and Pipfile.lock. "
             "If it isn't given, will try Pipfile.lock first then Pipfile.",
    )
    return _parse_args_or_exit(parser)


def _single_source_as_line(source, extra):
    url = source["url"]
    if extra:
        lines = ["--extra-index-url {}".format(url)]
    else:
        lines = ["--index-url {}".format(url)]
    if source.get("verify_ssl", True) and url.startswith('http:'):
        lines = ["{}\n--trusted-host {}".format(lines[0], urlparse(url).hostname)]
    return lines


def _sources_as_lines(sources):
    source_lines = list(dedup(itertools.chain(
        itertools.chain.from_iterable(
            _single_source_as_line(source, False)
            for source in sources[:1]
        ),
        itertools.chain.from_iterable(
            _single_source_as_line(source, True)
            for source in sources[1:]
        ),
    )))
    return source_lines


def _requirement_as_line(requirement, include_hashes):
    line = to_text(
        requirement.as_line(include_hashes=include_hashes)
    )
    return line


def _convert(file_instance, sources, section_names, hashes=False):
    """
    :param file_instance: pipfile or lockfile instance
    :param hashes: bool
    :return: list
    """
    sources_lines = _sources_as_lines(sources)

    requirements = [
        Requirement.from_pipfile(key, entry._data)
        for key, entry in itertools.chain.from_iterable(
            file_instance.get(name, {}).items()
            for name in section_names
        )
    ]

    if hashes:
        hashes = all(r.is_named for r in requirements)

    requirement_lines = sorted(dedup(
        _requirement_as_line(requirement, hashes)
        for requirement in requirements
    ))
    return sources_lines + [''] + requirement_lines


def _convert_pipfile(pipfile, dev=False):
    pipfile = Pipfile.load(pipfile).pipfile
    section_names = ["packages"]
    if dev:
        section_names.append("dev-packages")
    sources = pipfile.source

    return _convert(pipfile, sources, section_names, hashes=False)


def _convert_pipfile_lock(lockfile, hashes=False, dev=False):
    lockfile = Lockfile.load(lockfile).lockfile
    section_names = ["default"]
    if dev:
        section_names.append("develop")
    sources = lockfile.meta.sources._data

    return _convert(lockfile, sources, section_names, hashes=hashes)


def convert_pipfile_or_lock(project, pipfile=None, hashes=False, dev=False):
    """Convert given Pipfile/Pipfile.lock to requirements.txt content.
    :param project: the project path, default to `pwd`.
    :param pipfile: the path of Pipfile or Pipfile.lock. If it isn't given, will try
                    Pipfile.lock first then Pipfile.
    :param hashes: whether to include hashes
    :param dev: whether to choose both develop and default packages.
    :returns: the content of requirements.txt
    """
    if pipfile is None:
        if project.joinpath("Pipfile.lock").exists():
            pipfile = "Pipfile.lock"
        elif project.joinpath("Pipfile").exists():
            pipfile = "Pipfile"
    if pipfile and not Path(pipfile).is_absolute():
        full_path = project.joinpath(pipfile).as_posix()
    else:
        full_path = pipfile
    if pipfile is None or not os.path.exists(full_path):
        raise FileNotFoundError("No Pipfile* is found.")
    try:
        with io.open(full_path, encoding="utf-8") as f:
            json.load(f)
    except Exception:
        if hashes:
            warnings.warn(
                "Pipfile is given, the hashes flag won't take effect.\n", UserWarning
            )
        return _convert_pipfile(full_path, dev)
    else:
        return _convert_pipfile_lock(full_path, hashes, dev)


def main():
    args = parse_args()
    lines = convert_pipfile_or_lock(args.project, args.file, args.hashes, args.dev)
    if args.outfile:
        outfile = os.path.abspath(args.outfile)
        with open(outfile, 'w') as f:
            f.write('\n'.join(lines))
        print('Requirements file saved in:\n{}'.format(outfile))
    else:
        for line in lines:
            print(line)


if __name__ == "__main__":
    main()
