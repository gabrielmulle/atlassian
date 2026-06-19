"""
How to use
python3 extractPageIdFromSpaceKey.py <example.atlassian.net> <'space_key'>

Code below
"""

# Author: David Ingty, dingty@atlassian.net
# Date: 21 Jan 2021
# This script is for extracting the pageIds from a space, then saves them to a txt file
# This requires atlassian-python-api==2.7.0

from atlassian import Confluence
import sys
import json

cloud_url = sys.argv[1]
space_key = sys.argv[2]

confluence = Confluence(
    url='https://' + cloud_url,
    username='<EMAIL_ADDR>',
    password='<API_TOKEN>',
    api_version='cloud')

page_ids = []
data = confluence.get_all_pages_from_space(space_key)
for ele in data:
    if ele['id'] not in page_ids:
        page_ids.append(ele['id'])

with open('page_ids.txt', 'w') as f:
    for item in page_ids:
        f.write(item)
        f.write('\\n')
