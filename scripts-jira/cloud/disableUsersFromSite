import sys, argparse
import browser_cookie3
import requests

cookies = browser_cookie3.firefox()

parser = argparse.ArgumentParser(description='Bulk deactivate users from a Cloud site')
parser.add_argument('cloud_site_id', type=str, help='Unique ID of the Cloud Site')
parser.add_argument('users_to_deactivate_file', type=str, help='File contains Atlassian Account IDs of the users who need to deactivated. One User account in each line.')

args = parser.parse_args()

try:
	with open(args.users_to_deactivate_file, 'r') as fp:
		for aaid in iter(fp.readline, ''):
			url = 'https://admin.atlassian.com/gateway/api/adminhub/um/site/{}/users/{}/deactivate'.format(args.cloud_site_id, aaid.strip())
			print('Disabling user: {}'.format(aaid))
			response = requests.post(url, cookies = cookies)
			print("Response statsu code: {}".format(response.status_code))
			print("Response: {}".format(response))
except EnvironmentError: # parent of IOError, OSError *and* WindowsError where available
    print('Error opening input file; does it exist or corrupted?')
    print('')
