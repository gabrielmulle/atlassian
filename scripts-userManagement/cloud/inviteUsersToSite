"""
How to use
Create a CSV with the users email and display name
email,displayName
inviteuser1@test.com,inviteuser1@test.com
inviteuser2@test.com,inviteuser2@test.com
inviteuser3@test.com,inviteuser3@test.com
inviteuser4@test.com,inviteuser4@test.com
inviteuser5@test.com,inviteuser5@test.com

Code below
"""

import requests
from requests.auth import HTTPBasicAuth
import csv

# Inputs
username= 'email' #your email
password= 'token' #your token
csv_file= 'userlist.csv'
base_url= 'instance.atlassian.net' #The instance URL
auth = HTTPBasicAuth(username, password)
headers = {'Content-Type': 'application/json'}

count = 0
with open(csv_file, 'r') as file:
    reader = csv.DictReader(file)
    for entry in reader:
      email = entry['email']
      displayName = entry['displayName']
      url = 'https://' + base_url + '/rest/api/3/user'
      json_data = { 'emailAddress': email, 'displayName': displayName, 'notification': 'true'}
      r = requests.post(url, json=json_data, auth=auth, headers=headers)
      print(str(r.status_code) + ' - ' + str(email) + ' - ' + str(count))
      count = count + 1
