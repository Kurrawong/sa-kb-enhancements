from pathlib import Path
from lxml import etree
from rdflib import Graph, Namespace, URIRef, Literal, BNode
from rdflib.namespace import RDF, RDFS, SDO, SKOS, XSD
import re


NAMESPACES = {
    "csw": "http://www.opengis.net/cat/csw/2.0.2",
    "ogc": "http://www.opengis.net/ogc",
    "gml": "http://www.opengis.net/gml",
    "dc": "http://purl.org/dc/elements/1.1/",
    "dcterms": "http://purl.org/dc/terms/",
    "ows": "http://www.opengis.net/ows",
    "xlink": "http://www.w3.org/1999/xlink",
    "gmd": "http://www.isotc211.org/2005/gmd",
    "gco": "http://www.isotc211.org/2005/gco",
    "gmx": "http://www.isotc211.org/2005/gmx",
    "srv": "http://www.isotc211.org/2005/srv",
    "gmi": "http://www.isotc211.org/2005/gmi",
    "gts": "http://www.isotc211.org/2005/gts",
    "pubSub": "http://www.opengis.net/pubsub/1.0",
    "ows11": "http://www.opengis.net/ows/1.1",
    "gml32": "http://www.opengis.net/gml/3.2",
    "xacml": "urn:oasis:names:tc:xacml:3.0:core:schema:wd-17",
    "oai": "http://www.openarchives.org/OAI/2.0/",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "xs": "http://www.w3.org/2001/XMLSchema"
}

ISO_19139 = Namespace("http://def.isotc211.org/iso19139/2005/")
TC_211 = URIRef("https://linked.data.gov.au/org/tc211")
ISO = URIRef("https://linked.data.gov.au/org/iso")

STATIC_RDF = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX schema: <https://schema.org/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

<xxx>
    a skos:ConceptScheme ;
    schema:creator <https://linked.data.gov.au/org/tc211> ;
    schema:contributor
        <https://linked.data.gov.au/org/bodc> ,
        <https://kurrawong.ai> ;
    schema:dateCreated "2005"^^xsd:gYear ;
    schema:dateModified "2005"^^xsd:gYear ;
    schema:publisher <https://linked.data.gov.au/org/tc211> ;
    skos:historyNote "This SKOS form of this codelist was produces for the British Oceanographic Data Centre's contribution to the FAIR EASE project which involved the establishment of a Semantic Analyser tool that extracted keywords from ISO 19139 XML data and comared them to a knowledge Base" ; 
.

<https://linked.data.gov.au/org/tc211>
    a schema:Organization ;
    schema:name "ISO's Technical Committee 211" ;
    schema:description '''The International Organization for Standardization's Technical Committee on "Geographic information/Geomatics", is charged with standardization in the field of digital geographic information.''' ;
    schema:parentOrganization <https://linked.data.gov.au/org/iso> ;
    schema:url "https://www.iso.org/committee/54904.html"^^xsd:anyURI ;
.

<https://linked.data.gov.au/org/bodc>
    a schema:Organization ;
    schema:name "British Oceanographic Data Centre" ;
    schema:description '''The BODC's mission is to 'operate as a world-class data centre in support of UK marine science'.
    
The BODC is an independent self-governing organisation.''' ;
    schema:url "https://www.bodc.ac.uk"^^xsd:anyURI ;
    owl:sameAs <https://ror.org/03102fn17> ;
.

<https://kurrawong.ai>
    a schema:Organization ;
    schema:name "KurrawongAI" ;
    schema:description '''KurrawongAI is a small, Australian-based company enabling organisations to take control of their data.''' ;
    schema:url "https://kurrawong.ai"^^xsd:anyURI ;
.


"""


def titalize(id: str):
    parts = re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', id)).split()
    return " ".join(parts[1:])


if __name__ == "__main__":
    me = Path(__file__)
    et = etree.parse(me.parent / "gmxCodeLists.xml")

    # make vocabs
    for cs in et.xpath("//gmx:CodeListDictionary", namespaces=NAMESPACES):
        g = Graph()
        cs_id = cs.xpath("@gml:id", namespaces=NAMESPACES)[0]
        cs_iri = URIRef(ISO_19139 + cs_id)
        title = Literal(titalize(cs_id), lang="en")
        defn = Literal(cs.xpath("gml:description/text()", namespaces=NAMESPACES)[0], lang="en")

        g.bind("cs", cs_iri)
        g.bind("", Namespace(str(cs_iri) + "/"))

        # static RDF
        g.parse(data=STATIC_RDF.replace("xxx", str(cs_iri)), format="turtle")

        # dynamic RDF
        g.add((cs_iri, RDF.type, SKOS.ConceptScheme))
        g.add((cs_iri, SKOS.prefLabel, title))
        g.add((cs_iri, SKOS.definition, defn))

        # each code
        for concept in cs.xpath("gmx:codeEntry/gmx:CodeDefinition", namespaces=NAMESPACES):
            print([x for x in concept])
            c_id = concept.xpath("@gml:id", namespaces=NAMESPACES)[0]
            c_iri = URIRef(str(cs_iri) + "/" + c_id)
            title = Literal(concept.xpath("gml:identifier/text()", namespaces=NAMESPACES)[0], lang="en")
            defn = Literal(cs.xpath("gml:description/text()", namespaces=NAMESPACES)[0], lang="en")

            g.add((c_iri, RDF.type, SKOS.Concept))
            g.add((c_iri, SKOS.prefLabel, title))
            g.add((c_iri, SKOS.definition, defn))
            g.add((c_iri, SKOS.inScheme, cs_iri))
            g.add((c_iri, SKOS.topConceptOf, cs_iri))
            g.add((c_iri, RDFS.isDefinedBy, cs_iri))

            g.add((cs_iri, SKOS.hasTopConcept, c_iri))

        g.serialize(format="longturtle", destination=str(me.parent.parent / f"{cs_id}.ttl"))

print("complete")




