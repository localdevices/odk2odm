#!/usr/bin/python3

import sys, os
import requests

def projects(base_url, aut):
    """Fetch a list of projects on an ODK Central server."""
    url = f'{base_url}/v1/projects'
    return requests.get(url, auth = aut)

def forms(base_url, aut, projectId):
    """Fetch a list of forms in a project."""
    url = f'{base_url}/v1/projects/{projectId}/forms'
    return requests.get(url, auth = aut)

def submissions(base_url, aut, projectId, formId):
    """Fetch a list of submission instances for a given form."""
    url = f'{base_url}/v1/projects/{projectId}/forms/{formId}/submissions'
    return requests.get(url, auth = aut)

# Should work with ?media=false appended but doesn't. Use the odata version.
def csv_submissions(base_url, aut, projectId, formId):
    """Fetch a CSV file of the submissions to a survey form."""
    f'{base_url}/v1/projects/{projectId}/forms/{formId}/submissions.csv.zip'
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
        '{instanceId}/attachments'
    return requests.get(url, auth = aut)

def attachment(base_url, aut, projectId, formId, instanceId, filename):
    """Fetch a specific attachment by filename from a submission to a form."""
    url = f'{base_url}/v1/projects/{projectId}/forms/{formId}/submissions/'\
        '{instanceId}/attachments/{filename}'
    return requests.get(url, auth = aut)

if __name__ == '__main__':
    pass

    

    
