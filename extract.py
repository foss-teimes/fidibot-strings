#! /usr/bin/env python
#
# Author: Nick Raptis <airscorp@gmail.com>

import sys, re
import json

regex = re.compile(r"""_\(['"].*['"]\)""")

def main():
    if len(sys.argv) == 1:
        infile = sys.stdin
        outfile = sys.stdout
    elif len(sys.argv) == 2:
        infile = open(sys.argv[1], 'rb')
        outfile = sys.stdout
    elif len(sys.argv) == 3:
        infile = open(sys.argv[1], 'rb')
        outfile = open(sys.argv[2], 'wb')
    else:
        raise SystemExit(sys.argv[0] + " [infile [outfile]]")
    
    tokens = []
    str_dict = {}
    for line in infile:
        tokens += regex.findall(line)
    for token in tokens:
        key = token[3:-2]
        str_dict[key] = [key]
    
    json.dump(str_dict, outfile, sort_keys=True, indent=4, separators=(',', ': '))
    outfile.write('\n')


if __name__ == '__main__':
    main()
