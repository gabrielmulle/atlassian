import csv
import json
import requests
import sys

tempo_token='zR64bJwXxUbMj'
api_token = 'EQRhFWowOh7ZpMe'
cloud_token = 'Rzr0BJ6cE7A6'
headers = {'Authorization': 'Bearer EQRhFWMwOh7ZpMe'}
offset = 0

def write_to_csv(worklog_id, project_key, issue_key, timestemp, startime, worklog_aaid, author_name, worklog_data, attributes):
    with open('metapack_worklogs_all_starttime.csv', 'a') as csv_file:
        file_writer = csv.writer(csv_file, delimiter=',')
        file_writer.writerow([worklog_id, project_key, issue_key, timestemp, startime, worklog_aaid, author_name, worklog_data, attributes])

write_to_csv("Worklog ID", "Project key", "Issue Key", "Timestemp", "StartTime", "Author AAID","Author Name", "Worklog", "Attributes")

while offset < 9999999:
    req = requests.get("<https://api.tempo.io/core/3/worklogs?offset={}&limit=1000&>".format(offset), headers=headers)
    if req.ok:
        all_data = req.json()['results']
    else:
        print(req.status_code)
        print(req.json())
        sys.exit()
    print(offset)
    if not all_data:
        print("No more data")
        offset = 9999999999
    else:
        for worklog in all_data:
            worklog_id = worklog['tempoWorklogId']
            worklog_time = worklog['timeSpentSeconds']
            worklog_timestamp = worklog['startDate']
            worklog_description = worklog['description']
            author_aaid = worklog['author']['accountId']
            attributes = worklog['attributes']
            start_time = worklog['startTime']
            try:
                author_name = worklog['author']['displayName']
            except:
                author_name = ""
            issue_key = worklog['issue']['key']
            worklog_format = "{};{};{};{};{}".format(worklog_description, worklog_timestamp, author_aaid, worklog_time, start_time)
            project_key = issue_key.split('-')[0]
            write_to_csv(worklog_id, project_key, issue_key, worklog_timestamp, start_time, author_aaid, author_name, worklog_format, attributes)
        offset += 1000

