#!/usr/bin/env python3

import argparse
from xmlparser import getXML


def main():
    parser = argparse.ArgumentParser()
    parser.set_defaults(method=getXML)
    parser.add_argument("-s", "--search-term", dest="search", required=True, \
                        help = "term you wish to search for, e.g. Mycobacterium, 1773")
    parser.add_argument("-d", "--data-type", dest="dataType", required=True, \
                        help = "data type you wish to search for, e.g. read run")
    args = parser.parse_args() 
    args.method(**vars(args))



if __name__ == "__main__":
    main()
