#! /usr/bin/env python
#
# Author: Nick Raptis <airscorp@gmail.com>

import sys
import json
import shutil
import os.path
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.description = "Validate and pretty format fidibot JSON files"
    parser.add_argument('infile', nargs='+', help="input file")
    parser.add_argument('-n', '--no-overwrite', action="store_true",
                        help="don't overwrite the file(s) with pretty formatted version")
    parser.add_argument('-b', '--backup', action="store_true",
                        help="keep backups with extension .back")
    return parser.parse_args()


def main():
    args = get_args()
    
    # try to open and parse files
    print "Validating files:\n"
    files_dict = {}
    exceptions = {}
    for filename in args.infile:
        try:
            fp = open(filename)
            files_dict[filename] = json.load(fp)
            print "PASS: %s" % (filename)
        except IOError as e:
            raise SystemExit(e)
        except ValueError as e:
            exceptions[filename] = e
            print >> sys.stderr, "FAIL: %s -- %s" % (filename, e)
        finally:
            fp.close()
    if exceptions:
        raise SystemExit("\nOne or more files failed to validate!\nAborting!")
    
    if args.no_overwrite:
        return
    
    print "\nPretty Formatting files:"
    for filename in files_dict:
        if args.backup:
            shutil.copy2(filename, filename+".back")
        try:
            fp = open(filename, 'w')
            json.dump(files_dict[filename], fp,
                      sort_keys=True, indent=4, separators=(',', ': '))
            fp.write("\n")
            print "%s" % (filename)
        except IOError as e:
            raise SystemExit(e)
        finally:
            fp.close()


if __name__ == '__main__':
    main()
    print "\nFinished, ready for commit!"
