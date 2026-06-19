"""
Python version
How to use
Create a csv file with the usernames of the users to be deleted, e.g users-to-delete.csv
PS: this script will generate a log file as an output, it is possible also to tail -f delete-users.log

Code below
"""
  
import logging
import requests
import json
import csv

user = "gmuller"
pw = "passhere"
header = {"Content-type": "application/json"}
url = "https://jira-qa2.instance.com"

logging.basicConfig(filename="delete-users.log", format='%(asctime)s %(message)s', filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def deleteUser(username):
    req = requests.delete("{}/rest/api/2/user?username={}".format(url, username), headers=header, auth=(user, pw), verify=False)
    if req.ok:
        logger.info("SUCCESS,{}".format(username))
    else:
        logger.error("FAILED,{},{},{}".format(username, req.text, req.status_code))

def main(csv_file):
    with open(csv_file) as csvfile:
        line = csv.reader(csvfile, delimiter=',')
        for row in line:
            user_name = row[0]
            deleteUser(user_name)

main("users-to-delete.csv")
