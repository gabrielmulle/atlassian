"""
How to use
1. Create a csv file; in the first column add the aaid of the current account, in the second column add the desired email
2. Run the code below
"""

#!/bin/bash
file=file.csv
APIkey=orgTokenHere

header=true
while read line || [ -n "$line" ]
do
if [ "$header" = 'true' ];
then
header=false
continue
fi

account_id=`echo $line | cut -d ',' -f1`
email=`echo $line | cut -d ',' -f2`

echo "$account_id"
echo "$email"

email="${email%%[[:cntrl:]]}"

curl --request PUT \\
--url "<https://api.atlassian.com/users/${account_id}/manage/email>" \\
--header "Authorization: Bearer ${APIkey}" \\
--header 'Content-Type: application/json' \\
--data '{
  "email": "'"$email"'"
}'

done <$file

"""
Alternative, in case you want to obfuscate emails and append something to the old emails.
1. Create a csv file; in the first column add the aaid of the account you want to obfuscate, in the second column add its current email
2. Run the code below
"""

#!/bin/bash
file=file2.csv
APIkey=orgTokenHere

header=true
while read line || [ -n "$line" ]
do
if [ "$header" = 'true' ];
then
header=false
continue
fi

account_id=`echo $line | cut -d ',' -f1`
email=`echo $line | cut -d ',' -f2`
email=${email/@/.old@}

echo "$account_id"
echo "$email"

email="${email%%[[:cntrl:]]}"

curl --request PUT \\
--url "<https://api.atlassian.com/users/${account_id}/manage/email>" \\
--header "Authorization: Bearer ${APIkey}" \\
--header 'Content-Type: application/json' \\
--data '{
  "email": "'"$email"'"
}'

done <$file
