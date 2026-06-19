""" 
How to use
1. Place all project keys from the projects you want to delete in a CSV file
2. Run the script below
"""

import requests
from requests.auth import HTTPBasicAuth
import csv

# Inputs
username= 'email' #your email
password= 'token' #your token
csv_file= 'projectkey.csv'

base_url= 'careerbuilder.atlassian.net' #The instance URL

auth = HTTPBasicAuth(username, password)
headers = {'Content-Type': 'application/json'}

count = 1

with open(csv_file, 'r') as file:

    reader = csv.DictReader(file)

    for entry in reader:

      projectkey = entry['projectkey']

      url = 'https://' + base_url + '/rest/api/3/project/' + str(projectkey)

      r = requests.delete(url, auth=auth, headers=headers)

      print(str(r.status_code) + ' - ' + str(projectkey) + ' - ' + str(count))

      count = count + 1
