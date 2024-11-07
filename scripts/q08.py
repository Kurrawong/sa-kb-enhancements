from pathlib import Path
from rdflib import Graph, Namespace
from rdflib.namespace import RDF, SDO

from utils import kb_graph_add, kb_graph_replace

REPO_HOME = Path(__file__).parent.parent.resolve()


SA = Namespace("https://w3id.org/semanticanalyser/")
SYSTEM_GRAPH_IRI = "https://w3id.org/semanticanalyser/system-graph"


if __name__ == "__main__":
    # read the provided System Graph
    g = Graph().parse(Path("system-graph-new-vocs.ttl"))

    # for each statically provided vocab in content/
    # if present, remove it from the KB and replace it with this content
    no = 0
    rep = 0
    for v in g.subjects(RDF.type, SA.Vocabulary):
        no += 1
        for d_bn in g.objects(v, SDO.distribution):
            for o in g.objects(d_bn, SDO.contentUrl):
                if not "nalt" in str(o):  # exclude NALT due to size
                    pth = REPO_HOME / Path(str(o))
                    rep += 1
                    print(f"reloading {pth}")
                    kb_graph_replace(pth, str(v))

    kb_graph_add(Path("system-graph-new-vocs.ttl"), SYSTEM_GRAPH_IRI)

    print(f"{no} vocabs, {rep} replaced")

