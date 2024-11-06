# Semantic Analyser Knowledge Base Enhancements

This repository contains enhancements to the Semantic Analyser's Knowledge Base in the forms of:

* new content 
    * mostly new vocabularies
* new structures
    * the "system Graph", identified by the Semantic Analyser namespace-based IRI of `<http://w3id.org/semanticanalyser/system-graph>`

> [!NOTE]  
> This repository does _NOT_ contain any parts of the Semantic Analyser's metadata processing code. 
> 
> For that see the [SA XML Processor](https://github.com/Kurrawong/sa-xml-processor) repository.

## Contents

* `config/` - configuration information for the KB in Fuseki
* `content/` - new content to load and scripts for it
* `scripts/` - a series of SPARQL scripts to be run on the KB as dumped on 22nd July to improve it
* `requirements.txt` - Python packages needed for all the scripts in this repo
* `system-graph*.ttl` - various parts of an update System Graph
