## Bambenek Feeds

A python program for pulling down and parsing the information from the Bambenek Consulting High-Confidence C2 All Indicator Feed found 
[here](https://osint.bambenekconsulting.com/feeds/) in the top table. This is the master feed of all current known, active and non-sinkholed C&C domains using DGAs.
The data is structured in the following manner:
- *domain*: the active non-sinkholed C&C domain that uses DGAs
- *ip*: corresponding IP address
- *nsname*: domain names of the autoritative nameserver (DNS) for the given DGA domain
- *nsip*: corresponding IP addresses
- *description*
- *manpage*

The program is made up of several functions which can be called by a menu: 1 to list all the information, 2 to only list the domain names (to potentially block), 3 to list the domains and name server IPs (to potentially find malware and the attacker), 4 to list all the information of a certain C&C IP (to block that server specifically), and 5 to list all the information on the C&Cs of a specific DGA family; with this information, the domain names could be blacklisted and the malware and attacker potentially identified.

#### Prerequisites

This project requires Python 3.

#### Get the Sources

```
$ git clone https://github.com/tamglaeser/threatquotient.git
$ cd ./threatquotient
```

#### Run Program 
```
$ python3 c2_all_indicator.py
``` 

#### Motivation

Please see [here](./motivation.md) for more on my motivation, why I picked the particular intel feed from Bambenek Consulting, and what applications this program
could have.
