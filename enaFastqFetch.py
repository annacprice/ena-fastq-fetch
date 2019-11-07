#!/usr/bin/env python3

import argparse
from xmlparser import getXML, parseXMLgetFTP, parseFTPgetFASTQ
from reportwriter import writeReport

def main():
    parser = argparse.ArgumentParser()
    parser.set_defaults(method=getXML)
    parser.add_argument("-s", "--search-term", dest="search", required=True, \
                        help = "term you wish to search for, e.g. Mycobacterium, 1763, SRR5188398, SRX2504319, PRJNA360902, SELEX")
    parser.add_argument("-d", "--data-type", dest="dataType", required=True, \
                        help = "datatype you wish to search for, e.g. run, study, experiment, sample")
    parser.add_argument("-n", "--num-runs", dest="numRuns", \
                        help = "number of runs you wish to download")
    parser.add_argument("-r", "--report-file", dest="reportWrite", action="store_true", \
                        help = "generate a report file")
    args = parser.parse_args() 
    args.method(**vars(args))

    dataType = args.dataType
    numRuns = args.numRuns
    reportWrite = args.reportWrite
    
    parseXMLgetFTP('ena.xml', dataType, numRuns)
    seqType = parseFTPgetFASTQ('fastq.txt')

    if reportWrite:
        writeReport('ena.xml', dataType, numRuns, seqType)

if __name__ == "__main__":
    main()
