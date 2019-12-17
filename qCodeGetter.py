from bs4 import BeautifulSoup
import requests
import csv

uniList = []
uniDict = {}

f = open("top200links.txt","r")
codes = f.read().splitlines()
for line in codes:
	uniList.append(line)

for uni in uniList:

	getUrl = 'https://en.wikipedia.org/wiki/' + uni
	url = getUrl

	content = requests.get(url).content
	soup = BeautifulSoup(content,'lxml')

	#extracting page title
	firstHeading = soup.find('h1',{'class' : 'firstHeading'})
	print(firstHeading.text)

	qCode = soup.find('li', {'id' : 't-wikibase'})
	qCode2 = qCode.a['href'].rsplit('/')[-1]

	uniDict[uni] = qCode2

	print(qCode2)


with open('top200qcodes.csv', mode='a', encoding = "UTF-8") as top200qcodes:
	fieldnames = ['Name', 'Q code']
	writer = csv.DictWriter(top200qcodes, fieldnames=fieldnames)
	writer.writeheader()
	for uni in uniDict:
		writer.writerow({'Name': uni, 'Q code': uniDict[uni]})