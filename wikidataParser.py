from qwikidata.linked_data_interface import get_entity_dict_from_api
from qwikidata.entity import WikidataItem, WikidataProperty

codeList = []

f = open("codeList.txt", "r")
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
	except:
		print("Education not there for", person.get_label(), "!")
		continue
	eduEntries = len(eduGroups) # How many different entries there are

	print("--------------------------")
	print("Education of", person.get_label())
	print("--------------------------")
	for i in range(eduEntries):
		eduEntry = eduGroups[i] # Get list entry
		qid = eduEntry.mainsnak.datavalue.value["id"] # Get its ID
		eduValue = WikidataItem(get_entity_dict_from_api(qid)) # Get its actual name
		print(eduValue.get_label()) # Print that name
