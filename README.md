# Table of Contents
1. [Dependencies](README.md#dependencies)
1. [Method](README.md#method)
1. [Run Instructions](README.md#run-instructions)
1. [Data Corner Case Handling](README.md#data-corner-case-handling)
1. [Note](README.md#note)
--------

This is a project that gathers drug information from prescription data. The finial output consists of a listing of the drugs, their costs, and the number of unique prescriptions. This project is based on the data challenge from Insight.

--------

## Dependencies

1. Python 2.7 or above
2. Python standard library
3. Python modules: NumPy, operator, filecmp, unittest, datetime

## Method

The original data is in text format. The text is parsed and we identify columns representing the first name, the last name, the drug name, and the drug cost. This data is formatted in a table, and we first sort the table by the drug name in ascending order. This will accelerate the following processes as information of each drug is now localized. Next, we identify drug types, and their frequency in the data. We then compute, for each drug, the number of unique prescribers, and the total drug cost. Since the table is sorted and we know the frequency of each drug, we avoid the need to search the whole table for these computations. Finally, the desired information, namely the drug name, number of prescribers, and the total cost, forms a final table. We then sort the table by descending order in cost, and then by ascending order in drug name, as requested.


## Run Instructions

The program can be simply run with

   $ sh run.sh

This will use the input data from /input/. If one wishes to pass different input data to the program, generally one can do

   $ python ./src/pharmacy-counting.py ${PATH-TO-INPUT-DATA} ${PATH-TO-OUTPUT-FILE}

Unit tests can be run by

   $ python src/test_mymodule.py

## Data Corner Case Handling

Several corner cases were considered. They are:

1. Missing data

If the input data has a missing field, such as
```
0001,,JAMES,DRUG1,788
```
, then this line of data will be skipped.

2.  Corrupted data

If the input data has corrupted fields, such as
```
0001,HARDEN,JAMES,DRUG1,gha8
```
, where the cost is not a number, then this line of data will be skipped.

3. Lowercase/uppercase

When counting the number of prescribers, I ignore differences in uppercase and lowercase letters. 'Jordan' is considered the same as 'JORDAN'. Drug names, however, are exactly the same as in the input file. 'DRUG1' is considered different from 'Drug1'.

## Note

The program automatically scans the cost entry of the input data, and finds the largest number of decimal digits. The output cost will follow this decimal convention. For example, if the input data is such:

```
0001,MILLER,REGGIE,DRUG1,10
0002,CURRY,STEPHEN,DRUG1,9.991
0003,THOMPSON,KLAY,DRUG2,76.1
```
Since the maximal number of decimal digits is three (9.991), the output cost will be formatted as:

```
DRUG2,1,76.100
DRUG1,2,19.991
```
