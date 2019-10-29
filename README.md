# ena-fastq-fetch
enaFastqFetch can be used to query the ENA for different types of data and bulk download the associated fastq files. Upon completion of the download several report files are generated providing information on the downloaded data.

CAUTION: Please be aware you may be downloading very large datasets. Before downloading, the program will print to the terminal the total size of the files to be downloaded.

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
                      term you wish to search for, e.g. Mycobacterium, 1773
-d DATATYPE, --data-type DATATYPE
                      data type you wish to search for, e.g. read run
```

