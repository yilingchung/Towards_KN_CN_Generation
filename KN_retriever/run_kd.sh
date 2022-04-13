#!/bin/bash

for file in CN/*.txt; do
	java -jar KD.jar -lang ENGLISH --no_idf -cp -p MEDIUM -l 1 -us -v -n 5 -m 6 $file
done

for file in HS/*.txt; do
	java -jar KD.jar -lang ENGLISH --no_idf -cp -p MEDIUM -l 1 -us -v -n 5 -m 6 $file
done
