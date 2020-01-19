from rdflib import Graph, Literal, Namespace, RDF, URIRef, BNode
import ast #.literal_eval
import csv
import pprint


graph = Graph()

bibo = Namespace('http://purl.org/ontology/bibo/')
skos = Namespace('http://www.w3.org/2004/02/skos/core#')
rdfs = Namespace('http://www.w3.org/2000/01/rdf-schema#')
foaf = Namespace('http://xmlns.com/foaf/0.1/')
dc = Namespace('http://purl.org/dc/elements/1.1/')
dcterms = Namespace('http://purl.org/dc/terms/')
rdf = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
bio = Namespace('http://purl.org/vocab/bio/0.1/')
schema = Namespace('https://schema.org/')
prism = Namespace('http://prismstandard.org/namespaces/1.2/basic/')
fabio = Namespace('http://purl.org/spar/fabio/')
mrel = Namespace('http://id.loc.gov/vocabulary/relators/')
digest = Namespace('http://dijest.technion.ac.il/ontology/')
bf = Namespace('http://id.loc.gov/ontologies/bibframe/')
djo = Namespace('http://dijest.ac.il/ontology/')
djr = Namespace('http://dijest.ac.il/resource/')
owl = Namespace('http://www.w3.org/2002/07/owl#')
gnd = Namespace('https://d-nb.info/standards/elementset/gnd#')

graph.bind('bibo', bibo)
graph.bind('skos', skos)
graph.bind('rdfs', rdfs)
graph.bind('foaf', foaf)
graph.bind('dc', dc)
graph.bind('dcterms', dcterms)
graph.bind('rdf', rdf)
graph.bind('bio', bio)
graph.bind('schema', schema)
graph.bind('prism', prism)
graph.bind('fabio', fabio)
graph.bind('mrel', mrel)
graph.bind('bf', bf)
graph.bind('digest', digest)
graph.bind('djo', djo)
graph.bind('djr', djr)
graph.bind('owl', owl)
graph.bind('gnd', gnd)

#basis_uri = 'http://dijest.technion.ac.il/book/'
#basis_person_uri = 'http://dijest.technion.ac.il/person/'
basis_uri = 'djr:book/'
basis_person_uri = 'djr:person/'

with open ('mifalbibl_first_selection.csv','r') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		book_uri = basis_uri + row['uri']
		creator_uri = basis_person_uri + row['entityID']
		#graph.add((URIRef(book_uri), RDF['type'], bibo['Book']))
		#graph.add((URIRef(book_uri), RDF['type'], schema['Book']))
		#graph.add((URIRef(book_uri), RDF['type'], fabio['Book']))
		#graph.add((URIRef(book_uri), RDF['type'], owl['Thing']))
		graph.add((URIRef(book_uri), RDF['type'], djo['Book']))

		graph.add((URIRef(book_uri), dcterms['language'], Literal(row['dcterms:lanugage'])))
		book_label = row['dcterms:title']

		if len (row['dcterms:created']) > 0 and row['dcterms:created'] != 'TBD':
			book_label = row['dcterms:title'] + ' (' + row['dcterms:created'] + ')'
		else:
			book_label = row['dcterms:title']
		graph.add((URIRef(book_uri), rdfs['label'], Literal(book_label)))

		creatorNode = BNode('author-' + row['uri'])
		graph.add((creatorNode, RDF['type'], djo['Person']))
		graph.add((creatorNode, schema['name'], Literal(row['AuthorNoPoint'])))
		if len(row['entityID']) > 0:
			creator_uri = basis_person_uri + row['entityID']
			graph.add((creatorNode, schema['url'], URIRef(creator_uri)))
		graph.add((URIRef(book_uri),  dcterms['creator'], creatorNode))

		graph.add((URIRef(book_uri), dcterms['title'], Literal(row['dcterms:title'])))
		graph.add((URIRef(book_uri), fabio['hasSubtitle'], Literal(row['fabio:hasSubtitle'])))

		publicationPlace = BNode('publication-place-' + row['uri'])
		graph.add((publicationPlace, RDF['type'], djo['Place']))
		graph.add((publicationPlace, schema['name'], Literal(row['mrel:pup'])))
		if len(row['dijest:kimaID']) > 0:
			graph.add((publicationPlace, schema['url'], URIRef(row['dijest:kimaID'])))
		graph.add((URIRef(book_uri), fabio['hasPlaceOfPublication'], publicationPlace))

		graph.add((URIRef(book_uri), gnd['printer'], Literal(row['dijest:printer'])))
		graph.add((URIRef(book_uri), dcterms['publisher'], Literal(row['dcterms:publisher'])))
		graph.add((URIRef(book_uri), dcterms['created'], Literal(row['dcterms:created'])))

		if len(row['dijest:Haskama']) > 0:
			haskamahNode = BNode('haskamah-' + row['uri'])
			graph.add((haskamahNode, RDF['type'], bf['Note']))
			graph.add((haskamahNode, bf['notetype'], Literal('Haskamah', lang='en')))
			graph.add((haskamahNode, bf['notetype'], Literal('הסכמה', lang='he')))
			graph.add((haskamahNode, rdfs['label'], Literal(row['dijest:Haskama'], lang='he')))
			graph.add((URIRef(book_uri), bf['note'], haskamahNode))

		graph.add((URIRef(book_uri), bf['note'], Literal(row['bf:note'])))


graph.serialize(destination='book_samples.ttl',format='turtle', encoding='utf8') 