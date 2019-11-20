from qwikidata.linked_data_interface import get_entity_dict_from_api
from qwikidata.entity import WikidataItem, WikidataProperty
import csv
import pandas

codeList = []
eduDict = {}
foundCount = 0
missingCount = 0

f = open("codeList100.txt", "r")
lines = f.read().splitlines()
for code in lines:
	codeList.append(code)

#exit()

for name in codeList:

	personDict = get_entity_dict_from_api(name) # Insert QCode here
	person = WikidataItem(personDict)

	claim_groups = person.get_truthy_claim_groups() # Have no idea what this does
	try:
		eduGroups = claim_groups["P69"] # Grabs person's education
		foundCount++
	except:
		print("--------------------------")
		print("Education not there for", person.get_label() + "!")
		missingCount++
		continue
	eduEntries = len(eduGroups) # How many different entries there are

	print("--------------------------")
	print("Writing education for", person.get_label())
	print("--------------------------")
	eduList = []
	for i in range(eduEntries):
		eduEntry = eduGroups[i] # Get list entry
		qid = eduEntry.mainsnak.datavalue.value["id"] # Get its ID
		eduValue = WikidataItem(get_entity_dict_from_api(qid)) # Get its actual name
		#print(eduValue.get_label()) # Print that name
		eduList.append(eduValue.get_label())

	eduDict[name] = eduList
	eduList = []

print("Education found for:", foundCount)
print("Education missing for: ", missingCount)

with open('eduCSV.csv', mode='w') as eduCSV:
	fieldnames = ['wikidata_code_B', 'education']
	writer = csv.DictWriter(eduCSV, fieldnames=fieldnames)

	writer.writeheader()
	for qcode in eduDict:
		writer.writerow({'wikidata_code_B': qcode, 'education': eduDict[qcode]})


df = pandas.read_csv('eduCSV.csv')
print(df)