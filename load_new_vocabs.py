import httpx
from pathlib import Path
from rdflib import Graph, Namespace
from rdflib.namespace import RDF, SDO, SKOS

SA = Namespace("http://w3id.org/semanticanalyser/")


def upload_file_to_db(ttl_file: Path, graph_iri: str):
    r = httpx.delete(
        "http://localhost:3030/ds",
        params={"graph": graph_iri},
        timeout=25
    )
    print(r.status_code)
    r = httpx.post(
        "http://localhost:3030/ds",
        params={"graph": graph_iri},
        headers={"Content-Type": "text/turtle"},
        data=ttl_file.read_bytes(),
        timeout=60
    )

    return r.status_code, r.text


if __name__ == "__main__":
    # read the provided System Graph
    g = Graph().parse("system-graph.ttl")

    # for each statically provided vocab in content/
    # if present, remove it from the KB and replace it with this content
    no = 0
    rep = 0
    for v in g.subjects(RDF.type, SA.Vocabulary):
        no += 1
        for d_bn in g.objects(v, SDO.distribution):
            for o in g.objects(d_bn, SDO.contentUrl):
                if not str(o).startswith("nalt"):  # exclude NALT due to size
                    rep += 1
                    print(f"reloading {o}")
                    upload_file_to_db(Path(".") / "content" / str(o), str(v))
    print(f"{no} vocabs, {rep} replaced")

    # reload the system graph too
    # upload_file_to_db(Path(".") / "system-graph.ttl", "http://w3id.org/semanticanalyser/system-graph")


# g.serialize("system-graph.2.ttl", format="longturtle")
