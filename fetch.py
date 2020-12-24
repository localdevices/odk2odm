#! /usr/bin/python3

import sys, os
import requests

def projects(base_url, authtuple):
    r = requests.get(f'{base_url}/v1/projects', auth = authtuple)
    return r

def forms(base_url, projectId, authtuple):
    r = requests.get(f'{base_url}/v1/projects/{projectId}/forms', auth = authtuple)
    return r

def submissions(base_url, projectId, formId, authtuple):
    r = requests.get(f'{base_url}/v1/projects/{projectId}/forms/{formId}/submissions', auth = authtuple)
    return r
    
def csv(base_url, projectId, formId, authtuple):
    r = requests.get(f'{base_url}/v1/projects/{projectId}/forms/{formId}.csv', auth = authtuple)
    
def attachment_list(base_url, projectId, formId, instanceId, authtuple):
    r = requests.get(f'{base_url}/v1/projects/{projectId}/forms/{formId}/submissions/{instanceId}/attachments', auth = authtuple)
    return r

def attachment(base_url, projectId, formId, instanceId, filename, authtuple):
    r = requests.get(f'{base_url}/v1/projects/{projectId}/forms/{formId}/submissions/{instanceId}/attachments/{filename}', auth = authtuple)
    return r

if __name__ == '__main__':
    pass

    

    
