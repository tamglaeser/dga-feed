import urllib.request
from urllib.error import HTTPError, URLError
import sys
import argparse, textwrap



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
        if id in dga:  #is dga fam
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
    url = "file:///home/tullia/projects/dga-feed/c2-masterlist-high.txt"  # data page

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

    def required_length(nmin,nmax):
        class RequiredLength(argparse.Action):
            def __call__(self, parser, args, values, option_string=None):
                if not nmin<=len(values)<=nmax:
                    msg='argument "{f}" requires between {nmin} and {nmax} arguments'.format(
                        f=self.dest,nmin=nmin,nmax=nmax)
                    raise argparse.ArgumentTypeError(msg)
                setattr(args, self.dest, values)
        return RequiredLength

    parser=argparse.ArgumentParser(description='program for listing information from C&C servers',
                                   usage='use "python %(prog)s --help" for more information',
                                   formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-d", "--dga", action="store_true", help="Lists all possible DGA families")
    parser.add_argument('-l', "--list", nargs='+', action=required_length(1, 2), help=textwrap.dedent('''\
    1st parameter -- options:
        1 - to list all information in format (ip: [domain, [nsname], [nsip], description, manpage])
        2 - to only list C&C server domains
        3 - to list C&C server domains and corresponding DNS IPs
    2nd parameter -- optional specification of which DGA family or a C&C server IP'''))

    args = parser.parse_args()
    d = args.dga
    l = args.list


    if d:  # if -d  # to list all possible DGA fams
        for key in dga.keys():
            print(key)
    else:  # if -l # to list info
        if len(l) == 1:  # all info  # no specific ip or dga fam
            l = l[0]
            if l == '1':  # list all info
                pull(complete)
            elif l == '2':  # only domains
                only_domain(complete)
            elif l == '3':  # C&C domain and corresponding DNS IPs
                domains_nsips(complete)
            else:
                print("Not an available option. Please choose 1 to list all information, 2 for only the C&C domains, and 3 for C&C domains and corresponding DNS IPs")
        elif len(l) == 2:  # specified DGA fam or C&C IP
            if l[0] == '1':  # all info
                if l[1].lower() in dga.keys():  # of specific DGA fam
                    pull(dga, l[1].lower())
                elif l[1] in complete.keys():  # of specific C&C IP
                    pull(complete, l[1])
                else:
                    print("Your 2nd parameter neither specified a DGA family nor a C&C IP. Please enter either a correct value or nothing")
            elif l[0] == '2':  # only C&C domains
                if l[1].lower() in dga.keys():  # of specific dga fam
                    only_domain(dga, l[1].lower())
                elif l[1] in complete.keys():  # of specific C&C IP
                    only_domain(complete, l[1])
                else:
                    print("Your 2nd parameter neither specified a DGA family nor a C&C IP. Please enter either a correct value or nothing")
            elif l[0] == '3':  # C&C domain AND corresponding DNS IPs
                if l[1].lower() in dga.keys():  # of specific DGA fam
                    domains_nsips(dga, l[1].lower())
                elif l[1] in complete.keys():  # of specific C&C IP
                    domains_nsips(complete, l[1])
                else:
                    print("Your 2nd parameter neither specified a DGA family nor a C&C IP. Please enter either a correct value or nothing")
        else:
            print("Too many parameters. Please input a maximum of 2 parameters, the 1st being your choice of what information to output and your 2nd the optional filter of DGA family or C&C IP")


if __name__ == '__main__':  # to easily run main from terminal
    main(sys.argv)
