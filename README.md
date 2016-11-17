# orcid_author_list
Generate an RTF formatted author list from a set of ORCIDs. Currently, there are a few mappings coded into the program that convert certain institution names to their canonical reference.


## Installation
```
pip install git+https://github.com/vtrubets/orcid_author_list.git
```
This installs orcid_author_list and its dependencies. It makes `orcid_author_list.py` callable from the command line. If you don't want to pollute your current python environment, it is recommended that you use a `virtualenv`, `conda` env or something similar.

## Usage
Installation makes `orcid_author_list.py` available as a command line script. 
```
$ orcid_author_list.py --input tests/test_orcids.txt --out test_author_list.rtf
```
This generates an RTF formatted file `test_author_list.rtf` containing the author list.

