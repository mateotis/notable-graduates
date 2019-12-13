from qwikidata.linked_data_interface import get_entity_dict_from_api
from qwikidata.entity import WikidataItem, WikidataProperty
from time import perf_counter
import csv

codeList = []
eduDict = {}
foundCount = 0
missingCount = 0
readyToAppend = False

# with open('top200qcodes.csv', mode='r', encoding = "UTF-8") as top200: # Gets Q-codes from raw database
# 	reader = csv.reader(top200, delimiter=',')
# 	codeCount = 0
# 	for row in reader:
# 		if codeCount == 0:
# 			continue
# 		else:
# 			codeList.append(row[1])
# 			codeCount += 1

f = open("top200qcodes.txt","r")
codes = f.read().splitlines()
codeCount = 0
for line in codes:
	codeList.append(line)
	codeCount += 1

print('Processed', codeCount, 'Q-codes.')
timeStart = perf_counter()

cnt = 0
for name in codeList:
	cnt += 1

	try:
		personDict = get_entity_dict_from_api(name) # Insert QCode here
	except:
		continue
	person = WikidataItem(personDict)

	claim_groups = person.get_truthy_claim_groups()
	try:
		eduGroups = claim_groups["P571"]
		foundCount += 1
	except:
		print(str(cnt) + ".", "Founding year not there for", person.get_label())
		missingCount += 1
		if(cnt % 10 == 0):
			readyToAppend = True
		continue
	eduEntries = len(eduGroups) # How many different entries there are
	print()

	print(str(cnt) + ".", "Writing founding year for", person.get_label())
	eduList = []
	eduEntry = eduGroups[0] # Get list entry

	qid = eduEntry.mainsnak.datavalue.value["time"] # Get the year
	qid = qid[1:5] # Only add the year
	print(qid)


	eduDict[name] = qid
	eduList = []

	if(cnt % 10 == 0 or readyToAppend == True): # Write to file after 10 processed entries
		print("-------------------", '\n', "CHECKPOINT AT", cnt, '\n' + "-------------------")
		with open('unisWithFounding.csv', mode='a', encoding = "UTF-8") as unisWithFounding:
			fieldnames = ['Q code', 'founding']
			writer = csv.DictWriter(unisWithFounding, fieldnames=fieldnames)
			if(cnt < 11): # Write header only at first checkpoint
				writer.writeheader()
			for qcode in eduDict:
				writer.writerow({'Q code': qcode, 'founding': eduDict[qcode]})
		eduDict = {}
		eduList = []
		readyToAppend = False

with open('unisWithFounding.csv', mode='a', encoding = "UTF-8") as unisWithFounding:
	fieldnames = ['Q code', 'founding']
	writer = csv.DictWriter(unisWithFounding, fieldnames=fieldnames)
	if(cnt < 11): # Write header only at first checkpoint
		writer.writeheader()
	for qcode in eduDict:
		writer.writerow({'Q code': qcode, 'founding': eduDict[qcode]})	

eduDict = {}
eduList = []
readyToAppend = False

print("Parsed", cnt, "people.")
print("Education found for:", foundCount)
print("Education missing for: ", missingCount)

timeEnd = perf_counter()
print("Execution time:", timeEnd - timeStart)