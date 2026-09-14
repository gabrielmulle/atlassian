import csv
import json
import requests
import urllib3

# Hide noisy security warnings from verify=False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://jira.instance.net"
pat = "tokenhere"
permission_scheme_id = 10140
csv_file_path = "readonlyprojects.csv"

headers = {
    "Authorization": f"Bearer {pat}",
    "Content-Type": "application/json"
}

def set_permission_scheme_for_project(project_id_or_key):
    payload = {"id": str(permission_scheme_id)}
    endpoint = f"{url}/rest/api/2/project/{project_id_or_key}/permissionscheme"
    
    print(f"Sending request to: {endpoint} ...")
    response = requests.put(endpoint, data=json.dumps(payload), headers=headers, verify=False)
    
    if response.status_code in [200, 204]:
        check_response = requests.get(endpoint, headers=headers, verify=False)
        if check_response.status_code == 200:
            current_scheme = check_response.json()
            if int(current_scheme.get('id', 0)) == permission_scheme_id:
                print(f"  ✅ Success! '{project_id_or_key}' is now set to: {current_scheme.get('name')}")
            else:
                print(f"  ⚠️ Jira accepted the request but ignored the change for '{project_id_or_key}'. Current scheme is still ID: {current_scheme.get('id')}")
        else:
            print(f"  ⚠️ Changed '{project_id_or_key}', but verification request failed.")
    else:
        print(f"  ❌ Failed to update {project_id_or_key}: {response.status_code} - {response.text}")

print(f"Opening {csv_file_path}...")

with open(csv_file_path, mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    
    first_row = next(reader, None)
    
    if first_row:
        target = first_row[0].strip()

        # If the first row contains a non-numeric string header like 'project_id', skip it. Otherwise, if it's already an ID (like 14697), process it immediately!
        if target.isdigit() or len(target) <= 10 and target.isalnum():
            print(f"Found target in row 1: {target}")
            set_permission_scheme_for_project(target)
        else:
            print(f"Skipping header row: {first_row}")
            
        for row in reader:
            if row:
                target = row[0].strip()
                if target:
                    print(f"Found target: {target}")
                    set_permission_scheme_for_project(target)
    else:
        print("Error: The CSV file appears to be completely empty.")
