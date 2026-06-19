"""
How to use
1. Create a CSV file with the AAID in the first column, and the desired name in the second. Example: 
712020:1c2d7770-359a-4120-a8a5-c432d5d95e4b, Source Gabriel Mulle
557058:e89104c1-8242-4244-b261-6705fcd09067, Target Gabriel Mulle
2. Replace the ABCDE in line 4 with your org api token
3. Execute the script below
"""

#!/bin/bash

file="userstoupdate.csv"
API_TOKEN="ABCDE"
SKIP_HEADER=false  # Set to false if there is no header

# Read file line by line
first_line=true
while IFS= read -r line || [[ -n "$line" ]]
do
    # Skip the first line if SKIP_HEADER is true
    if [[ "$SKIP_HEADER" == "true" && "$first_line" == "true" ]]; then
        first_line=false
        continue
    fi

    # Extract fields using awk
    account_id=$(awk -F',' '{print $1}' <<< "$line")
    account_name=$(awk -F',' '{print $2}' <<< "$line" | xargs)

    echo "Processing: ID=$account_id, Name=$account_name"

    # API Request
    curl --request PATCH \
        --url "https://api.atlassian.com/users/$account_id/manage/profile" \
        --header "Authorization: Bearer $API_TOKEN" \
        --header "Content-Type: application/json" \
        --data "$(jq -n --arg name "$account_name" '{"name":$name}')" -i

    first_line=false  # Ensures only the first line is skipped if needed
done < "$file"
