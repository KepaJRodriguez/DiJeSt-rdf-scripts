from rdflib import Graph, Literal, Namespace, RDF, URIRef, BNode
import ast #.literal_eval
import csv
import pprint


graph = Graph()
skos = Namespace('http://www.w3.org/2004/02/skos/core#')
rdfs = Namespace('http://www.w3.org/2000/01/rdf-schema#')
rdf = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
schema = Namespace('https://schema.org/')
djo = Namespace('http://dijest.ac.il/ontology/')
djr = Namespace('http://dijest.ac.il/resource/')
owl = Namespace('http://www.w3.org/2002/07/owl#')
gn = Namespace('https://www.geonames.org/ontology#')
wgs84_pos = Namespace('http://www.w3.org/2003/01/geo/wgs84_pos#')


graph.bind('djo', djo)
graph.bind('djr', djr)
graph.bind('owl', owl)
graph.bind('rdfs', rdfs)
graph.bind('skos', skos)
graph.bind('schema', schema)
graph.bind('gn', gn)
graph.bind('wgs84_pos', wgs84_pos)

basis_uri = 'http://geo-kima.org/place/'
wikidata_namespace = 'https://www.wikidata.org/wiki/'
viaf_namespace = 'https://viaf.org/viaf/'
geonames_namespace = 'https://www.geonames.org/'


with open ('kimaPlaces2020-01-17.csv', 'r') as csvfile:
	reader = csv.DictReader(csvfile, delimiter='\t')
	for row in reader:
		place_uri = basis_uri + row['_ - id']
		graph.add((URIRef(place_uri), RDF['type'], djo['Place']))
		graph.add((URIRef(place_uri), schema['name'], Literal(row['_ - primary_heb_full'], lang='und-Hebr')))
		graph.add((URIRef(place_uri), schema['name'], Literal(row['_ - primary_rom_full'], lang='und-Latn')))
		if len(row['_ - coor']) > 0:
			pointer = row['_ - coor'].lower()
			graph.add((URIRef(place_uri), wgs84_pos['Point'], Literal(pointer)))
		if len(row['_ - viaF_ID']) > 0:
			graph.add((URIRef(place_uri), skos['closeMatch'], URIRef(viaf_namespace + row['_ - viaF_ID'])))
		if len(row['_ - wd']) > 0:
			graph.add((URIRef(place_uri), skos['closeMatch'], URIRef(wikidata_namespace + row['_ - wd'].replace(' ',''))))
		if len(row['_ - geoname_ID']) > 0:
			graph.add((URIRef(place_uri), skos['closeMatch'], URIRef(geonames_namespace + row['_ - geoname_ID'])))
		if len(row['_ - naF_ID']) > 0:
			nli_url = 'http://uli.nli.org.il/F/?func=direct&doc_number=00' + row['_ - naF_ID'] + '&local_base=nlx10'
			graph.add((URIRef(place_uri), rdfs['seeAlso'], URIRef(nli_url)))










graph.serialize(destination='dijest_places.ttl',format='turtle', encoding='utf8') 
