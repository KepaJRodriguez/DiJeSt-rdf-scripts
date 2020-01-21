from rdflib import Graph, Literal, Namespace, RDF, URIRef, BNode
import ast #.literal_eval
import csv
import pprint


graph = Graph()
skos = Namespace('http://www.w3.org/2004/02/skos/core#')
rdfs = Namespace('http://www.w3.org/2000/01/rdf-schema#')
#foaf = Namespace('http://xmlns.com/foaf/0.1/')
#dc = Namespace('http://purl.org/dc/elements/1.1/')
rdf = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
#bio = Namespace('http://purl.org/vocab/bio/0.1/')
schema = Namespace('https://schema.org/')
eaccpf = Namespace('http://culturalis.org/eac-cpf#')
dbo = Namespace('http://dbpedia.org/ontology/')
rdaad = Namespace('http://rdaregistry.info/Elements/a/datatype/')
djo = Namespace('http://dijest.ac.il/ontology/')
djr = Namespace('http://dijest.ac.il/resource/')
owl = Namespace('http://www.w3.org/2002/07/owl#')


graph.bind('skos', skos)
graph.bind('rdfs', rdfs)
#graph.bind('foaf', foaf)
#graph.bind('dc', dc)
graph.bind('rdf', rdf)
#graph.bind('bio', bio)
graph.bind('schema', schema)
graph.bind('eac-cpf', eaccpf)
graph.bind('dbo', dbo)
graph.bind('rdaad', rdaad)
graph.bind('djo', djo)
graph.bind('djr', djr)
graph.bind('owl', owl)

#basis_uri = 'http://dijest.ac.il/person/'
basis_uri = 'djr:person/'

entities_links = {}

with open ('people-links-sample-2-tsv.csv', 'r') as csvfile:
	reader = csv.DictReader(csvfile, delimiter="\t")
	for row in reader:
		if row['entity_ID'] in entities_links:
			if row['source'] == 'wikidata':
				entities_links[row['entity_ID']]['wikidata'].append(row['link'])
			if row['source'] == 'VIAF':
				entities_links[row['entity_ID']]['VIAF'].append(row['link'])
			if row['source'] == 'Yiddish Leksikon':
				entities_links[row['entity_ID']]['Yiddish Leksikon'].append(row['link'])
		else:
			entity = {'wikidata':[], 'VIAF':[], 'Yiddish Leksikon':[]}
			if row['source'] == 'wikidata':
				entity['wikidata'].append(row['link'])
			if row['source'] == 'VIAF':
				entity['VIAF'].append(row['link'])
			if row['source'] == 'Yiddish Leksikon':
				entity['Yiddish Leksikon'].append(row['link'])
			entities_links[row['entity_ID']] = entity


