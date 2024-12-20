import httpx
from pathlib import Path


def kb_graph_add(ttl_file: Path, graph_iri: str):
    r = httpx.post(
        "http://localhost:3030/ds",
        params={"graph": graph_iri},
        headers={"Content-Type": "text/turtle"},
        data=ttl_file.read_bytes(),
        timeout=120
    )

    return r.status_code, r.text


def kb_graph_replace(ttl_file: Path, graph_iri: str):
    r = httpx.delete(
        "http://localhost:3030/ds",
        params={"graph": graph_iri},
        timeout=120
    )

    kb_graph_add(ttl_file, graph_iri)

    print(f"replaced {graph_iri}")

    return r.status_code, r.text


def kb_graph_add_if_missing(ttl_file: Path, graph_iri: str):
    if not graph_exists(graph_iri):
        kb_graph_add(ttl_file, graph_iri)
        print(f"Added {graph_iri}")
    else:
        print(f"Already exists {graph_iri}")


def graph_exists(iri: str) -> bool:
    q = """
        ASK
        WHERE {
          GRAPH <IRI> {
                ?s ?p ?o
            }
        }    
        """.replace("IRI", iri)

    r = httpx.get(
        "http://localhost:3030/ds",
        params={"query": q}
    )

    return r.json()["boolean"]
