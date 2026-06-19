"""
Add view permission
"""

#!/bin/bash
cat spaces.csv | while read line;
do
    spacekey=`echo $line | cut -d ',' -f1`
    echo ""
    echo "Adding group to space $spacekey"
    sleep 0.25
    curl -s -o /dev/null -w "%{http_code}" --request POST --url "<https://instance.atlassian.net/wiki/rest/api/space/$spacekey/permission>" --user "gm250363@example.com:ATATT3xFfGF0IfqkRiDcLBWGWx3VmAfoODi0ifXgFTF3a" --header 'Accept: application/json' --header 'Content-Type: application/json' --data '{"subject": {"type": "group", "identifier": "confluence-users"}, "operation": {"key": "read", "target": "space"}}'
done

"""
Add create permission
Check the —data and change the options accordingly
"""

#!/bin/bash
cat spaces.csv | while read line;
do
    spacekey=`echo $line | cut -d ',' -f1`
    echo ""
    echo "Adding create permissions to space $spacekey"
    sleep 0.25
    curl -s -o /dev/null -w "%{http_code}" --request POST --url "<https://instance.atlassian.net/wiki/rest/api/space/$spacekey/permission>" --user "gm250363@example.com:ATATT3xFfGF0IfqkRiDcLBWGWx3VmAfoODi0ifXgFTF3a" --header 'Accept: application/json' --header 'Content-Type: application/json' --data '{"subject": {"type": "group", "identifier": "confluence-users"}, "operation": {"key": "create", "target": "attachment"}}'
done
