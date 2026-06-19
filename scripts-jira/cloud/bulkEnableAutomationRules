"""
Requirements
Need an input CSV file with these headers:
name,idUuid

To get only enabled rules:
- export (JSON) the rules from DC and cloud
- convert from JSON to CSV
- lookup by name to get only active rules

Note
To convert JSON to CSV, you can use jq on the terminal

brew install jq

command for cloud file
jq -r '
["name","idUuid"],
(.rules[] | [.name, .idUuid])
| @csv
' rulescloud.json > rulescloudnew.csv

command for dc file
jq -r '
["name","state"],
(.rules[] | [.name, .state])
| @csv
' rulesdc.json > rulesdcnew.csv
"""

import csv
import requests
import time

# ===== CONFIG =====
PRODUCT = "jira"
CLOUD_ID = "<INSTANCE ID>"

EMAIL = "<EMAIL>"
API_TOKEN = "<TOKEN>"

INPUT_CSV = "automation_rules.csv"
LOG_CSV = "enable_rules_log.csv"

SLEEP_SECONDS = 0.2
# ==================

BASE_URL = f"https://api.atlassian.com/automation/public/{PRODUCT}/{CLOUD_ID}/rest/v1"

auth = (EMAIL, API_TOKEN)

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

with open(INPUT_CSV, mode="r", encoding="utf-8-sig", newline="") as infile, \
     open(LOG_CSV, mode="w", encoding="utf-8", newline="") as logfile:

    reader = csv.DictReader(infile)

    required_columns = {"name", "idUuid"}
    missing = required_columns - set(reader.fieldnames or [])

    if missing:
        raise ValueError(f"Missing required columns in CSV: {missing}")

    writer = csv.DictWriter(logfile, fieldnames=[
        "name",
        "idUuid",
        "status_code",
        "result",
        "response"
    ])
    writer.writeheader()

    for row in reader:
        name = row["name"].strip()
        rule_uuid = row["idUuid"].strip()

        if not rule_uuid:
            writer.writerow({
                "name": name,
                "idUuid": rule_uuid,
                "status_code": "",
                "result": "SKIPPED",
                "response": "Missing idUuid"
            })
            print(f"SKIPPED: {name} | Missing idUuid")
            continue

        url = f"{BASE_URL}/rule/{rule_uuid}/state"

        payload = {
            "value": "ENABLED"
        }

        try:
            response = requests.put(
                url,
                headers=headers,
                auth=auth,
                json=payload
            )

            if response.status_code == 200:
                result = "SUCCESS"
            else:
                result = "FAILED"

            response_text = response.text

            writer.writerow({
                "name": name,
                "idUuid": rule_uuid,
                "status_code": response.status_code,
                "result": result,
                "response": response_text
            })

            print(
                f"{result}: {name} | {rule_uuid} | "
                f"HTTP {response.status_code} | {response_text}"
            )

        except Exception as e:
            writer.writerow({
                "name": name,
                "idUuid": rule_uuid,
                "status_code": "",
                "result": "ERROR",
                "response": str(e)
            })

            print(f"ERROR: {name} | {rule_uuid} | {e}")

        time.sleep(SLEEP_SECONDS)

print(f"\nDone. Log saved to: {LOG_CSV}")
