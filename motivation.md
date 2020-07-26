#### Why that feed? What did you find interesting about the information you pulled out?

Of all the feeds, the High-Confidence C2 All Indicator Feed seemed to have referenced the highest
number of family-specific feeds and have all the important information about them as well. It still
had some family-specific feeds missing (Banjori, Matsnu, Nymaim, Pixd, Pykspa, 9 from Ramnit, Simda, Suppobox, Virut)
and had an extra domain from Tinba, however I expect that this is simply due to it not being completely
up-to-date/synced. I also thought this feed would be helpful since it contains all the current C&C domains using DGAs which one could easily block.

I specifically pulled out the C&C domain names in the [only_domain()](./c2_all_indicator.py#L13) function so that these could all be added to a blacklist and blocked.

In the [domains_nsips()](./c2_all_indicator.py#L28) function, I pulled out the C&C domains and the name server ips so that one could see if the DNS had requests for those domains and
could thereby locate the malware and let the owner of the computer know their computer has a virus OR see who registered that domain name thereby finding
the attacker.
