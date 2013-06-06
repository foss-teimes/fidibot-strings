#! /usr/bin/env python
#
# Author: Nick Raptis <airscorp@gmail.com>

import sys
import json
import shutil
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


class ParameterMissmatchError(TypeError):
    pass

def count_fmt_params(string):
    """Count the number of parameters the string accepts"""
    string = string.replace("%%", "")
    return len(string.split("%")) - 1

def check_format_strs(str_dict):
    """
    Check for format parameter mismatch
    
    Check that each alternative in each key has
    the same number of format parameters as the key
    """
    error_fewer = 'Key "%s" has fewer parameters than alternative "%s"'
    error_more = 'Key "%s" has more parameters than alternative "%s"'
    errors_held = []
    # scan dictionary for missmatches
    for key, str_list in str_dict.iteritems():
        key_params = count_fmt_params(key)
        for alt_fmt_str in str_list:
            alt_params = count_fmt_params(alt_fmt_str)
            if key_params < alt_params:
                errors_held.append(error_fewer % (key, alt_fmt_str))
            elif key_params > alt_params:
                errors_held.append(error_more % (key, alt_fmt_str))
    if errors_held:
        # prepare and send an exception with all the errors
        e = ParameterMissmatchError("Parameter Missmatch(es)")
        e.errors = errors_held
        raise e


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
            check_format_strs(files_dict[filename])
            print "PASS: %s" % (filename)
        except IOError as e:
            raise SystemExit(e)
        except ValueError as e:
            exceptions[filename] = e
            print >> sys.stderr, "FAIL: %s -- %s" % (filename, e)
        except ParameterMissmatchError as e:
            exceptions[filename] = e
            print >> sys.stderr, "MISS: %s -- %s" % (filename, e)
            for err in e.errors:
                print >> sys.stderr, "\t%s" % err
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
