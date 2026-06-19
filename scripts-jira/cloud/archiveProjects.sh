"""
How to use
1. Create a CSV file with the keys of the projects you want to archive
2. Execute the script below (sh archive.sh)
"""

#!/bin/bash

cat projects.csv | while read line;
do
    printf "Archiving project $line: "
    sleep 0.25
    curl -s -o /dev/null -w "%{http_code}" -X POST --url "https://newaustin.atlassian.net/rest/api/3/project/$line/archive" --user 'gabriel.muller@example.com:<TOKEN>' --header 'Accept: application/json' -i
    echo 
done
