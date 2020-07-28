import urllib.request
from urllib.error import HTTPError, URLError
import sys
import argparse



# function to list out all the information on the C&C servers using DGAs
# dictionary format: {ip: [domain, [nsnames], [nsips], description, manpage]
# id can either be none, a specific DGA family, or a specific C&C IP to get info on
# dict is either dga for a specific DGA fam, otherwise complete
def pull(dict, id=None):
    if id is not None:
        print(*dict[id.lower()], sep="\n")

    else:
        print("Format: (ip, [domain, nsdomains, nsips, description, manpage])")
        print(*dict.items(), sep='\n')


# function to pull out only all the C&C domains using DGAs
# -- could be used to to block them / put them on a blacklist
# id can either be none, a specific DGA family, or a specific C&C IP to get info on
# dict is either dga for a specific DGA fam, otherwise complete
def only_domain(dict, id=None):
    dms = []  # array to be filled w all the C&C domains on the page  # for memory
    if id is not None:
        for val in dict[id.lower()]:
            if val not in dms:
                print(val[0])
                dms.append(val[0])

    else:
        for val in dict.values():
            for each in val:  # for each value for that key
                if each[0] not in dms:
                    print(each[0])  # for nice output formatting
                    dms.append(each[0])


# function to pull out C&C domains and name server ips
# -- could be used to find malware and attacker
# find malware : see who is querying any of those ns ips for that specific C&C domain -- could be malware
# find attacker : find who registered that domain --
# look at outed log to see who registered the C&C domain (which ip -- cld be ip of attacker)
# id can either be none, a specific DGA family, or a specific C&C IP to get info on
# dict is either dga for a specific DGA fam, otherwise complete
def domains_nsips(dict, id=None):

    together = {}  # dictionary containing key C&C domain and value ns ips  # for memory

    if id is not None:
        if isinstance(id, str):  #is dga fam
            for val in dict[id.lower()]:
                if val[0] not in together.keys():
                    together[val[0]] = val[3]
                    print(val[0], val[3])
        else:  # ip
            for val in dict[id]:
                if val[0] not in together.keys():
                    together[val[0]] = val[2]
                    print(val[0], val[2])
    else:
        for val in dict.values():
            for each in val:  # for each value for that key
                if each[0] not in together.keys():
                    together[each[0]] = each[2]  # key = each[0] = C&C domain  # value = each[2] = ns ips for that domain
                    print(each[0], each[2])


def main(argv):
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

            if '|' in parts[1]:  # if has multiple C&C IPs
                for x in parts[1].split('|'):
                    if x not in complete.keys():
                        complete[x] = [[parts[0], parts[2].split('|'), parts[3].split('|'), parts[4], parts[5]]]  # complete[ip] = [domain, ns_host, ns_ip, description, manpage] # dictionary
                    else:  # if ip already in dictionary, append new values
                        complete[x].append([parts[0], parts[2].split('|'), parts[3].split('|'), parts[4], parts[5]])

            elif parts[1] not in complete.keys():  # if ip not already in dictionary, add
                complete[parts[1]] = [[parts[0], parts[2].split('|'), parts[3].split('|'), parts[4], parts[5]]]  # complete[ip] = [domain, ns_host, ns_ip, description, manpage] # dictionary
            else:  # if ip already in dictionary, append new values
                complete[parts[1]].append([parts[0], parts[2].split('|'), parts[3].split('|'), parts[4], parts[5]])

            name = parts[5].split('/')[4].split('.')[0]  # get name of DGA family
            if name not in dga.keys():
                dga[name] = [[parts[0], parts[1], parts[2].split('|'), parts[3].split('|'), parts[4], parts[5]]]
            else:
                dga[name].append([parts[0], parts[1], parts[2].split('|'), parts[3].split('|'), parts[4], parts[5]])

    # Command Line setup  # python3 c22.py --l  # python3 c22.py --c CHOICE --i ID  # python3 c22.py --c ID
    parser = argparse.ArgumentParser(description='A program to pull information about different C&C servers')

    parser.add_argument("-l", "--list", action="store_true", help="Lists all possible DGA families")
    parser.add_argument("-c", "--choice", choices=[1,2,3], type=int, help="denotes the user's choice of either\n"
                                                               " - 1.Listing all information in the following format (ip: [domain, [nsname], [nsip], description, manpage]\n"
                                                               " - 2.Listing only the C&C server domains\n"
                                                               " - 3.Listing the C&C server domains and corresponding DNS IP addresses")
    parser.add_argument("-i", "--id", help="represents which specific DGA family or C&C IP the user would like to learn about")

    args = parser.parse_args()
    list = args.list
    choice = args.choice
    id = args.id

    if list:  # if --l  # to list all possible DGA fams
        for key in dga.keys():
            print(key)
    else:
        if choice == 1:  # to pull all info
            if id in dga.keys():  # if want specific DGA fam info
                pull(dga, id)
            elif id in complete.keys():  # if want specific IP info
                pull(complete, id)
            elif id == None:  # if want all info
                pull(complete)
            else:  # user entered something wrong for id
                print("ID not found. Please enter a valid DGA family or C&C IP.")
        elif choice == 2:  # to list only domains
            if id in dga.keys():
                only_domain(dga, id)
            elif id in complete.keys():
                only_domain(complete, id)
            elif id == None:
                only_domain(complete)
            else:  # user entered something wrong for id
                print("ID not found. Please enter a valid DGA family or C&C IP.")
        elif choice == 3:  # to list domains and corresponding DNS IPs
            if id in dga.keys():
                domains_nsips(dga, id)
            elif id in complete.keys():
                domains_nsips(complete, id)
            elif id == None:
                domains_nsips(complete)
            else:  # user entered something wrong for id
                print("ID not found. Please enter a valid DGA family or C&C IP.")
        else:  # didn't enter a CHOICE or --l
            print("Please enter a choice. 1 for all information, 2 for only C&C domains, and 3 for C&C domains and DNS Ips")


if __name__ == '__main__':  # to easily run main from terminal
    main(sys.argv)
