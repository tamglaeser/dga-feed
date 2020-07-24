import urllib.request

url = "https://osint.bambenekconsulting.com/feeds/c2-ipmasterlist-high.txt"
file = urllib.request.urlopen(url)

ip = []
description = []
date = []
manpage = []

f = open("output/c2_ip_feed.txt", "w") # overwrites if file/content already exists
for line in file:
    decoded_line = line.decode("utf-8")
    f.write(decoded_line)
    if decoded_line[0] != '#':
        parts = decoded_line.split(',')
        ip.append(parts[0])
        description.append(parts[1])
        date.append(parts[2])
        manpage.append(parts[3])

f.close()