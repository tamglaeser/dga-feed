import urllib.request

url = "https://osint.bambenekconsulting.com/feeds/c2-masterlist-high.txt" #data page
file = urllib.request.urlopen(url)

complete = []
domain = ip = description = manpage = ""
ns_host = ns_ip = []

f = open("output/c2_all_indicator.txt", "w") # overwrites if file/content already exists
for line in file:
    decoded_line = line.decode("utf-8")
    f.write(decoded_line)
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

f.close()
print(complete)