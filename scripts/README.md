# `scripts/`

## 1. Establish KB

### 1.1 Use the data files from https://github.com/Kurrawong/fair-ease-matcher/tree/bodc/triple_store_dump_2024_07_22/data/fuseki_triple_store_dump_2024_07_22

### 1.2 merge data files, rename sa-kb.nq

```
cat fair-ease-with-rdfs_2024-07-22_13-43-19.nq.gz_part_* > fair-ease-with-rdfs_2024-07-22_13-43-19.nq.gz

gunzip fair-ease-with-rdfs_2024-07-22_13-43-19.nq.gz
mv fair-ease-with-rdfs_2024-07-22_13-43-19.nq sa-kb.nq
```

### 1.3 load into Fuseki DB

Using Jena - https://jena.apache.org/download/:

```
./tdb2.xloader --loc /home/nick/work/bodc/sa-kb/fuseki/databases/ds sa-kb.nq
```

### 1.4 Run Fuseki

```
docker run --rm --env=ADMIN_PASSWORD=admin --volume=/home/nick/work/bodc/sa-kb/fuseki/configuration:/fuseki-base/configuration --volume=/home/nick/work/bodc/sa-kb/fuseki/databases:/fuseki-base/databases -p 3030:3030 --name SAKB5 secoresearch/fuseki:5.1.0
```

### 1.5 Test DB creation

Run query at http://localhost:3030

```
SELECT (COUNT(?g) AS ?c)
WHERE {
	SELECT DISTINCT ?g
	WHERE {
  	GRAPH ?g {
	    ?s ?p ?o
  		}
	}
}
```

Should be 92, takes ~15 sec

### 1.6 Test text index

??

## 2. Enhance the KB

SPARQL queries to be run on the KB as dumped on 22nd July 2024 to improve it.

The queries:

Testing queries to be run after DB establishment

* qT01 - qT03 - testing queries to see if the Full Text Index is working

Improvement queries to be run if above queries performing well:

* q01
* q02
* q03
* q04 - view results
* q05 - patch results from q04
* q04 - again, check for zero results
* q06 - populates the System Graph
    * q06-outputs.ttl - backup of the System Graph after q06
* q07 - a Python script that adds system-graph-existing-prefs.ttl to the System Graph
* q08 - load the new vocs

Count the graphs now:

```
SELECT (COUNT(?g) AS ?c)
WHERE {
	SELECT DISTINCT ?g
	WHERE {
  	GRAPH ?g {
	    ?s ?p ?o
  		}
	}
}
```

Should be , takes ~15 sec

* q09 OPTIONAL - load the ISO codelist vocs
* 
