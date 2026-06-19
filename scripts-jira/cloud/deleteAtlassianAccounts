"""
Script 1

Requirements
pip3 install browser-cookie3 pip3 install requests

How to use
1. Replace the aaid1, aaid2, etc for real Atlassian Account id of the users
2. Run the code below
"""
  
import browser_cookie3
import requests

cookies = browser_cookie3.chrome()
users_to_delete = ['aaid1', 'aaid2']

for i in users_to_delete:
    url = 'https://admin.atlassian.com/gateway/api/users/{}'.format(i)
    print('Deleting user {}'.format(i))
    response = requests.delete(url, cookies = cookies)
    print(response)


"""
Script 2
"""

import sys, argparse, requests, json, browser_cookie3
from datetime import datetime
from csv import reader

def main():

    parser = argparse.ArgumentParser(description='Bulk delete users from an Atlassian Organisation')
    parser.add_argument('org_id', type=str, help='Unique ID of the Atlassian Organisation')
    parser.add_argument('org_api_key', type=str, help='API key created at the Org level')
    parser.add_argument('users_to_delete_file', type=str, help='File contains eamil address of the users. One user per line.')
    args = parser.parse_args()

    user_cookies = browser_cookie3.firefox()

    print('{} - Initiated Account Delete Process.....'.format(datetime.now()))

    delete_users=[]
    with open(args.users_to_delete_file, 'r') as read_users:
        for u in read_users:
            delete_users.append(u.strip().lower())

    # Get Atlassian Account ID of the each User
    aa_ids = get_user_aaid(args.org_id, args.org_api_key, delete_users)
    #print(aa_ids)
    #print(*aa_ids, sep = "\\n")

    # Now delete Atlassian Account of each user
    for user in aa_ids:
        if user["status"]!='closed':
            print('{} - Deleting User: {} [{}]'.format(datetime.now(),user["email"],user["aa_id"]))
            delete_user(user_cookies, user["aa_id"])
        else:
            print('{} - User: {} [{}] is already deleted. No action required.'.format(datetime.now(),user["email"],user["aa_id"]))

    print('{} - Finished Account Delete Process....'.format(datetime.now()))

def get_user_aaid(orgId, orgApiKey, usersList):
    orgUsers = []
    requestUrl = "https://api.atlassian.com/admin/v1/orgs/{}/users".format(orgId)

	# Set the HTTP headers for the request
    headers = {
	   "Accept": "application/json",
	   "Authorization": "Bearer " + orgApiKey
	}

    sys.stdout.write("{} - Getting Users Atlassian Accounts IDs\\n".format(datetime.now()))

	# Execute the HTTP request
    while True:
        response = requests.request(
            "GET",
            requestUrl,
            headers=headers
		)

		# Deserialize the response text as JSON
        responseJson = json.loads(response.text)

        for i in responseJson["data"]:
            if i["email"].lower() in usersList:
                orgUsers.append({'aa_id':i["account_id"],'email':i["email"].lower(),'status':i["account_status"]})

		# If there is pagination, re-define the requestUrl to the next page from the cursor
        if 'next' in list(responseJson["links"]):
            requestUrl = responseJson["links"]["next"]
        else:
            break

    return orgUsers

def delete_user(user_cookie, userAAID):

    requestUrl = "https://admin.atlassian.com/gateway/api/users/{}".format(userAAID)

    # REST API call
    response = requests.delete(
        requestUrl,
        cookies = user_cookie
    )

    if response.status_code == 204:
        sys.stdout.write('{} - SUCCESS: Atlassian Account [{}] has been deleted\\n'.format(datetime.now(), userAAID))
    else:
       sys.stdout.write('{} - ERROR: Atlassian Account [{}] cannot be delete. Response: {}\\n'.format(datetime.now(), userAAID, response.text))

if __name__ == "__main__":
        main()
