# ena-fastq-fetch
enaFastqFetch can be used to query the ENA for different types of data and bulk download the associated fastq files. Upon completion of the download several report files are generated providing information on the downloaded data.

CAUTION: Please be aware you may be downloading very large datasets. Before downloading, the program will print to the terminal the total size of the files to be downloaded.

## **Requirements**

enaFastqFetch requires python 3.x

The following python packages are prerequisites:
- requests

## **Usage**
```
usage: enaFastqFetch.py [-h] -s SEARCH -d DATATYPE -n NUMBER

optional arguments:
  -h, --help            show this help message and exit
  -s SEARCH, --search-term SEARCH
                        term you wish to search for, e.g. SELEX,
                        Mycobacterium, SRR5188398, SRX2504319, PRJNA360902
  -d DATATYPE, --data-type DATATYPE
                        data type you wish to search for, e.g. READ_RUN,
                        READ_EXPERIMENT, READ_STUDY
  -n NUMBER, --number-download NUMBER
                        number of runs/experiments/studies you wish to
                        download
```

## **How EnaFastqFetch works**
enaFastqFetch works by building REST URLs to query the ENA Advanced Search. By providing enaFastqFetch with a search term, datatype, and number of downloads, it will automatically download the fastqs associated with your request. It will also generate useful reports on the data including the accession IDs, the recorded title of the data, links to the data record, and whether the fastqs are single or paired.

### **Search term**
The search term is specified through the -s flag. You can search for data by using its accession ID. Alternatively, you can also search using more generic search terms such as the species name.

### **Datatype**
The datatype is specified through the -d flag. enaFastqFetch supports three datatypes: READ_RUN, READ_EXPERIMENT, and READ_STUDY.

The ENA uses a hierarchical system to define the datatype:
• STUDY (accessions beginning with SRP, ERP, or DRP)
A study defines an overarching investigation. In most cases it's a dataset associated with a publication.
• SAMPLE (accessions beginning with SRS, ERS, or DRS)
A sample is a biological sample which is used in a study.
• EXPERIMENT (accessions beginning with SRX, ERX, or DRX)
An experiment is conducted on a sample. This defines things like the instrument used for sequencing and the library preparation.
• RUN (accessions beginning with SRR, ERR, or DRR)
A run is the actual sequencing reads which are associated with a sample and experiment. I.e. these are the fastq files.

So for example the run [SRR3206414](https://www.ebi.ac.uk/ena/data/view/SRR3206414) is associated with the sample [SRS1318643](https://www.ebi.ac.uk/ena/data/view/SRS1318643) and the experiment [SRX1615315](https://www.ebi.ac.uk/ena/data/view/SRX1615315), and overall it belongs to the study [SRP071047/PRJNA313382](https://www.ebi.ac.uk/ena/data/view/PRJNA313382).

### **Number of downloads **
The maximum number of allowed downloads for your requested search term and datatype is specified through the -n flag. The number of downloads has an upper limit of 100,000. When downloading by accession ID the number of downloads will always be 1.

## **Examples of using the accession ID to download**
E.g. to download the fastq associated with the run SRR3206414:
```
python enaFastqFetch.py -s SRR3206414 -d READ_RUN -n 1
```
E.g. to download all the fastqs associated with the experiment SRX1615315: 
```
python enaFastqFetch.py -s SRX1615315 -d READ_EXPERIMENT -n 1
```
E.g. to download all of the fastqs associated with the study SRP071047:
```
python enaFastqFetch.py -s SRP071047 -d READ_STUDY -n 1
```

## **Examples of using generic search terms to download**
E.g. to download 3 selex studies:
```
python enaFastqFetch.py -s SELEX -d READ_STUDY -n 3
```
E.g. to download 10 mycobacterium tuberculosis runs:
```
python enaFastqFetch.py -s "mycobacterium tuberculosis" -d READ_RUN -n 10
```
