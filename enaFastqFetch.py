#!/usr/bin/env python3

import argparse
from xmlparser import getXML, parseXMLgetFTP, parseFTPgetFASTQ

def main():
    parser = argparse.ArgumentParser()
    parser.set_defaults(method=getXML)
    parser.add_argument("-s", "--search-term", dest="search", required=True, \
                        help = "term you wish to search for, e.g. Mycobacterium, 1763, SRR5188398, SRX2504319, PRJNA360902, SELEX")
    parser.add_argument("-d", "--data-type", dest="dataType", required=True, \
                        help = "datatype you wish to search for, e.g. run, study, experiment")
    parser.add_argument("-n", "--num-runs", dest="numRuns",\
                        help = "number of runs you wish to download")
    args = parser.parse_args() 
    args.method(**vars(args))

    dataType = args.dataType
    numRuns = args.numRuns
    
    parseXMLgetFTP('ena.xml', dataType, numRuns)
    parseFTPgetFASTQ('fastq.txt')

if __name__ == "__main__":
    main()
