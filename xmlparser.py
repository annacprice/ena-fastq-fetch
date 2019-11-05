#!/usr/bin/env python3

import sys
import requests
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import fromstring, ElementTree
import re
import urllib.request

def getXML(search, dataType, **kwargs):
    # download an xml file for the specified search terms

    # if search query is entirely numeric, download by taxon
    if all(charac.isdigit() for charac in search):
        # ammend datatype for api
        if dataType == "run":
            dataType = "read_run"
        elif dataType == "study":
            dataType = "read_study"
        elif dataType == "experiment":
            dataType = "read_experiment"
        else:
            print ("Datatype is not recognised. Supported values are: run, study or experiment")
            exit()
        # build the url for the query and download the xml file
        build_url = {"accession": search,
                    "result": dataType
                    }
        response = requests.get("https://www.ebi.ac.uk/ena/browser/api/xml/links/taxon", params=build_url)
    # else use free text search
    else:
        # ammend datatype for api
        if dataType == "run":
            dataType = "sra-run"
        elif dataType == "study":
            dataType = "sra-study"
        elif dataType == "experiment":
            dataType = "sra-experiment"
        else:
            print ("Datatype is not recognised. Supported values are: run, study or experiment")
            exit()
        # build the url for the query and download the xml file
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
    
    # collate filesizes, filenamess and ftplinks
    fileSize = []
    filename = []
    ftplink = []
    
    with open(ftpinfo, 'r') as infile:
        for line in infile:
            # collate all the filesizes
            try:
                linesplit = line.split()[3]
            except IndexError:
                linesplit = "null"
            if regexSize.match(linesplit):
            # check for paired fastq files
                for elem in linesplit.split(";", 2):
                    fileSize.append(elem)
            # collate filenames and ftplinks
            try:
                linesplit = line.split()[1]
            except IndexError:
                linesplit = "null"
            if regexFTP.match(linesplit):
            # check for paired fastq files
                for elem in linesplit.split(";", 2):
                    filename.append(elem[elem.rfind("/")+1:])
                    ftplink.append("ftp://" + elem)
                        
    # sum total filesizes and print to terminal
    add = [int(x) for x in fileSize]
    tot = sum(add)/10**9
    print("You are about to download " + str(round(tot, 2)) +  " GB of files")
    sys.stdout.flush()

    # fetch fastqs
    for link, name in zip(ftplink, filename):
        urllib.request.urlretrieve(link, name)
