#!/bin/bash

# hard-coded input path is a directory with foo.jpg and foo.json
# output foo.jpg in /tmp/out

mkdir -p /tmp/out
d="/scratch/jason-data/pandemic51/test"
for i in $d/*.jpg; do
    j=${i/jpg/json};
    b=$(basename $i);
    echo $b;
    python test_redaction.py -d /tmp/out/$b $i $j; 
done

