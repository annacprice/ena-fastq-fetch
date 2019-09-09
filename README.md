# ena-fastq-fetch
EnaFastqFetch can be used to query the ENA for different types of data and bulk download the associated fastq files.

CAUTION: Please be aware you may be downloading very large datasets. Before downloading, the program will report the total size of the files to be downloaded and request confirmation.

## **Requirements**

EnaFastqFetch requires python 3.x

The following python packages are prerequisites:
- requests

## **Usage**
```
usage: enaFastqFetch.py [-h] -s SEARCH -d DATATYPE -n NUMBER

optional arguments:
  -h, --help            show this help message and exit
  -s SEARCH, --search-term SEARCH
                        term you wish to search for, e.g. SELEX,
                        Mycobacterium, SRR5188398, PRJNA360902
  -d DATATYPE, --data-type DATATYPE
                        data type you wish to search for, e.g. READ_STUDY,
                        READ_RUN
  -n NUMBER, --number-download NUMBER
                        number of studies/reads you wish to download
```
## **Examples**
E.g. to download 3 selex studies:
```
python enaFastqFetch.py  -s SELEX -d READ_STUDY  -n 3
```
E.g. to download an individual study, for example study PRJNA360902:
```
python enaFastqFetch.py  -s PRJNA360902  -d READ_STUDY  -n 1
```
E.g. to download an individual run, for example run SRR5188398:
```
python enaFastqFetch.py  -s SRR5188398 -d READ_RUN  -n 1
```
E.g. to download 10 mycobacterium tuberculosis runs:
```
python enaFastqFetch.py -s "mycobacterium tuberculosis" -d READ_RUN -n 10
```
