#!/usr/bin/env python3

import sys
import os
import requests
import re
import argparse
import xml.etree.ElementTree as ET
import urllib.request


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
    outfile = open('ena.xml', 'wb')
    outfile.write(response.content)
    outfile.close()

def parseXMLgetFTP(xmlfile):
    # parse the xml file for http links which contain information on the fastq files
    # open the http links and write the result to file

    # create element tree object
    tree = ET.parse(xmlfile)
    # get root element
    root = tree.getroot()
    
    # initialise httplinks
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

def parseFTPgetFASTQ(ftpinfo):
    # parse the txt file with the fastq info for the ftp links and download
        
    # use regex to compile ftp links
    regexFTP = re.compile("ftp.")
    # use regex to compile filesizes
    regexSize = re.compile(r"\d*;\d*|\d")

    Size = []
    with open(ftpinfo, 'r') as infile:
        # collate all the filesizes
        for line in infile:
            linesplit = line.split()[3]
            if regexSize.match(linesplit):
                for elem in linesplit.split(";", 1):
                    Size.append(elem)
    
        # sum total filesizes and launch CLI to confirm download
        add = [int(x) for x in Size]
        tot = sum(add)/10**9
        print("You are about to download " + str(round(tot, 2)) +  " GB of files. Do you wish to continue?")
        YesOrNo(answer=None)

    with open(ftpinfo, 'r') as infile:
    # fetch files from ftpserver
        for line in infile:
            linesplit = line.split()[1]
            if regexFTP.match(linesplit):
                # check for paired fastq files
                for elem in linesplit.split(";", 1):
                    filename = elem[elem.rfind("/")+1:]
                    ftplink = "ftp://" + elem
                    urllib.request.urlretrieve(ftplink, filename)

def YesOrNo(answer=None):
    #CLI to check whether user wishes to download files

    yes = ("yes", "y", "ye")
    no = ("no", "n")

    while answer not in (yes, no):
        answer = input().lower()
        if answer in yes:
            answer =yes
            continue
        elif answer in no:
            exit()
        else:
            print("Please enter yes or no:")

def main():
    parser = argparse.ArgumentParser()
    parser.set_defaults(method=getXML)
    parser.add_argument("-s", "--search-term", dest="search", required=True, \
			help = "term you wish to search for, e.g. SELEX, Mycobacterium, SRR5188398, PRJNA360902")
    parser.add_argument("-d", "--data-type", dest="dataType", required=True, \
		        help = "data type you wish to search for, e.g. READ_STUDY, READ_RUN")
    parser.add_argument("-n", "--number-download", dest="number", required=True, \
			help = "number of studies/reads you wish to download")
    args = parser.parse_args() 
    args.method(**vars(args))
	
    parseXMLgetFTP('ena.xml')
    parseFTPgetFASTQ('fastq.txt')

if __name__ == "__main__":
    main()
