#!/usr/bin/python3

import sys, os
import requests

def projects(base_url, aut):
    """Fetch a list of projects on an ODK Central server."""
    r = requests.get(f'{base_url}/v1/projects', auth = aut)
    return r

def forms(base_url, aut, projectId):
    """Fetch a list of forms in a project."""
    r = requests.get(f'{base_url}/v1/projects/{projectId}/forms', auth = aut)
    return r

def submissions(base_url, aut, projectId, formId):
    """Fetch a list of submission instances for a given form."""
    r = requests.get(f'{base_url}/v1/projects/{projectId}/forms/{formId}/submissions', auth = aut)
    return r
    
def csv(base_url, aut, projectId, formId):
    """Fetch a CSV file of the submissions to a survey form."""
    r = requests.get(f'{base_url}/v1/projects/{projectId}/forms/{formId}.csv', auth = aut)
    
def attachment_list(base_url, aut, projectId, formId, instanceId):
    """Fetch an individual media file attachment."""
    r = requests.get(f'{base_url}/v1/projects/{projectId}/forms/{formId}/submissions/{instanceId}/attachments', auth = aut)
    return r

def attachment(base_url, aut, projectId, formId, instanceId, filename):
    """Fetch a specific attachment by filename from a submission to a form."""
    r = requests.get(f'{base_url}/v1/projects/{projectId}/forms/{formId}/submissions/{instanceId}/attachments/{filename}', auth = aut)
    return r

if __name__ == '__main__':
    pass

    

    
