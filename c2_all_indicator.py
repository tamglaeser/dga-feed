import urllib.request

def pull():

    url = "https://osint.bambenekconsulting.com/feeds/c2-masterlist-high.txt" #data page
    file = urllib.request.urlopen(url)

    complete = []
    domain = ip = description = manpage = ""
    ns_host = ns_ip = []

    for line in file:
        decoded_line = line.decode("utf-8")

        if decoded_line[0] != '#':
            parts = decoded_line.split(',')


            domain = parts[0]
            ip = parts[1]
            ns_host = parts[2].split('|')  # add array of new domains for each seed w/in new_domains array
            ns_ip = parts[3].split('|') # add array of new ip addresses for each seed w/in new_ips array
            description = parts[4]
            manpage = parts[5]

            each = [] # array for each line
            each.append(domain)
            each.append(ip)
            each.append(ns_host)
            each.append(ns_ip)
            each.append(description)
            each.append(manpage)
            complete.append(each) # complete array with whole feed's data

    print(complete)

#function to pull out only all the C&C domains using DGAs to block them
def only_domain():
    url = "https://osint.bambenekconsulting.com/feeds/c2-masterlist-high.txt" #data page
    file = urllib.request.urlopen(url)

    dms = []

    for line in file:
        decoded_line = line.decode("utf-8")

        if decoded_line[0] != '#':
            parts = decoded_line.split(',')
            dms.append(parts[0])

    print(dms)

# function to pull out C&C domains and name server ips to find malware and attacker
# find malware : see who is asking any of those nsips for that specific C&C domain -- could be malware
# find attacker : find who registered that domain
def domains_nsips():
    url = "https://osint.bambenekconsulting.com/feeds/c2-masterlist-high.txt" #data page
    file = urllib.request.urlopen(url)

    together = []

    for line in file:
        decoded_line = line.decode("utf-8")

        if decoded_line[0] != '#':
            dm_nsips = []
            parts = decoded_line.split(',')
            dm_nsips.append(parts[0])
            dm_nsips.append(parts[3].split('|'))
            together.append(dm_nsips)

    print(together)



ans = True

while ans:
    print ("""
    1.Pull all information on active and non-sinkholed C&C domains using DGAs
    2.Pull only domains of active and non-sinkholed C&C domains using DGAS -- to block
    3.Pull domains of active and non-sinkholed C&C domains using DGAs and autoritative DNS names for the given DGA domain -- to find malware and attacker
    4.Exit/Quit
    """)

    ans=input("What would you like to do? ")
    if ans == "1":
        pull()
    elif ans == "2":
        only_domain()
    elif ans == "3":
        domains_nsips()
    elif ans == "4":
        print("\n Goodbye")
        ans = False
    else:
        print("\n Not Valid Choice, try again")
