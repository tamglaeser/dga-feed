import urllib.request
from urllib.error import HTTPError, URLError

# function to pull out all the information on the C&C domains using DGAs
# $domain, $ip, $nsname, $nsip, $description, $manpage
def pull():

    print(complete)


# function to pull out only all the C&C domains using DGAs
# -- could be used to to block them / put them on a blacklist
def only_domain():

    dms = []  # array to be filled w all the C&C domains on the page

    for line in complete:
        dms.append(line[0])

    print(dms)


# function to pull out C&C domains and name server ips
# -- could be used to find malware and attacker
# find malware : see who is querying any of those ns ips for that specific C&C domain -- could be malware
# find attacker : find who registered that domain --
# look at outed log to see who registered the C&C domain (which ip -- cld be ip of attacker)
def domains_nsips():

    together = []  # array containing all pairs (C&C domain, nsips)

    for line in complete:
        dm_nsips = [line[0], line[3]]  # [C&C domain, nsips] array
        together.append(dm_nsips)

    print(together)


# main
complete = []  # array containing all information on page


def main():
    url = "https://osint.bambenekconsulting.com/feeds/c2-masterlist-high.txt"  # data page

    try:
        file = urllib.request.urlopen(url)
    except HTTPError as e:
        print('The server couldn\'t fulfill the request. URL might be wrong / not exist anymore')
        print('Error code: ', e.code)
        return
    except URLError as e:
        print('Cannot reach the server. May have lost access to the Internet')
        print('Reason: ', e.reason)
        return

    for line in file:
        decoded_line = line.decode("utf-8")

        if decoded_line[0] != '#':  # if past the beggining comments
            parts = decoded_line.split(',')

            domain = parts[0]
            ip = parts[1]
            ns_host = parts[2].split('|')
            ns_ip = parts[3].split('|')
            description = parts[4]
            manpage = parts[5]

            each = [domain, ip, ns_host, ns_ip, description, manpage]  # array for each line of info
            complete.append(each)
    ans = True

    while ans:
        print("""
        1.List all information on active and non-sinkholed C&C domains using DGAs
        2.List only the domains of active and non-sinkholed C&C domains using DGAS -- to block or blacklist
        3.List the domains of active and non-sinkholed C&C domains using DGAs AND autoritative DNS names for the given DGA domain -- to find malware and attacker
        4.Exit/Quit
        """)

        ans = input("What would you like to do? ")
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


if __name__ == '__main__':
    main()
