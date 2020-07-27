#### Why that feed? What did you find interesting about the information you pulled out?

Of all the feeds, the High-Confidence C2 All Indicator Feed seemed to reference the highest number of family-specific feeds and have all the important information about them as well. It still has some family-specific feeds missing (Banjori, Matsnu, Nymaim, Pixd, Pykspa, part of Ramnit, Simda, Suppobox, Virut)
and has an extra domain from Tinba, however I expect that this is simply due to it not being completely up-to-date/synced. I also thought this feed would be helpful since it contains all the current C&C domains using DGAs which one could then easily block.
 
I specifically listed out the C&C domain names in the [only_domain()](./c2_all_indicator.py#L13) function so that these could all be added to a blacklist and blocked.

In the [domains_nsips()](./c2_all_indicator.py#L25) function, I listed the C&C domains and the corresponding name server IPs so that one could see if the DNS had requests for those domains and could thereby locate the malware and let the owner of the computer know their computer has a virus AND/OR see who registered that domain name thereby finding the attacker.

My other functions allow the user to retrieve specific information, such as all the information concerning a certain C&C server or a sertain DGA family.
