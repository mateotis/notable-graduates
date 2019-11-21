import requests
from time import perf_counter

codeList = []
f = open("codeList100.txt", "r")
lines = f.read().splitlines()
for code in lines:
	codeList.append(code)

# construct the URL for the HTTP GET call
timeStart = perf_counter()

for code in codeList:
	endpointUrl = 'https://query.wikidata.org/sparql'
	query = '''
	PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
	PREFIX wd: <http://www.wikidata.org/entity/>
	PREFIX wdt: <http://www.wikidata.org/prop/direct/>
	SELECT ?item ?itemLabel ?eduLabel
	WHERE
	{
	    ?item wdt:P31 wd:Q5 .

	    FILTER (?item IN (wd:'''+ code +'''))

	    OPTIONAL {
	        ?item wdt:P69 ?edu
	    }
	    SERVICE wikibase:label { bd:serviceParam wikibase:language  
	                                "[AUTO_LANGUAGE],en" }
	}
	ORDER BY ASC(?name)
	'''
	#print(query)

	# The endpoint defaults to returning XML, so the Accept: header is required.
	# application/sparql-results+json is the official Internet Media Type for JSON results.
	# However, endpoints typically will also respond to application/json
	r = requests.get(endpointUrl, params={'query' : query}, headers={'Accept' : 'application/sparql-results+json'})
	#r = requests.post(endpointUrl, data=query, headers={'Content-Type': 'application/sparql-query', 'Accept' : 'application/sparql-results+json'})

	#print(r.url)
	#print()
	#print(r.text)

	#print(r.json())
	try:
		resultsList = r.json()['results']['bindings']
	except:
		continue

	try:
		resultsList[0].get('eduLabel').get('value')
	except:
		continue

	for i in range(len(resultsList)):
		print(resultsList[i].get('eduLabel').get('value'))

timeEnd = perf_counter()
print("Execution time:", timeEnd - timeStart)