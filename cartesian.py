#!/usr/bin/python3

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

def get_stdin():
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        return sys.stdin.readlines()

def line_strip(lines,sep):
    for line in lines:
        yield line.rstrip(sep)

def generate(*paths,stdin=False,sep=EMPTY_STRING,line_sep=LINE_SEP,all=False):
    with contextlib.ExitStack() as stack:
        stdin_lines = get_stdin()
        files = [line_strip(
            stack.enter_context(open(path,'r')),
            line_sep
        ) for path in paths]
        if stdin_lines:
            stdin_lines = line_strip(stdin_lines,line_sep)
            if stdin:
                files.insert(0,stdin_lines)
            else:
                files.append(stdin_lines)
        if all:
           for contents in permutations(*files):
                print(sep.join(contents))
        else:
            for contents in product(*files):
                print(sep.join(contents))
            
def product(*datas):
    for contents in itertools.product(*datas):
        yield contents
    
def permutations(*datas):
    for contents in product(*datas):
        for content in itertools.permutations(contents):
            yield content
        
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
    group.add_argument(
        "-s",dest='stdin',action='store_true', help="use stdin to first"
    )
    group.add_argument(
        "-a",dest='all',action='store_true', help="show all possible orderings"
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
    print(args)
    generate(*paths,all=args.all,stdin=args.stdin,sep=args.sep,line_sep=args.line)
    
if __name__ == "__main__":
    main()
