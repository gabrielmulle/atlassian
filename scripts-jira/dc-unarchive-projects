import requests
import json
from requests.auth import HTTPBasicAuth
import sys

def unarchive_projects(base_url, username, api_token, project_keys):
    """
    Unarchive multiple Jira projects by their project keys
    
    Args:
        base_url (str): Your Jira instance URL (e.g., "https://your-domain.atlassian.net")
        username (str): Your Jira username/email
        api_token (str): Your Jira API token or password
        project_keys (list): List of project keys to unarchive
    """
    # Create authentication
    auth = HTTPBasicAuth(username, api_token)
    
    # Set headers
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # Counter for successful operations
    success_count = 0
    failed_projects = []
    
    for project_key in project_keys:
        try:
            # Construct the URL for the archive/unarchive operation
            url = f"{base_url}/rest/api/2/project/{project_key}/archiving"
            
            # Payload to unarchive the project
            payload = json.dumps({
                "archived": False  # False means unarchive
            })
            
            # Make the API request
            response = requests.put(url, data=payload, headers=headers, auth=auth)
            
            # Check if the request was successful
            if response.status_code == 204 or response.status_code == 200:
                print(f"Project {project_key} successfully unarchived.")
                success_count += 1
            else:
                print(f"Failed to unarchive project {project_key}. Status code: {response.status_code}")
                print(f"Response: {response.text}")
                failed_projects.append(project_key)
                
        except Exception as e:
            print(f"Error occurred while unarchiving project {project_key}: {str(e)}")
            failed_projects.append(project_key)
    
    # Summary
    print("\n--- Summary ---")
    print(f"Total projects processed: {len(project_keys)}")
    print(f"Successfully unarchived: {success_count}")
    print(f"Failed: {len(failed_projects)}")
    
    if failed_projects:
        print("\nFailed projects:")
        for key in failed_projects:
            print(f"- {key}")

if __name__ == "__main__":
    # Configuration - replace these values with your Jira instance details
    JIRA_BASE_URL = "https://your-jira-instance.com"  # Change this to your Jira URL
    JIRA_USERNAME = "your_username"  # Change this to your Jira username/email
    JIRA_API_TOKEN = "your_api_token"  # Change this to your API token or password
    
    # List of project keys to unarchive
    PROJECT_KEYS = [
        "PROJ1",
        "PROJ2",
        "PROJ3",
        # Add more project keys as needed
    ]
    
    # Alternatively, you can load project keys from a text file (one key per line)
    # Uncomment the following section if you want to use this approach
    """
    try:
        with open('project_keys.txt', 'r') as file:
            PROJECT_KEYS = [line.strip() for line in file if line.strip()]
        print(f"Loaded {len(PROJECT_KEYS)} project keys from file.")
    except FileNotFoundError:
        print("Error: project_keys.txt file not found.")
        sys.exit(1)
    """
    
    # Execute the unarchive operation
    unarchive_projects(JIRA_BASE_URL, JIRA_USERNAME, JIRA_API_TOKEN, PROJECT_KEYS)
