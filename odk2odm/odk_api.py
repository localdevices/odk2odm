#!/usr/bin/python3
"""Utilities for interacting with ODK Central API

These are functions that return replies from an ODK Central server. https://docs.getodk.org/central-intro/

These functions mostly return requests.Response() objects. That object contains status code of the request (200, 404, etc), and the data itself, as well as a number of other attributes.

Here's a great reference on how to use the returned objects: https://www.w3schools.com/python/ref_requests_response.asp

The base_url parameter is just the URL of the ODK Central server. The extra characters needed to actually reach the API ('/v1/') are built into the functions.

The aut parameter is a tuple of the username and password used to authenticate the requester on the server, in the form (username, password). The passwords are in plain text; ideally this should be a hash but I haven't gotten around to that.

Simple usage:
If you want to see if a server is working and you are able to reach it, use the projects function:

url = 'https://3dstreetview.org'
aut = ('myusername', 'mypassword')
r = fetch.projects(url, aut)
r.status_code

If all went well, that'll return '200'. If you got the username/password wrong (or aren't authorized on the server for whatever reason) it'll return '401', or '404' if the server isn't found at all.

To see the data:

r.json()

That'll return a JSON-formatted string with information about the projects on the server.

To see the information on a single project:

r.json()[0]

That'll return a dictionary with the attributes of the first project on the server.

To see the name of the first project:

r.json()[0]['name']

"""

import sys, os
import requests
import json
import zlib
import qrcode

import urllib

def projects(base_url, aut):
    """Fetch a list of projects on an ODK Central server."""
    url = f'{base_url}/v1/projects'
    return requests.get(url, auth = aut)

def project_id(base_url, aut, projectName):
    """Fetch the id of a project based on the name on an ODK Central server."""
    url = f'{base_url}/v1/projects'
    projects = requests.get(url, auth = aut).json()
    projectId = [p for p in projects if p['name']== projectName][0]['id']
    return projectId

def forms(base_url, aut, projectId):
    """Fetch a list of forms in a project."""
    url = f'{base_url}/v1/projects/{projectId}/forms'
    return requests.get(url, auth = aut)

def submissions(base_url, aut, projectId, formId):
    """Fetch a list of submission instances for a given form."""
    url = f'{base_url}/v1/projects/{projectId}/forms/{formId}/submissions'
    return requests.get(url, auth = aut)

def users(base_url, aut):
    """Fetch a list of users."""
    url = f'{base_url}/v1/users'
    return requests.get(url, auth = aut)

def app_users(base_url, aut, projectId):
    """Fetch a list of app-users."""
    url = f'{base_url}/v1/projects/{projectId}/app-users'
    return requests.get(url, auth = aut)

# Should work with ?media=false appended but doesn't.
# Probably a bug in ODK Central. Use the odata version; it works.
def csv_submissions(base_url, aut, projectId, formId):
    """Fetch a CSV file of the submissions to a survey form."""
    url = f'{base_url}/v1/projects/{projectId}/forms/{formId}/submissions.csv.zip'
    return requests.get(url, auth = aut)


def odata_submissions(base_url, aut, projectId, formId):
    """
    Fetch the submissions using the odata api. 
    use submissions.json()['value'] to get a list of dicts, wherein 
    each dict is a single submission with the form question names as keys.
    """    
    url = f'{base_url}/v1/projects/{projectId}/forms/{formId}.svc/Submissions'
    submissions = requests.get(url, auth = aut)
    return submissions


def attachment_list(base_url, aut, projectId, formId, instanceId):
    """Fetch an individual media file attachment."""
    url = f'{base_url}/v1/projects/{projectId}/forms/{formId}/submissions/'\
        f'{instanceId}/attachments'
    return requests.get(url, auth = aut)


def attachment(base_url, aut, projectId, formId, instanceId, filename):
    """Fetch a specific attachment by filename from a submission to a form."""
    url = f'{base_url}/v1/projects/{projectId}/forms/{formId}/submissions/'\
        f'{instanceId}/attachments/{filename}'
    return requests.get(url, auth = aut)

# POST 

def create_project(base_url, aut, project_name):
    """Create a new project on an ODK Central server"""
    url = f'{base_url}/v1/projects'
    return requests.post(url, auth = aut, json = {'name': project_name})

def create_app_user(base_url, aut, projectId, app_user_name = 'Surveyor'):
    """Create a new project on an ODK Central server"""
    url = f'{base_url}/v1/projects/{projectId}/app-users'
    return requests.post(url, auth = aut, json = {'displayName': app_user_name})


#Not sure if this is needed
def create_public_link(base_url, aut, projectId, formId, linkName):
    """Give access to anybody to submit a form"""
    url = f'{base_url}/v1/projects/{projectId}/forms/{formId}/public-links'
    return requests.post(url, auth = aut, json = {'displayName': linkName}) 


def give_access_app_users(base_url, aut, projectId):
    """Give all the app-users in the project access to all the forms in that project"""
    url = f'{base_url}/v1/projects/{projectId}/forms'
    forms = requests.get(url, auth = aut).json()

    for form in forms:
        formId = form['xmlFormId']
        url = f'{base_url}/v1/projects/{projectId}/app-users'
        app_users = requests.get(url, auth = aut).json()
        for user in app_users:
            actorId = user['id']        
            roleId = 2
            url = f'{base_url}/v1/projects/{projectId}/forms/{formId}/assignments/{roleId}/{actorId}' 
            requests.post(url, auth = aut)  


def delete_project(base_url, aut, project_id):
    """Permanently delete project from an ODK Central server. Probably don't."""
    url = f'{base_url}/v1/projects/{project_id}'
    return requests.delete(url, auth = aut)

###### Editing
def create_form(base_url, aut, projectId, path2Form):
    """Create a new form on an ODK Central server"""
    base_name = os.path.basename(path2Form)
    file_name = os.path.splitext(base_name)[0]
    form_file = open(path2Form, 'rb')
    #sheet = form_file.active

    headers = {
    'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    f'X-XlsForm-FormId-Fallback': file_name
    }
    url = f'{base_url}/v1/projects/{projectId}/forms?ignoreWarnings=true&publish=true'
    values = form_file

    # From the requests, gives the same error
    return requests.post(url, auth = aut, data = form_file, headers = headers)

def compress_qr_data(base_url, aut, qr_data):
    false = False
    true = True
    qr_data_bytes = json.dumps(qr_data).encode('utf-8')     
    qr_data_comp = zlib.compress(qr_data_bytes, level=9)
    img = qrcode.make(qr_data_bytes)
    img.save('MyQRCode1.png') 
    return qr_data_bytes

# Test QR settings data
false = False
true = True

qr_data = {
  "general": {
    "protocol": "google_sheets",
    "constraint_behavior": "on_finalize"
  },
  "admin": {
    "edit_saved": false
  }
}

###### editing until

if __name__ == '__main__':
    pass
