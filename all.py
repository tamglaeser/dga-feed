import urllib.request
from bs4 import BeautifulSoup

url = "https://osint.bambenekconsulting.com/feeds/" #URL for free intel feeds offered by Bambenek Consulting
html = urllib.request.urlopen(url)
soup = BeautifulSoup(html, "lxml")
text = soup.get_text()
lines = text.splitlines() #newline ch after IP List | -- account for this in for/elif/if

start = 0 ## 0 until at beginning of listings of family-specific feeds

domain = ip = description = manpage = ""
ns_host = ns_ip = []

for line in lines:

    if line == "Family-Specific Feeds":
        start = 1
    elif start == 1: ## entered listings of family-specific feeds

        element = line.split('|')

        if not len(line.strip()) == 0 and element[0].split()[0][0:2] != 'NS': # if not empty line or middle of line starting w NS Host List
            if element[0].split()[0] == "Cryptolocker": #exception
                name = "cl"
            elif element[0].split()[1] == "GOZ": #exception
                name = element[0].split()[0] + element[0].split()[1]
            else:
                name = element[0].split()[0] #1st word on line
            name = name.split('/')[0] #stop at / if no spaces before
            name = name.lower()

            exec(f'{name} = []') #complete array for this feed

            each_url = url + name + "-master.txt"
            data = urllib.request.urlopen(each_url) #open master to get data

            after = 0 ## 0 until reach beginning of data set (past the beginning comments)
            for ln in data:
                decoded_line = ln.decode("utf-8")
                if decoded_line[0]  != '#' and after == 0:
                    after = 1
                    f = open("output/" + name + ".txt", "w") # overwrites if file/content already exists
                if after == 1 and decoded_line[0] != '#': #while data

                    f.write(decoded_line)

                    parts = decoded_line.split(',')
                    domain = parts[0] #domain
                    ip = parts[1] #IP
                    ns_host = parts[2].split('|')
                    ns_ip = parts[3].split('|')
                    description = parts[4]
                    manpage = parts[5]

                    each = [] # array for each line of data
                    each.append(domain)
                    each.append(ip)
                    each.append(ns_host)
                    each.append(ns_ip)
                    each.append(description)
                    each.append(manpage)

                    exec(f'{name}.append(each)') #add each line of data to that feed's complete array

            if after == 1:
                f.close()
