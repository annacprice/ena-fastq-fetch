# ena-fastq-fetch
enaFastqFetch can be used to query the ENA for different types of data and bulk download the associated fastq files.

CAUTION: Please be aware you may be downloading very large datasets. Before downloading the fastqs, the program will print to the terminal the total size of the files to be downloaded.

## **Requirements**

enaFastqFetch requires python 3.x

The following python packages are prerequisites:
- requests

## **Usage**
```
usage: enaFastqFetch.py [-h] -s SEARCH -d DATATYPE

optional arguments:
-h, --help            show this help message and exit
-s SEARCH, --search-term SEARCH
                      term you wish to search for, e.g. Mycobacterium, 1763,
                      SRR5188398, SRX2504319, PRJNA360902, SELEX
-d DATATYPE, --data-type DATATYPE
                      datatype you wish to search for, e.g. run, study,
                      experiment
```
## **Examples of using the accession ID to download**
E.g. to download the fastq associated with the run SRR5188398:
```
python enaFastqFetch.py -s SRR5188398 -d run
```
E.g. to download all of the fastqs associated with the study PRJNA360902:
```
python enaFastqFetch.py -s PRJNA360902 -d study
```
E.g. to download all of the fastqs associated with the experiment SRX2504319:
```
python enaFastqFetch.py -s SRX2504319 -d experiment
```
## **Examples of using the taxonomic ID to download**
E.g. to download all the runs found for the taxon 47839:
```
python enaFastqFetch.py -s 47839 -d run
```
## **Examples of using free text search to download**
E.g. to download selex studies:
```
python enaFastqFetch.py -s "SELEX" -d study
```


