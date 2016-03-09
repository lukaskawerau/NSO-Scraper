from bs4 import BeautifulSoup
import requests
import csv
import re

output = open("stat_sites.csv", 'w')
csv_writer = csv.writer(output)

link = "http://unstats.un.org/unsd/methods/inter-natlinks/sd_natstat.asp"

page = requests.get(link)
soup = BeautifulSoup(page.text, "lxml")

table = soup.find_all("td", class_="content")
continents = table[0].find_all("h3")
continents.pop(0)
previous_country = "empty"

for continent in continents:
	table = continent.next_sibling.next
	rows = table.find_all("tr")
	for row in rows:
		country = row.next.next.next
		country = re.sub('<[^<]+?>', '', str(country)) # Strip html tags
		if country == " ": # NONBREAKING SPACE! (Opt + Space) for USA List
			country = "United States"
		links = row.next.next.next_sibling.next.find_all("a")
		if len(links) > 1:
			for l in links:
				link = l["href"]
				name = l.next
				name = " ".join(name.split())
				csv_writer.writerow([country, link, name])
		else:
			link = row.next.next.next_sibling.next.find_all("a")[0]["href"]
			name = row.next.next.next_sibling.next.find_all("a")[0].next
			name = " ".join(name.split())
			csv_writer.writerow([country, link, name])