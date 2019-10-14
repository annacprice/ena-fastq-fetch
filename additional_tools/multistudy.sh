#!/bin/bash

# This script can be used to download and organise the data for an input list of studies

while read x
do 
docker run -v $(pwd)/data:/data --rm enafastqfetch -s $x -d READ_STUDY -n 1
mkdir $(pwd)/$x
mv $(pwd)/data/* $(pwd)/$x
done < example_study_list.txt 


