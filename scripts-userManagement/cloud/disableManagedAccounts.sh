"""
Endpoint
https://developer.atlassian.com/cloud/admin/user-management/rest/api-group-lifecycle/#api-users-account-id-manage-lifecycle-disable-post

How to use
1. Create a CSV file with the account IDs in that need to be deactivated
2. Run the script below
"""
  
#!/bin/bash
file=userstodeactivatetest.csv

header=false
while read line || [ -n "$line" ]
do
if [ "$header" = 'true' ];
then
header=false
continue
fi

account_id=`echo $line | cut -d ',' -f1`

echo "$account_id"
#to help troubleshoot, uncomment the below to check the data that is being sent
#url="https://api.atlassian.com/users/${account_id}/manage/lifecycle/disable"
#echo "$url"

curl --request POST \
--url "https://api.atlassian.com/users/$account_id/manage/lifecycle/disable" \
--header 'Authorization: Bearer ABCDE' \
--header 'Content-Type: application/json' \
--data '{}' -i

done <$file
