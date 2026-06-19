"""
Atlassian method, Source here, https://bitbucket.org/atlassianlabs/jira-read-only-mode-migrations/src/master/

Python method below
"""

import json
import requests

url = "http://jira server url" #without / in the end

# PAT is Personal Access Token, works for intances protected by API Constraints.
pat = ""
permission_scheme_id = 10000

headers = {
    "Authorization": f"Bearer {pat}",
    "Content-Type": "application/json"
}

def get_projects():
    return requests.get(url+"/rest/api/2/project", headers=headers).json()

def set_permission_scheme_for_project(project):
    return requests.put(url+f"/rest/api/2/project/{project['key']}/permissionscheme", data=json.dumps({"id": permission_scheme_id}, headers=headers))

for project in get_projects():
    set_permission_scheme_for_project(project)
