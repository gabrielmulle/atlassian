"""
Notes
Since there is no official API endpoint to remove users from a cloud site, this script “simulate” an operation through the UI, so it uses the browser_cookie3 to do so.

Code below
"""
  
import sys, argparse
import browser_cookie3
import requests

cookies = browser_cookie3.chrome()

parser = argparse.ArgumentParser(description='Bulk delete users from a Cloud site')
parser.add_argument('cloud_site_id', type=str, help='Unique ID of the Cloud Site')
parser.add_argument('users_to_delete_file', type=str, help='File contains Atlassian Account IDs of the users who need to deleted. One User account in each line.')

args = parser.parse_args()

try:
	with open(args.users_to_delete_file, 'r') as fp:
		for aaid in iter(fp.readline, ''):
			url = 'https://admin.atlassian.com/gateway/api/adminhub/um/site/{}/users/{}'.format(args.cloud_site_id, aaid.strip())
			print('Deleting user: {}'.format(aaid))
			response = requests.delete(url, cookies = cookies)
			print("Response statsu code: {}".format(response.status_code))
			print("Response: {}".format(response))
except EnvironmentError: # parent of IOError, OSError *and* WindowsError where available
    print('Error opening input file; does it exist or corrupted?')
    print('')

"""
New code
To use: replace the site id in the code, create a CSV file with all aaids, put it in the same folder, and run the python code.
"""

import sys, argparse
import browser_cookie3
import requests

cookies = browser_cookie3.chrome()

try:
	with open("users.csv", 'r') as fp:
		for aaid in iter(fp.readline, ''):
			url = f'https://admin.atlassian.com/gateway/api/adminhub/um/site/<SITEID>/users/{aaid.strip()}'
			print('Deleting user: {}'.format(aaid))
			response = requests.delete(url, cookies = cookies)
			print("Response statsu code: {}".format(response.status_code))
			print("Response: {}".format(response))
except EnvironmentError: # parent of IOError, OSError *and* WindowsError where available
    print('Error opening input file; does it exist or corrupted?')
    print('')
