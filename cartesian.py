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

def get_readline():
    while True:
        line = sys.stdin.readline()
        if line:
            yield line
        else:
            break

def get_readlines():
    return sys.stdin.readlines()
            
def line_strip(lines,sep):
    for line in lines:
        yield line.rstrip(sep)

def generate(*paths,big=False,all=False,waitable=False,reverse=False,sep=EMPTY_STRING,line_sep=LINE_SEP):
    if waitable or sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        if big:
            stdin_lines = get_readline()
        else:
            stdin_lines = get_readlines()
    with contextlib.ExitStack() as stack:
        files = [line_strip(
            stack.enter_context(open(path,'r')),
            line_sep
        ) for path in paths]
        if stdin_lines:
            stdin_lines = line_strip(stdin_lines,line_sep)
            if reverse:
                files.append(stdin_lines)
            else:
                files.insert(0,stdin_lines)
        if all:
            for contents in permutations(*files):
                print(sep.join(contents))
            return
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
    parser.add_argument(
        "-v", "--version", action="store_true",required=False, help="Show the version of this program."
    )
    parser.add_argument(
        "-t",dest='sep',default=EMPTY_STRING,required=False,metavar='CHARSET', help="use CHAR as output field separator"
    )
    parser.add_argument(
        "-l",dest='line',default=LINE_SEP,metavar='CHARSET',required=False, help="use CHAR as input file line separator"
    )
    parser.add_argument(
        "-r","--reverse",action='store_true',required=False, help="append stdin after paths"
    )
    parser.add_argument(
        "-w","--waitable",action='store_true',required=False, help="wait stdin input"
    )
    parser.add_argument(
        "-a","--all",action='store_true',required=False,help="all possible orderings"
    )
    parser.add_argument(
        "-b","--big",action='store_true',required=False,help="stdin input big data"
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
    generate(*paths,big=args.big,all=args.all,waitable=args.waitable,reverse=args.reverse,sep=args.sep,line_sep=args.line)
    
if __name__ == "__main__":
    main()
