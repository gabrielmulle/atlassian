"""
Python version  
1. Create a CSV file with the account IDs in that need to be deactivated
2. Run the script below
"""
  
from requests import post
import pandas as pd

class Jira:
    apikey = "7BRbga0JaJgMPdr9kLDA"
    
    def getcsv(self, filename):
        csv = pd.read_csv(filename)
        return csv.to_dict()

    def endpoint(self, account_id):
        return f"https://api.atlassian.com/users/{account_id}/manage/lifecycle/disable"

    def disable_user(self, url):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.apikey}'
        }
        r = post(url, headers=headers)
        return r

jira = Jira()
users = jira.getcsv("users.csv")["account_id"].values()
for user in users:
    url = jira.endpoint(user)
    jira.disable_user(url)
