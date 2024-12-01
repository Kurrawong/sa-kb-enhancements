from pathlib import Path
from rdflib import Graph
from rdflib.namespace import DC, DCTERMS, RDF, SKOS
from rdflib.paths import Path as RdfPath

o = ""
for f in sorted(Path(__file__).parent.glob("*.ttl")):
    print(f)
    g = Graph().parse(f)
    cs_iri = g.value(predicate=RDF.type, object=SKOS.ConceptScheme)
    plabel = None
    for p in g.objects(cs_iri, DC.title|DCTERMS.title|SKOS.prefLabel):
        if p is not None:
            if p.language == "en" or p.language is None:
                plabel = p

    rdf = """<IRI>
    a sa:Vocabulary ;
    skos:prefLabel "PLABEL" ;
    schema:distribution [
            schema:contentUrl "content/new-vocs/FNAME.ttl"
        ] ;
.

""".replace("IRI", cs_iri).replace("PLABEL", plabel).replace("FNAME", str(f))
    o += rdf

print(o)
