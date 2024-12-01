from pathlib import Path
from rdflib import Graph, Namespace
from rdflib.namespace import RDF, SDO

from utils import kb_graph_add, graph_exist

REPO_HOME = Path(__file__).parent.parent.resolve()


SA = Namespace("https://w3id.org/semanticanalyser/")
SYSTEM_GRAPH_IRI = "https://w3id.org/semanticanalyser/system-graph"


if __name__ == "__main__":
    # read the provided System Graph
    g = Graph().parse(Path("system-graph.ttl"))

    # for each, load if there is no Nameg Graph for it in the target Fuseki
    no = 0
    added = 0
    for v in g.subjects(RDF.type, SA.Vocabulary):
        no += 1
        for d_bn in g.objects(v, SDO.distribution):
            for o in g.objects(d_bn, SDO.contentUrl):
                if not "nalt" in str(o):  # exclude NALT due to size
                    print(v)
                    if graph_exist(str(v)):
                        pass
                    else:
                        print(f"Adding <{v}>")
                        kb_graph_add(REPO_HOME / Path(str(o)), str(v))
                        added += 1

    print(f"{no} vocabs, {added} added")

