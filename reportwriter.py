#!/usr/bin/env python3

import xml.etree.ElementTree as ET

def writeReport(xmlfile, dataType, numRuns):
    
    # create element tree object
    tree = ET.parse(xmlfile)
    # get root element
    root = tree.getroot()
    
    # gather info for report file
    accessID = []
    title = []

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

    if numRuns:
        num = int(numRuns)
        accessID = accessID[:num]
        title = title[:num]

    # write report file
    with open('report.txt', 'w') as outfile:
        for item in zip(accessID, title):
            outfile.write("{0}\t{1}\n".format(item[0], item[1]))
