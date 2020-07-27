import urllib.request
from urllib.error import HTTPError, URLError


# function to list out all the information on the C&C servers using DGAs
# dictionary format: {ip: [domain, [nsnames], [nsips], description, manpage]
def pull():

    print("Format: (ip, [domain, nsdomains, nsips, description, manpage])")
    print(*complete.items(), sep='\n')


# function to pull out only all the C&C domains using DGAs
# -- could be used to to block them / put them on a blacklist
def only_domain():

    dms = []  # array to be filled w all the C&C domains on the page  # for memory

    for val in complete.values():
        for each in val:  # for each value for that key
            print(each[0])  # for nice output formatting
            dms.append(each[0])


# function to pull out C&C domains and name server ips
# -- could be used to find malware and attacker
# find malware : see who is querying any of those ns ips for that specific C&C domain -- could be malware
# find attacker : find who registered that domain --
# look at outed log to see who registered the C&C domain (which ip -- cld be ip of attacker)
def domains_nsips():

    together = {}  # dictionary containing key C&C domain and value ns ips  # for memory

    for val in complete.values():
        for each in val:  # for each value for that key
            together[each[0]] = each[2]  # key = each[0] = C&C domain  # value = each[2] = ns ips for that domain
            print(each[0], each[2])


# function to list all info of certain C&C server ips
# to block all domains on specific C&C server
def get_info(ip):
    print("Format: [domain, nsdomains, nsips, description, manpage]")
    print(*complete[ip], sep='\n')


# function to list all info of all active non-sinkholed C&C servers of certain DGA family
def get_fam(fam):
    if fam.lower() in dga.keys():
        print(*dga[fam.lower()], sep="\n")
    else:
        print("DGA family not found. See option 6 to list all DGA families.")


def main():
    global complete
    complete = {}  # dictionary containing all information on page  # key=ip
    global dga
    dga = {}  # dictionary containing all information on page organized by dga fam
    url = "https://osint.bambenekconsulting.com/feeds/c2-masterlist-high.txt"  # data page

    try:
        file = urllib.request.urlopen(url)
    except HTTPError as e:
        print('The server couldn\'t fulfill the request. URL might be wrong / not exist anymore')
        print('Error code: ', e.code)
    except URLError as e:
        print('Cannot reach the server. May have lost internet connection')
        print('Reason: ', e.reason)

    for line in file:
        decoded_line = line.decode("utf-8")

        if decoded_line[0] != '#':  # if past the beginning comments
            parts = decoded_line.split(',')

            if parts[1] not in complete.keys():  # if ip not already in dictionary, add
                complete[parts[1]] = [[parts[0], parts[2].split('|'), parts[3].split('|'), parts[4], parts[5]]]  # complete[ip] = [domain, ns_host, ns_ip, description, manpage] # dictionary
            else:  # if ip already in dictionary, append new values
                complete[parts[1]].append([parts[0], parts[2].split('|'), parts[3].split('|'), parts[4], parts[5]])

            name = parts[5].split('/')[4].split('.')[0]
            if name not in dga.keys():
                dga[name] = [[parts[0], parts[1], parts[2].split('|'), parts[3].split('|'), parts[4], parts[5]]]
            else:
                dga[name].append([[parts[0], parts[1], parts[2].split('|'), parts[3].split('|'), parts[4], parts[5]]])
    ans = True

    while ans:
        print("""
        1.List all information on active and non-sinkholed C&C domains using DGAs. Presented in the following format: (ip, [domain, nsnames, nsips, description, manpage])
        2.List only the domains of active and non-sinkholed C&C domains using DGAS -- to block or blacklist
        3.List the domains of active and non-sinkholed C&C domains using DGAs AND the autoritative DNS names for the given DGA domain -- to find malware and attacker
        4.List information of specific C&C IP.
        5.List all information on active non sinkholed C&C domains of specific DGA family.
        6.List all DGA families.
        7.Exit/Quit
        """)

        ans = input("What would you like to do? ")
        if ans == "1":
            pull()
        elif ans == "2":
            only_domain()
        elif ans == "3":
            domains_nsips()
        elif ans == "4":
            ip = input("Which IP? ")
            if ip in complete.keys():
                get_info(ip)
            else:
                print("IP address "+ ip +" not found.")
        elif ans == "5":
            fam = input("Which DGA family? ")
            get_fam(fam)
        elif ans == "6":
            for key in dga.keys():
                print(key)
        elif ans == "7" or ans == "quit" or ans == "exit":
            print("\n Goodbye")
            ans = False
        else:
            print("\n Not Valid Choice, try again")
            ans = True  # otherwise exits program with Enter key


if __name__ == '__main__':
    main()
