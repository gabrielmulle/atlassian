#!/bin/bash
cookie='ajs_user_id=f9a19594aa14102c5a82bf11e5ec99f8a51dfeb9; ajs_anonymous_id=3efa2da1; JSESSIONID=0167F57D4A3CADBFD; seraph.rememberme.cookie=3311870b7978; atlassian.xsrf.token=AF47-77ZL-0DVc8a81c_lin'

cat boards.csv | while read line;
do
echo "Changing admin of board $line"
curl -X PUT --header "$cookie" --header 'Content-Type: application/json' --header "Authorization: Bearer MzkwPKWYrrF5W/k" --url "https://jira.com/rest/greenhopper/1.0/rapidviewconfig/boardadmins" --data "{"id":$line,"boardAdmins":{"userKeys":["sa230506"],"groupKeys":[]}}" -i
sleep 2s
done
