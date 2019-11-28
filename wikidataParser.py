from qwikidata.linked_data_interface import get_entity_dict_from_api
from qwikidata.entity import WikidataItem, WikidataProperty
from time import perf_counter
import csv

codeList = []
eduDict = {}
foundCount = 0
missingCount = 0
readyToAppend = False

# with open('MAT_alma_mater_top100_436countries2.csv', mode='r', encoding = "ISO-8859-1") as bigData: # Gets Q-codes from raw database
#     reader = csv.reader(bigData, delimiter=',')
#     codeCount = 0
#     for row in reader:
#         if codeCount == 0:
#         	codeCount += 1
#         else:
#             codeList.append(row[0])
#             codeCount += 1

f = open("codeList11.txt","r")
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
		missingCodes = open("missingCodes.txt","a")
		missingCodes.write(name+'\n')
		continue
	person = WikidataItem(personDict)

	claim_groups = person.get_truthy_claim_groups() # Have no idea what this does
	try:
		eduGroups = claim_groups["P69"] # Grabs person's education
		foundCount += 1
	except:
		print(str(cnt) + ".", "Education not there for", person.get_label())
		missingCount += 1
		if(cnt % 10 == 0):
			readyToAppend = True
		continue
	eduEntries = len(eduGroups) # How many different entries there are

	print(str(cnt) + ".", "Writing education for", person.get_label())
	eduList = []
	for i in range(eduEntries):
		try:
			eduEntry = eduGroups[i] # Get list entry
			qid = eduEntry.mainsnak.datavalue.value["id"] # Get its ID
			eduValue = WikidataItem(get_entity_dict_from_api(qid)) # Get its actual name
			eduList.append(eduValue.get_label())
		except:
			continue

	eduDict[name] = eduList
	eduList = []

	if(cnt % 10 == 0 or readyToAppend == True): # Write to file after 10 processed entries
		print("-------------------", '\n', "CHECKPOINT AT", cnt, '\n' + "-------------------")
		with open('eduCSV11.csv', mode='a', encoding = "UTF-8") as eduCSV:
			fieldnames = ['wikidata_code_B', 'education']
			writer = csv.DictWriter(eduCSV, fieldnames=fieldnames)
			if(cnt < 11): # Write header only at first checkpoint
				writer.writeheader()
			for qcode in eduDict:
				writer.writerow({'wikidata_code_B': qcode, 'education': eduDict[qcode]})
		eduDict = {}
		eduList = []
		readyToAppend = False		

print("Parsed", cnt, "people.")
print("Education found for:", foundCount)
print("Education missing for: ", missingCount)

timeEnd = perf_counter()
print("Execution time:", timeEnd - timeStart)