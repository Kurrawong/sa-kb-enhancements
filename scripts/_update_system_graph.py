from pathlib import Path
from rdflib import Graph, Namespace

from utils import kb_graph_replace

REPO_HOME = Path(__file__).parent.parent.resolve()


SA = Namespace("https://w3id.org/semanticanalyser/")
SYSTEM_GRAPH_IRI = "https://w3id.org/semanticanalyser/system-graph"

g = Graph()
g.parse(REPO_HOME / "scripts" / "system-graph-existing-prefs.ttl")
# g.parse(REPO_HOME / "scripts" / "system-graph-iso-codelists.ttl")
g.parse(REPO_HOME / "scripts" / "system-graph-new-vocs.ttl")
g.serialize(destination=REPO_HOME / "scripts" / "system-graph.ttl", format="longturtle")

# kb_graph_replace()