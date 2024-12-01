from pathlib import Path
from rdflib import Graph

for f in Path(__file__).parent.glob("*.rdf"):
    print(f)
    g = Graph().parse(f)
    g.serialize(destination=f.with_suffix(".ttl"), format="longturtle")