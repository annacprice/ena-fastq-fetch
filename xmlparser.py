#!/usr/bin/env python3

import sys
import requests
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import fromstring, ElementTree
import re
import urllib.request

def getXML(search, dataType, **kwargs):
    # download an xml file for the specified search terms	

    # build the url for the query and download the xml file
    if all(charac.isdigit() for charac in search):
        build_url = {"accession": search,
                    "result": dataType
                    }
        response = requests.get("https://www.ebi.ac.uk/ena/browser/api/xml/links/taxon", params=build_url)
    else:
        if dataType == "read_run":
            dataType = "sra-run"

        build_url = {"domain": dataType,
                    "query": search
                    }
        response = requests.get("https://www.ebi.ac.uk/ena/browser/api/xml/textsearch", params=build_url)

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

def parseFTPgetFASTQ(ftpinfo):
    # parse the txt file with the fastq info for the ftp links and download
    
    # use regex to compile ftp links
    regexFTP = re.compile("ftp.")
    # use regex to compile filesizes
    regexSize = re.compile(r"\d*;\d*|\d")
    
    # gather info on filesizes and if single/paired sequencing
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