with open ('DiJeSt_personalities.csv', 'r') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		person_uri = basis_uri + row['entityID']
		graph.add((URIRef(person_uri), RDF['type'], djo['Person']))
		if row['entityID'] in entities_links:
			if len(entities_links[row['entityID']]['VIAF']) > 0:
				graph.add((URIRef(person_uri), skos['closeMatch'], URIRef(entities_links[row['entityID']]['VIAF'][0])))
			if len(entities_links[row['entityID']]['wikidata']) > 0:
				graph.add((URIRef(person_uri), skos['closeMatch'], URIRef(entities_links[row['entityID']]['wikidata'][0])))
			if len(entities_links[row['entityID']]['Yiddish Leksikon']) > 0:
				graph.add((URIRef(person_uri), rdfs['seeAlso'], URIRef(entities_links[row['entityID']]['Yiddish Leksikon'][0])))
		if len(row['gender']) > 0:
			if row['gender'] == 'male':
				graph.add((URIRef(person_uri), schema['gender'], URIRef('https://schema.org/Male')))
			if row['gender'] == 'female':
				graph.add((URIRef(person_uri), schema['gender'], URIRef('https://schema.org/Female')))
		if len(row['birthDate']) > 0: 
			graph.add((URIRef(person_uri), schema['birthDate'], Literal(row['birthDate'])))
		if len(row['deathDate']) > 0: 
			graph.add((URIRef(person_uri), schema['deathDate'], Literal(row['deathDate'])))
		if len(row['activeDate']) > 0: 
			graph.add((URIRef(person_uri), dbo['activeYears'], Literal(row['activeDate'])))
		if len(row['language']) > 0: 
			languages = row['language'].split('; ')
			for language in languages:
				graph.add((URIRef(person_uri), rdaad['P50102'], Literal(language)))

		if len(row['birthPlaceKima']) > 0:
			graph.add((URIRef(person_uri), schema['birthPlace'], URIRef(row['birthPlaceKima'])))
		else:
			if len(row['birthPlace']) > 0:
				graph.add((URIRef(person_uri), schema['birthPlace'], Literal(row['birthPlace'])))

		if len(row['deathPlaceKima']) > 0:
			graph.add((URIRef(person_uri), schema['deathPlace'], URIRef(row['deathPlaceKima'])))
		else:
			if len(row['deathPlace']) > 0:
				if row['deathPlace'] != '[]':
					graph.add((URIRef(person_uri), schema['deathPlace'], Literal(row['deathPlace'])))


		if len(row['associatedPlaces']) > 0:
			associatedPlaces = ast.literal_eval(row['associatedPlaces'])
			if len(associatedPlaces) > 0:
				for assp in associatedPlaces:
					if len(list(assp.values())[0]) > 0:
						graph.add((URIRef(person_uri), eaccpf['hasPlace'], URIRef(list(assp.values())[0])))
					else:
						place_name = list(assp.keys())[0]
						graph.add((URIRef(person_uri), eaccpf['hasPlace'], Literal(place_name)))


		if len(row['nameHeb']) > 0:
			graph.add((URIRef(person_uri), schema['name'], Literal(row['nameHeb'], lang='und-Hebr')))
		if len(row['firstNameHeb']) > 0:
			graph.add((URIRef(person_uri), schema['givenName'], Literal(row['firstNameHeb'], lang='und-Hebr')))
		if len(row['lastNameHeb']) > 0:
			graph.add((URIRef(person_uri), schema['familyName'], Literal(row['lastNameHeb'], lang='und-Hebr')))


		if len(row['firstNameHeb']) > 0 and len(row['lastNameHeb']) > 0:
			label_name_heb = row['firstNameHeb'] + ' ' + row['lastNameHeb']
			graph.add((URIRef(person_uri), rdfs['label'], Literal(label_name_heb, lang='und-Hebr')))
		if len(row['firstNameLat']) > 0 and len(row['lastNameLat']) > 0:
			label_name_lat = row['firstNameLat'] + ' ' + row['lastNameLat']
			graph.add((URIRef(person_uri), rdfs['label'], Literal(label_name_lat, lang='und-Latn')))
		if len(row['firstNameCyr']) > 0 and len(row['lastNameCyr']) > 0:
			label_name_cyr = row['firstNameCyr'] + ' ' + row['lastNameCyr']
			graph.add((URIRef(person_uri), rdfs['label'], Literal(label_name_cyr, lang='und-Cyrl')))
		if len(row['firstNameAra']) > 0 and len(row['lastNameAra']) > 0:
			label_name_ar = row['firstNameAra'] + ' ' + row['lastNameAra']
			graph.add((URIRef(person_uri), rdfs['label'], Literal(label_name_ar, lang='und-Arab')))


		if len(row['nameLat']) > 0:
			graph.add((URIRef(person_uri), schema['name'], Literal(row['nameLat'], lang='und-Latn')))
		if len(row['firstNameLat']) > 0:
			graph.add((URIRef(person_uri), schema['givenName'], Literal(row['firstNameLat'], lang='und-Latn')))
		if len(row['lastNameLat']) > 0:
			graph.add((URIRef(person_uri), schema['familyName'], Literal(row['lastNameLat'], lang='und-Latn')))

		if len(row['nameCyr']) > 0:
			graph.add((URIRef(person_uri), schema['name'], Literal(row['nameCyr'], lang='und-Cyrl')))
		if len(row['firstNameCyr']) > 0:
			graph.add((URIRef(person_uri), schema['givenName'], Literal(row['firstNameCyr'], lang='und-Cyrl')))
		if len(row['lastNameCyr']) > 0:
			graph.add((URIRef(person_uri), schema['familyName'], Literal(row['lastNameCyr'], lang='und-Cyrl')))

		if len(row['nameAra']) > 0:
			graph.add((URIRef(person_uri), schema['name'], Literal(row['nameAra'], lang='und-Arab')))
		if len(row['firstNameAra']) > 0:
			graph.add((URIRef(person_uri), schema['givenName'], Literal(row['firstNameAra'], lang='und-Arab')))
		if len(row['lastNameAra']) > 0:
			graph.add((URIRef(person_uri), schema['familyName'], Literal(row['lastNameAra'], lang='und-Arab')))

		if len(row['alternateNameHeb']) > 0:
			if row['alternateNameHeb'] != 'set()':
				altNameHeb = ast.literal_eval(row['alternateNameHeb'])
				if len(altNameHeb) > 0:
					for anH in altNameHeb:
						graph.add((URIRef(person_uri), schema['alternateName'], Literal(anH, lang='und-Hebr')))


		if len(row['alternateNameLat']) > 0:
			if row['alternateNameLat'] != 'set()':
				altNameHeb = ast.literal_eval(row['alternateNameLat'])
				if len(altNameHeb) > 0:
					for anH in altNameHeb:
						graph.add((URIRef(person_uri), schema['alternateName'], Literal(anH, lang='und-Latn')))

		if len(row['alternateNameCyr']) > 0:
			if row['alternateNameCyr'] != 'set()':
				altNameHeb = ast.literal_eval(row['alternateNameCyr'])
				if len(altNameHeb) > 0:
					for anH in altNameHeb:
						graph.add((URIRef(person_uri), schema['alternateName'], Literal(anH, lang='und-Cyrl')))


		if len(row['alternateNameAra']) > 0:
			if row['alternateNameAra'] != 'set()':
				altNameHeb = ast.literal_eval(row['alternateNameAra'])
				if len(altNameHeb) > 0:
					for anH in altNameHeb:
						graph.add((URIRef(person_uri), schema['alternateName'], Literal(anH, lang='und-Arab')))




graph.serialize(destination='person_sample.ttl',format='turtle', encoding='utf8') 

#(format="turtle")
#(format="xml")