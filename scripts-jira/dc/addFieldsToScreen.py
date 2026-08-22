"""
The script needs 2 files, examples below

input.csv (project and fields to be added)
projectKey,customFieldId
ABC,customfield_23417
DEF,customfield_17333

screenmapping.csv (ids mapping)
project_id,project_key,issue_type_screen_scheme_id,issue_type_screen_scheme_name,issue_type_id,issue_type_name,screen_scheme_id,screen_scheme_name,screen_id
22621,ABC,17006,Accounts Service Desk,,,17013,Accounts Service Desk Default Screen Scheme,16115
23220,DEF,21201,Accounts2 Service Desk,,,21604,Accounts2 Service Desk Default Screen Scheme,25804

"""

import csv
import requests
import time
from collections import defaultdict

# config

JIRA_BASE_URL = "https://jira.instance.com"
TOKEN = "NZ3cPfiUr7F"

TAB_NAME = "LegacyFields"
TARGET_SCREEN_TYPE = "edit"

session = requests.Session()
session.headers.update({
    "Content-Type": "application/json",
    "Authorization": f"Bearer {TOKEN}"
})

# read input.csv (projectKey, customFieldId)

def read_fields_csv(csv_file):
    grouped = defaultdict(list)
    with open(csv_file, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            grouped[row["projectKey"]].append(row["customFieldId"])
    return grouped

# read screenmapping.csv (projectKey, screen_id)

def read_screen_mapping(csv_file):
    mapping = {}
    with open(csv_file, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # get only default, empty issue_type_id
            if row["issue_type_id"] == "":
                mapping[row["project_key"]] = row["screen_id"]
    return mapping

# Jira functions

def get_or_create_tab(screen_id, tab_name):
    url = f"{JIRA_BASE_URL}/rest/api/2/screens/{screen_id}/tabs"
    r = session.get(url)
    r.raise_for_status()

    for tab in r.json():
        if tab["name"] == tab_name:
            return tab["id"]

    r = session.post(url, json={"name": tab_name})
    r.raise_for_status()
    return r.json()["id"]


def add_field_to_tab(screen_id, tab_id, field_id):
    url = f"{JIRA_BASE_URL}/rest/api/2/screens/{screen_id}/tabs/{tab_id}/fields"
    r = session.post(url, json={"fieldId": field_id})
    if r.status_code not in (200, 201, 204):
        raise Exception(f"Error {r.status_code}: {r.text}")

# execution

def main():
    fields_by_project = read_fields_csv("input.csv")
    screen_by_project = read_screen_mapping("screenmapping.csv")

    for project_key, field_ids in fields_by_project.items():
        print(f"\n🔧 Project: {project_key}")

        if project_key not in screen_by_project:
            print(f"⚠️  Project {project_key} not found on screenmapping.csv. Skipping.")
            continue

        screen_id = screen_by_project[project_key]
        print(f"➡️  Screen ID detected: {screen_id}")

        tab_id = get_or_create_tab(screen_id, TAB_NAME)
        print(f"➡️  Tab '{TAB_NAME}' (ID={tab_id})")

        for field_id in field_ids:
            try:
                add_field_to_tab(screen_id, tab_id, field_id)
                print(f"    ✔ Field added: {field_id}")
                time.sleep(0.8)
            except Exception as e:
                print(f"    ❌ Failed to add {field_id}: {e}")
                time.sleep(0.8)


if __name__ == "__main__":
    main()
