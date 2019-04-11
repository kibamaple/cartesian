#!/usr/bin/python

import sys
import select
import argparse
import itertools
import contextlib

__author__ = "kiba.x.zhao"
__license__ = "MIT"
__version__ = "0.0.0"

EMPTY_STRING = ""
LINE_SEP = '\n'

def get_stdin(sep):
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        return line_strip(sys.stdin.readlines(),sep)

def line_strip(lines,sep):
    for line in lines:
        yield line.rstrip(sep)

def product(*paths,sep=EMPTY_STRING,line_sep=LINE_SEP):
    with contextlib.ExitStack() as stack:
        files = [line_strip(
            stack.enter_context(open(path,'r')),
            line_sep
        ) for path in paths]
        for line in generate(*files,sep=sep):
            print(line)

def generate(*datas,sep=EMPTY_STRING):
    for contents in itertools.product(*datas):
        yield sep.join(contents)

def get_parser():
    parser = argparse.ArgumentParser(description="Cartesian Product")
    parser.add_argument(dest='paths',nargs='*',help='path of files',metavar='filepath')
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "-v", "--version", action="store_true", help="Show the version of this program."
    )
    group.add_argument(
        "-t",dest='sep',default=EMPTY_STRING,metavar='CHARSET', help="use CHAR as output field separator"
    )
    group.add_argument(
        "-l",dest='line',default=LINE_SEP,metavar='CHARSET', help="use CHAR as input file line separator"
    )
    return parser

def version():
    print("cartesian version "+__version__)

def main():
    parser = get_parser()
    args = parser.parse_args()
    if args.version:
        version()
        return
    paths = args.paths
    stdin_paths = get_stdin(args.line)
    if stdin_paths:
        paths += stdin_paths
    product(*paths,sep=args.sep,line_sep=args.line)
    
if __name__ == "__main__":
    main()
