from rdflib import Graph, Literal, Namespace, RDF, URIRef, BNode

graph = Graph()
#skos = Namespace('http://www.w3.org/2004/02/skos/core#')
rdfs = Namespace('http://www.w3.org/2000/01/rdf-schema#')
#foaf = Namespace('http://xmlns.com/foaf/0.1/')
#dc = Namespace('http://purl.org/dc/elements/1.1/')
rdf = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
#bio = Namespace('http://purl.org/vocab/bio/0.1/')
schema = Namespace('https://schema.org/')
eaccpf = Namespace('http://culturalis.org/eac-cpf#')
dbo = Namespace('http://dbpedia.org/ontology/')
#rdaad = Namespace('http://rdaregistry.info/Elements/a/datatype/')
djo = Namespace('http://dijest.ac.il/ontology/')
djr = Namespace('http://dijest.ac.il/resource/')
#bibo = Namespace('http://purl.org/ontology/bibo/')
owl = Namespace('http://www.w3.org/2002/07/owl#')
fabio = Namespace('http://purl.org/spar/fabio/')
eaccpf = Namespace('http://culturalis.org/eac-cpf#')
owl = Namespace('http://www.w3.org/2002/07/owl#')
bf = Namespace('http://id.loc.gov/ontologies/bibframe/')
gnd = Namespace('https://d-nb.info/standards/elementset/gnd#')
gn = Namespace('https://www.geonames.org/ontology#')

#graph.bind('skos', skos)
graph.bind('rdfs', rdfs)
#graph.bind('foaf', foaf)
#graph.bind('dc', dc)
graph.bind('rdf', rdf)
#graph.bind('bio', bio)
graph.bind('schema', schema)
graph.bind('eac-cpf', eaccpf)
graph.bind('dbo', dbo)
#graph.bind('rdaad', rdaad)
graph.bind('djo', djo)
graph.bind('djr', djr)
#graph.bind('bibo', bibo)
graph.bind('owl', owl)
graph.bind('fabio', fabio)
graph.bind('eac-cpf', eaccpf)
graph.bind('bf', bf)
graph.bind('gnd', gnd)
graph.bind('gn', gn)

graph.add((djo['Place'], RDF['type'], owl['Class']))
graph.add((djo['Place'], rdfs['label'], Literal('Place')))
graph.add((djo['Place'], rdfs['subClassOf'], owl['Thing']))
graph.add((djo['Place'], owl['equivalentClass'], schema['Place']))
graph.add((djo['Place'], owl['equivalentClass'], gn['Feature']))

graph.add((djo['Book'], RDF['type'], owl['Class']))
graph.add((djo['Book'], rdfs['label'], Literal('Book')))
graph.add((djo['Book'], rdfs['subClassOf'], owl['Thing']))
graph.add((djo['Book'], owl['equivalentClass'], schema['Book']))
graph.add((djo['Book'], owl['equivalentClass'], fabio['Book']))
graph.add((djo['Book'], owl['equivalentClass'], bf['Work']))
graph.add((djo['Book'], owl['equivalentClass'], gnd['Work']))

graph.add((djo['Person'], RDF['type'], owl['Class']))
graph.add((djo['Person'], rdfs['label'], Literal('Person')))
graph.add((djo['Person'], rdfs['subClassOf'], owl['Thing']))
graph.add((djo['Person'], owl['equivalentClass'], schema['Person']))
graph.add((djo['Person'], owl['equivalentClass'], dbo['Person']))
graph.add((djo['Person'], owl['equivalentClass'], eaccpf['Person']))


'''
graph.add((bibo['Book'], RDF['type'], owl['Class']))
graph.add((bibo['Book'], rdfs['label'], Literal('Book')))
graph.add((bibo['Book'], rdfs['subClassOf'], owl['Thing']))
#graph.add((bibo['Book'], rdfs['subClassOf'], bibo['Document']))

graph.add((schema['Book'], RDF['type'], owl['Class']))
graph.add((schema['Book'], rdfs['label'], Literal('Book')))
graph.add((schema['Book'], rdfs['subClassOf'], owl['Thing']))
#graph.add((schema['Book'], rdfs['subClassOf'], schema['CreativeWork']))

graph.add((fabio['Book'], RDF['type'], owl['Class']))
graph.add((fabio['Book'], rdfs['label'], Literal('Book')))
graph.add((fabio['Book'], rdfs['subClassOf'], owl['Thing']))
#graph.add((fabio['Book'], rdfs['subClassOf'], fabio['Expression']))

graph.add((schema['Person'], RDF['type'], owl['Class']))
graph.add((schema['Person'], rdfs['label'], Literal('Person')))
graph.add((schema['Person'], rdfs['subClassOf'], owl['Thing']))

graph.add((dbo['Person'], RDF['type'], owl['Class']))
graph.add((dbo['Person'], rdfs['label'], Literal('Person')))
graph.add((dbo['Person'], rdfs['subClassOf'], owl['Thing']))

graph.add((eaccpf['Person'], RDF['type'], owl['Class']))
graph.add((eaccpf['Person'], rdfs['label'], Literal('Person')))
graph.add((eaccpf['Person'], rdfs['subClassOf'], owl['Thing']))
'''

graph.serialize(destination='ontology.ttl',format='turtle', encoding='utf8') 















'''

@prefix djo: <http://dijest.technion.ac.il/ontology/> .
@prefix fabio: <http://purl.org/spar/fabio/> .
@prefix bibo: <http://purl.org/ontology/bibo/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

djo:Place a owl:Class ;
    rdfs:label "Place" ;
    rdfs:subClassOf owl:Thing .

bibo:Book a owl:Class ;
    rdfs:label "Book" ;
    rdfs:subClassOf owl:Thing .

fabio:Book a owl:Class ;
    rdfs:label "Book" ;
    rdfs:subClassOf owl:Thing .

    '''