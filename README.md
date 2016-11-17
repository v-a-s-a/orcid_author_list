# orcid_author_list
Generate an RTF formatted author list from a set of ORCIDs. Currently, there are a few mappings coded into the program that convert certain institution names to their canonical reference.


## Installation
```
pip install git+https://github.com/vtrubets/orcid_author_list.git
```


## Usage
Installation makes `orcid_author_list.py` available as a command line script. 
```
$ orcid_author_list.py --input tests/test_orcids.txt --out test_author_list.rtf
```

This generates an RTF formatted file `test_author_list.rtf` containing the author list.

