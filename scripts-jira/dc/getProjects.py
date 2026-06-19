import requests 
import pandas as pd

# configuration
username = "<your.email@example.com>"
password = "<password_or_apikey_if_cloud>"
instance_url = "<instance_url_server_or_cloud>"

# project info
projects_url = instance_url + "/rest/api/2/project"
projects = requests.get(projects_url, auth=(username, password), params={"expand": "description,lead,issueTypes,url,projectKeys,permissions,insight"}, headers={"content-type":"application/json", "accept":"application/json"}).json()

new_list_of_projects = []
for p in projects:
    pkey = p["key"]
    jql = f"project = {pkey}"
    p["issuecount"] = requests.get(instance_url + "/rest/api/2/search", auth=(username, password), params={"jql": jql}).json()["total"]
    new_list_of_projects.append(p)

# save it as csv
df = pd.DataFrame(new_list_of_projects)
df.to_csv("projects.csv", index=False)
