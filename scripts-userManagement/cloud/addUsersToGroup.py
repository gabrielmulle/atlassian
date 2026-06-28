"""
How to use
Open the script in a text file and replace
* instance
* username (your email)
* api_token 
* usersIds (the aaids of the users you want to add to the group)
* group_name (the name of the group you want users in)

Code below
"""

import requests
from requests.auth import HTTPBasicAuth
import time

instance = 'https://instance.atlassian.net'
username = 'gabe@email.com'
api_token = 'ATATT3xFfGF0aaaaaaa'

group_name = "groupHere"

users_ids = [
'712020:e9479bxxxxxxxxccf7',
'712020:e43bxxxxxxxxxx120df'
]

url = f"{instance}/rest/api/3/group/user?groupname={group_name}"

for account_id in users_ids:
    response = requests.post(
        url,
        auth=HTTPBasicAuth(username, api_token),
        headers={"Content-Type": "application/json"},
        json={"accountId": account_id}
    )

    if response.status_code == 201:
        print(f"{account_id} added to group {group_name}")
    else:
        print(
            f"{account_id} failed - "
            f"Status: {response.status_code} - "
            f"Response: {response.text}"
        )

    time.sleep(0.5)
