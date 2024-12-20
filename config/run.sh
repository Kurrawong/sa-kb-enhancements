# create local dirs for Fuseki config & Data
mkdir -p ~/work/bodc/sa-kb/fuseki/configuration
mkdir -p ~/work/bodc/sa-kb/fuseki/datasets

# add assembler to config
cp assembler.ttl ~/work/bodc/sa-kb/fuseki/configuration

# build triple indexes
source ~/jena-source.sh
tdb2.tdbloader --loc ~/work/bodc/sa-kb/fuseki/databases/ds fair-ease-with-rdfs_2024-07-22_13-43-19.nq

# build text index
#   download the fuseki JAR
curl -o ~/work/bodc/sa-kb/fuseki/fuseki-server.jar https://repo1.maven.org/maven2/org/apache/jena/jena-fuseki-server/5.2.0/jena-fuseki-server-5.2.0.jar
# run the fuseki JAR against the data locally - using local version of assembler
java -cp /home/nick/work/bodc/sa-kb/fuseki/fuseki-server.jar jena.textindexer --desc=/home/nick/work/bodc/sa-kb-enhancements/config/assembler-local.ttl

# at this stage, the DB is as-received from BODC

# add new vocabs
# run content/new-vocs/_load.sh
sh home/nick/work/bodc/sa-kb-enhancements/content/new-vocs/_load.sh

# rerun the text indexer
java -cp /home/nick/work/bodc/sa-kb/fuseki/fuseki-server.jar jena.textindexer --desc=/home/nick/work/bodc/sa-kb-enhancements/config/assembler-local.ttl

# log in to the container
docker run --rm --entrypoint=/bin/bash -it --env=ADMIN_PASSWORD=admin --volume=/home/nick/work/bodc/sa-kb/fuseki/configuration:/fuseki-base/configuration --volume=/home/nick/work/bodc/sa-kb/fuseki/databases:/fuseki-base/databases -p 3030:3030 --name SAKB5 secoresearch/fuseki:5.1.0

# run Fuseki using pre-built data and text index
docker run --rm --env=ADMIN_PASSWORD=admin --volume=/home/nick/work/bodc/sa-kb/fuseki/configuration:/fuseki-base/configuration --volume=/home/nick/work/bodc/sa-kb/fuseki/databases:/fuseki-base/databases -p 3030:3030 --name SAKB5 secoresearch/fuseki:5.2.0

# after this point, go to scripts/README.md to update the DB