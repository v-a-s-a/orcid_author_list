# ORCID Author List
Generate an Rich Text Format (RTF) file containing an author list from a set of ORCIDs. Additionaly, there are a few mappings coded into the program that convert certain institution names to their canonical reference.

Using ORCID API v1.2_rc7

## Installation
```
$ pip install git+https://github.com/vtrubets/orcid_author_list.git
```
This installs orcid_author_list and its dependencies. It makes `orcid_author_list.py` callable from the command line. If you don't want to pollute your current python environment, it is recommended that you use a `virtualenv`, `conda` env or something similar.

## Usage
Installation makes `orcid_author_list.py` available as a command line script. 
```
$ orcid_author_list.py --input tests/test_orcids.txt --out test_author_list.rtf
```
This generates an RTF formatted file `test_author_list.rtf` containing the author list.

Additionally, there is a "comparison view" that generates a set of spreadsheets to aid in combining and replacing author affiliations. This can be invoked with the added `--comparison-view` flag.

