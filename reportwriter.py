#!/usr/bin/env python3

import xml.etree.ElementTree as ET

def writeReport(xmlfile, dataType, numRuns, seqType):
    
    # create element tree object
    tree = ET.parse(xmlfile)
    # get root element
    root = tree.getroot()
    
    # gather info for report file
    accessID = []
    title = []
    enaURL = []

    if dataType == "run":
        for item in root.iterfind("RUN/IDENTIFIERS/PRIMARY_ID"):
            accessID.append(item.text)
        for item in root.iter("TITLE"):
            title.append(item.text)
    elif dataType == "study":
        for item in root.iterfind("STUDY/IDENTIFIERS/PRIMARY_ID"):
            accessID.append(item.text)
        for item in root.iter("STUDY_TITLE"):
            title.append(item.text)
    elif dataType == "experiment":
        for item in root.iterfind("EXPERIMENT/IDENTIFIERS/PRIMARY_ID"):
            accessID.append(item.text)
        for item in root.iter("TITLE"):
            title.append(item.text)
    elif dataType == "sample":
        for item in root.iterfind("SAMPLE/IDENTIFIERS/PRIMARY_ID"):
            accessID.append(item.text)
        for item in root.iter("TITLE"):
            title.append(item.text)

    if numRuns:
        num = int(numRuns)
        accessID = accessID[:num]
        title = title[:num]

    for item in accessID:
        enaURL.append("https://www.ebi.ac.uk/ena/browser/view/{0}".format(item))

    # write report file
    with open('report.txt', 'w') as outfile:
        for item in zip(accessID, title, seqType, enaURL):
            outfile.write("{0}\t{1}\t{2}\t{3}\n".format(item[0], item[1], item[2], item[3]))
