#!/usr/bin/env python3

import sys
import os
import requests
import re
import argparse
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import fromstring, ElementTree
import urllib.request
import fileinput

def getXML(search, dataType, number, **kwargs):
    # download an xml file for the specified search terms	

    # build the url for the query and download the xml file
    build_url = {"query": search,
                 "result": dataType,
                 "offset": "0",
                 "length": number,
                 "download": "xml",
                 "display": "xml"
                 }
    
    response = requests.get("https://www.ebi.ac.uk/ena/data/search", params=build_url)

    # write to file
    with open('ena.xml', 'wb') as outfile:
        outfile.write(response.content)

def parseXMLgetFTP(xmlfile, dataType):
    # parse the xml file for http links which contain information on the fastq files
    # open the http links and write the result to file

    # create element tree object
    tree = ET.parse(xmlfile)
    # get root element
    root = tree.getroot()
    
    httplinks = []
    # iterate xml file for http links
    for item in root.iter("ID"):
        if item.text.startswith("http://") and item.text.endswith("fastq_bytes"):
           httplinks.append(item.text)
    
    # fetch http data and write to file
    with open('fastq.txt', 'wb') as outfile:
        for url in httplinks:
            response = requests.get(url)
            outfile.write(response.content)

    # gather info for report file
    accessID = []
    title = []
    enaURL = []

    if dataType == "READ_RUN":
    	for item in root.iterfind("RUN/IDENTIFIERS/PRIMARY_ID"):
            accessID.append(item.text)
            for item in root.iter("TITLE"):
                title.append(item.text)

    if dataType == "READ_STUDY":
    	for item in root.iterfind("STUDY/IDENTIFIERS/PRIMARY_ID"):
            accessID.append(item.text)
            for item in root.iter("STUDY_TITLE"):
                title.append(item.text)

    if dataType == "READ_EXPERIMENT":
        for item in root.iterfind("EXPERIMENT/IDENTIFIERS/PRIMARY_ID"):
            accessID.append(item.text)
            for item in root.iter("TITLE"):
                title.append(item.text)
    
    for item in accessID:
        enaURL.append("https://www.ebi.ac.uk/ena/data/view/{0}".format(item))

    return accessID, title, enaURL

def parseFTPgetFASTQ(ftpinfo):
    # parse the txt file with the fastq info for the ftp links and download
        
    # use regex to compile ftp links
    regexFTP = re.compile("ftp.")
    # use regex to compile filesizes
    regexSize = re.compile(r"\d*;\d*|\d")
    
    # gather info for report file
    fileSize = []
    seqType = []
    
    with open(ftpinfo, 'r') as infile:
        # collate all the filesizes
        for line in infile:
            try:
            	linesplit = line.split()[3]
            except IndexError:
                linesplit = "null"
            if regexSize.match(linesplit):
                for elem in linesplit.split(";", 2):
                    fileSize.append(elem)
                        
        # sum total filesizes
        add = [int(x) for x in fileSize]
        tot = sum(add)/10**9
        print("You are about to download " + str(round(tot, 2)) +  " GB of files")
        sys.stdout.flush()

    with open(ftpinfo, 'r') as infile:
        for line in infile:
            linesplit = line.split()[1]
            if regexFTP.match(linesplit):
                # check for paired fastq files
                if len(linesplit.split(";", 2)) >= 2:
                    seqType.append("PAIRED")
                else:
                    seqType.append("SINGLE")
                for elem in linesplit.split(";", 2):
                    filename = elem[elem.rfind("/")+1:]
                    ftplink = "ftp://" + elem
                    urllib.request.urlretrieve(ftplink, filename)

    return seqType

def writeReport(accessID, title, enaURL, seqType):
    # write report file
    with open('report.txt', 'w') as outfile:
        for item in zip(accessID, title, enaURL, seqType):
            outfile.write("{0}\t{1}\t{2}\t{3}\n".format(item[0], item[1], item[2], item[3]))

def studyBreakdown(ftpinfo):
    # extract information for report on each run in a study

    # use regex to compile run accessions
    regexSRR = re.compile("SRR|ERR|DRR")  
  
    # gather info for study report
    runAccess = []
    runTitle = []
    
    # get accession for each run
    with open(ftpinfo, 'r') as infile:
        for line in infile:
            linesplit = line.split()[0]
            if regexSRR.match(linesplit):
               runAccess.append(linesplit)

    # get xml for each run
    for elem in runAccess:
        build_url = {"query": elem,
                     "result": "READ_RUN",
                     "offset": "0",
                     "download": "xml",
                     "display": "xml"
                     }

        response = requests.get("https://www.ebi.ac.uk/ena/data/search", params=build_url)

        # create element tree object
        tree = ElementTree(fromstring(response.content))
        # get root element
        root = tree.getroot()

        for item in root.iter("TITLE"):
            runTitle.append(item.text)

    # write study report file
    with open('studyBreakdown.txt', 'w') as outfile:
        for item in zip(runAccess, runTitle):
            outfile.write("{0}\t{1}\n".format(item[0], item[1]))

def main():
    parser = argparse.ArgumentParser()
    parser.set_defaults(method=getXML)
    parser.add_argument("-s", "--search-term", dest="search", required=True, \
                        help = "term you wish to search for, e.g. SELEX, Mycobacterium, SRR5188398, SRX2504319, PRJNA360902")
    parser.add_argument("-d", "--data-type", dest="dataType", required=True, \
                        help = "data type you wish to search for, e.g. READ_RUN, READ_EXPERIMENT, READ_STUDY")
    parser.add_argument("-n", "--number-download", dest="number", required=True, \
                        help = "number of runs/experiments/studies you wish to download")
    args = parser.parse_args() 
    args.method(**vars(args))
    dataType = args.dataType
	
    accessID, title, enaURL = parseXMLgetFTP('ena.xml', dataType)
    seqType = parseFTPgetFASTQ('fastq.txt')

    writeReport(accessID, title, enaURL, seqType)

    if dataType == "READ_STUDY":
        studyBreakdown('fastq.txt')

if __name__ == "__main__":
    main()
