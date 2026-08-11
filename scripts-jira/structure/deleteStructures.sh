"""
- Use official API https://apidocs.structure.app/api#tag/Structures/operation/Retrieve%20a%20list%20of%20structures to get the list of all Structures, copy the result
- Paste the JSON from the above API into VS Code, select only the ids, and copy them
- Paste the ids from the Structures I want to delete into a csv file
- In the browser, I navigated to all Structures, opened dev tools, Network tab, and Deleted a single Structure
- Right click on the Delete call that is registered when deleting, and click Copy to Curl
- Paste the result to VS Code, copy this header: -H 'authorization: Bearer eyJra…..
- Add that bearer token to my script below and run it
"""

#!/bin/bash

token='Bearer eyJra............'
cat ids.csv | while read line;
do
	echo "\nDeleting Structure with id $line"
	curl -s -i \
      -X POST --url "https://structure.app/front/structure/delete" \
      -H "Authorization: $token" \
      -H 'Content-Type: application/json' \
      -H 'X-Api-Version: 38' \
	  -H 'x-tempo-domain-id: 5caa0470-8f39......' \
      --data-raw "[$line]"
done < ids.csv
