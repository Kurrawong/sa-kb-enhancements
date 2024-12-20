# Adds BODC vocab preferences and known altLabels for vocabs
# extracted from FAIR EASE XML records as thesauri to the System Graph

from pathlib import Path
from utils import kb_graph_add

SYSTEM_GRAPH_IRI = "https://w3id.org/semanticanalyser/system-graph"

if __name__ == "__main__":
    print(kb_graph_add(Path(Path(__file__).parent / "system-graph-existing-prefs.ttl"), SYSTEM_GRAPH_IRI))
