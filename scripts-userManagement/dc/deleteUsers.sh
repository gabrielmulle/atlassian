"""
Shell version
Tested in Confluence server instance
"""
  
cat conf-users-to-delete.csv | while read line;
do
    echo "Deleting $line"
    sleep 1
    curl  -X POST --url "https://example.com/admin/users/removeuser-confirm.action" \\
    -H 'content-type: application/x-www-form-urlencoded' \\
    -H 'cookie: AWSALBAPP-1=_remove_; AWSALBAPP-2=_remove_; AWSALBAPP-3=_remove_; seraph.confluence=223739905%; mywork.tab.tasks=false; JSESSIONID=; AWSALBAPP-0=/gqo=' \\
    --data-raw "atl_token=162e77username=$line&confirm=Delete" \\
    --write-out '%{http_code}\\n' --silent --show-error --output /dev/null
done | tee -a conf-deletion-logs.txt
