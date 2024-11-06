# Semantic Analyser Knowledge Base Enhancements

This repository contains enhancements to the Semantic Analyser's Knowledge Base in the forms of:

* new content 
    * mostly new vocabularies
* new structures
    * the "system Graph", identified by the Semantic Analyser namespace-based IRI of `<http://w3id.org/semanticanalyser/system-graph>`

> [!NOTE]  
> This repository does _NOT_ contain any parts of the Semantic Analyser's metadata processing code. It contains enhancements built on top of the [data dump of the SA' original KB](https://github.com/Kurrawong/fair-ease-matcher/tree/bodc/triple_store_dump_2024_07_22/data/fuseki_triple_store_dump_2024_07_22) only.
> 
> For that see the [SA XML Processor](https://github.com/Kurrawong/sa-xml-processor) repository.

## Contents

* `config/` - configuration information for the KB in Fuseki
* `content/` - new content to load into the KB, using scripts from `scripts/`
* `scripts/` - a series of SPARQL scripts to be run on the KB as dumped on 22nd July to improve it
* `requirements.txt` - Python packages needed for all the scripts in this repo
