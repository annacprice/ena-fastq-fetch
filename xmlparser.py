#!/usr/bin/env python3

import requests

def getXML(search, dataType, **kwargs):
    # download an xml file for the specified search terms	

    # build the url for the query and download the xml file
    if not any(charac.isdigit() for charac in search):
        if dataType == "read_run":
            dataType = "sra-run"
        
        build_url = {"domain": dataType,
                    "query": search
                    }
        response = requests.get("https://www.ebi.ac.uk/ena/browser/api/xml/textsearch", params=build_url)
    else:
        build_url = {"accession": search,
                    "result": dataType
                    }
        response = requests.get("https://www.ebi.ac.uk/ena/browser/api/xml/links/taxon", params=build_url)

    # write to file
    with open('ena.xml', 'wb') as outfile:
        outfile.write(response.content)

