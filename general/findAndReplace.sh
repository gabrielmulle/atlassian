"""
Simple shell script to add/replace comments
"""

#!/bin/bash

cat users.csv | while read line;
do
   source=`echo "$line" | cut -d ',' -f 1`
   target=`echo "$line" | cut -d ',' -f 2`
   sed -i '' "s/$source/$target/g" comments.csv
done
