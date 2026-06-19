import requests
import time

# Replace these values with your specific organization (orgId), group (groupId), and API key (generated from the organization)
org_id = "6e2646c4-ff89-4978-816f-a525b236b1d0"
group_id = "a9068c9a-1649-4026-9205-6ec118fa27f4"
api_key = "ATCTT3xFf4613"

# Base URL for the API endpoint
base_url = f"<https://api.atlassian.com/admin/v1/orgs/{org_id}/directory/groups/{group_id}/memberships>"

# Set the headers with your API key for auth
headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json"
}

# List of account IDs for users you want to remove from the group
user_account_ids = ["712020:a6667032-4a4c-4e63-a71f",
"712020:043f58c3-d993-4222-a1b3"]

# Iterate through the list of user account IDs and send DELETE requests for each user
for account_id in user_account_ids:
    url = f"{base_url}/{account_id}"

    response = requests.delete(url, headers=headers)

    if response.status_code == 200:
        print(f"User with account ID {account_id} removed successfully from the group.")
    else:
        print(f"Failed to remove user with account ID {account_id}. Status code: {response.status_code}")
    
    time.sleep(0.2)
