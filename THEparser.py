import csv

data = []
entry = []
cnt = 1

rankings = open("THE 2020 Rankings.txt","r")
lines = rankings.read().splitlines()
for line in lines:
	if(line.find('.') == -1 and line.find(',') != -1): # Line with rank and university name
		rank = line[:line.find(',')] # Split on comma
		name = line[line.find(',')+2:]
		entry.append(rank)
		entry.append(name)
		#data.append(dataList)
	elif(line.find(',') == -1): # Line with country
		country = line
		entry.append(country)
	else: # Line with various scores
		scores = line.split(', ')
		for i in scores:
			entry.append(i)

	if(cnt % 3 == 0): # Every entry is three lines in the file--once we have added all of them, push the whole entry to the dataset and reset the entry
		data.append(entry)
		entry = []
	cnt += 1

for i in data:
	print(i)

with open('THE2020.csv', mode='w') as THE2020:
	fieldnames = ['Rank', 'Name', 'Country/Region', 'Overall', 'Teaching', 'Research', 'Citations', 'Industry Income', 'International Outlook']
	writer = csv.DictWriter(THE2020, fieldnames=fieldnames)

	writer.writeheader()
	for entry in data:
		writer.writerow({'Rank': entry[0], 'Name': entry[1], 'Country/Region': entry[2], 'Overall': entry[3], 'Teaching': entry[4], 'Research': entry[5], 'Citations': entry[6], 'Industry Income': entry[7], 'International Outlook': entry[8]})