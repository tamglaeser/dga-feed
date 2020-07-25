## Bambenek Feeds

A python program for pulling down and parsing the information from the Bambenek Consulting High-Confidence C2 All Indicator Feed found 
[here](https://osint.bambenekconsulting.com/feeds/) in the top table. This is the master feed of all current known, active and non-sinkholed C&C domains using DGAs.
The data is structured in the following manner:
- *domain*: the active non-sinkholed C&C domain that uses DGAS
- *ip*: corresponding ip address
- *nsname*: domain names of the autoritative nameserver (DNS) for the given DGA domain
- *nsip*: corresponding ip addresses
- *description*
- *manpage*

The program is made up of three functions which can be called by a menu: 1 to pull down all the information, 2 to pull down only the domain names, and 3 to pull down the domains and name server ips all in an array format; with this information, the domain names could be blacklisted and the malware and attacker potentially identified.

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
