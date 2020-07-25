# Bambenek Feeds

A python program for pulling down and parsing the information from the Bambenek Consulting High-Confidence C2 All Indicator Feed found 
[here](https://osint.bambenekconsulting.com/feeds/) in the top table. This is the master feed of all current known, active and non-sinkholed C&C domains using DGAs.
The data is presented in the following manner, $domain, $ip, $nsname, $nsip, $description, and $manpage, with $domain representing the active non-sinkholed C&C domain
that uses DGAs, $ip the corresponding address, and $nsname and $nsip the autoritative nameserver (DNS) for the given DGA domain. The program is made up of three 
functions which can be called by a menu: 1 to pull down all the information, 2 to pull down only the domain names, and 3 to pull down the domains and name server ips
all in the format of an array; with this information, the domain names could be blacklisted and the malware and attacker potentially identified.

## Getting Started

The only prerequisite to running this program is having Python 3 which one can download [here](https://www.python.org/downloads/). Next, simply run 
```python3 c2_all_indicator.py``` 
to get the file running on your local server.
