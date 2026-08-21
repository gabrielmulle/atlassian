"""
This script uses a csv file with the required projects, and their screen ids, example below:
project_key,screen_id
ABCD,10171
EFGH,10152
"""

import csv
import requests
import time

from requests.auth import HTTPBasicAuth

# config Jira cloud

JIRA_BASE_URL = "https://instance.atlassian.net"
JIRA_EMAIL = "user@email.com"
JIRA_API_TOKEN = "<token>"

TAB_NAME = "LegacyFields"

TIMEOUT = 30
RETRIES = 3

session = requests.Session()
session.auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
session.headers.update({
    "Accept": "application/json"
})

# safe request, timeout + retry

def safe_request(method, url, **kwargs):
    for attempt in range(RETRIES):
        try:
            return session.request(method, url, timeout=TIMEOUT, **kwargs)

        except requests.exceptions.ReadTimeout:
            print(f"⏳ Timeout... retrying ({attempt + 1}/{RETRIES})")
            time.sleep(2)

    raise Exception("Request failed after retries due to timeout")

# csv reader

def read_screen_mapping(csv_file):
    mapping = {}
    with open(csv_file, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            mapping[row["project_key"]] = row["screen_id"]
    return mapping

# jira functions

def get_tab_id_if_exists(screen_id, tab_name):
    url = f"{JIRA_BASE_URL}/rest/api/3/screens/{screen_id}/tabs"
    r = safe_request("GET", url)
    r.raise_for_status()

    for tab in r.json():
        if tab["name"] == tab_name:
            return tab["id"]

    return None


def delete_tab(screen_id, tab_id):
    url = f"{JIRA_BASE_URL}/rest/api/3/screens/{screen_id}/tabs/{tab_id}"
    r = safe_request("DELETE", url)

    if r.status_code not in (204,):
        raise Exception(f"Error {r.status_code}: {r.text}")

# execution

def main():
    screen_by_project = read_screen_mapping("screenmappingcloud.csv")

    for project_key, screen_id in screen_by_project.items():
        print(f"\n🔧 Project: {project_key}")
        print(f"➡️  Screen ID: {screen_id}")

        try:
            tab_id = get_tab_id_if_exists(screen_id, TAB_NAME)

            if not tab_id:
                print(f"⚠️  Tab '{TAB_NAME}' not found. Skipping.")
                continue

            delete_tab(screen_id, tab_id)
            print(f"✅ Tab '{TAB_NAME}' removed (ID={tab_id})")

        except Exception as e:
            print(f"❌ Error for project {project_key}: {e}")

        # Rate limit protection
        time.sleep(2)


if __name__ == "__main__":
    main()
