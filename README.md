## DGA Feeds

A python program for pulling down and parsing the information from the Bambenek Consulting High-Confidence C2 All Indicator Feed found 
[here](https://osint.bambenekconsulting.com/feeds/) in the top table; since the website is subject to change or withdraw permissions, I have copied the data to the c2-masterlist-high.txt file. This is the master feed of all current known, active and non-sinkholed C&C domains using DGAs.
The data is structured in the following manner:
- *domain*: the active non-sinkholed C&C domain that uses DGAs
- *ip*: corresponding IP address
- *nsname*: domain names of the autoritative nameserver (DNS) for the given DGA domain
- *nsip*: corresponding IP addresses
- *description*
- *manpage*

The program is made up of several functions which can be called by the command line.

#### Prerequisites

This project requires Python 3.

#### Get the Sources

```
$ git clone https://github.com/tamglaeser/dga-feed.git
$ cd ./dga-feed
```

#### Run Program 

To see all options for running program, run
```
$ python3 c2_all_indicator.py -h
``` 

#### Motivation

Please see [here](./motivation.md) for more on my motivation, why I picked the particular intel feed from Bambenek Consulting, and what applications this program could have.
