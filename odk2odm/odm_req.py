import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


def token_auth(base_url, username, password):
    """
    Retrieve a 24-hr valid access token for provided WebODM base_url
    :param base_url:
    :param username:
    :param password:
    :return:
    """
    url = f"{base_url}/api/token-auth/"
    res = requests.post(
        url,
        data={
            "username": username,
            "password": password
        }
    )
    return res



def get_projects(base_url, token):
    url = f"{base_url}/api/projects"
    res = requests.get(
        url,
        headers={'Authorization': 'JWT {}'.format(token)},
    )
    return res


def get_project(base_url, token, project_id):
    url = f"{base_url}/api/projects/{project_id}"
    res = requests.get(
        url,
        headers={'Authorization': 'JWT {}'.format(token)},
    )
    return res


def post_project(base_url, token, data={}):
    url = f"{base_url}/api/projects/"
    res = requests.post(
        url,
        headers={'Authorization': 'JWT {}'.format(token)},
        data=data
    )
    return res

def get_task(base_url, token, project_id, task_id):
    url = f"{base_url}/api/projects/{project_id}/tasks/{task_id}/"
    res = requests.get(
        url,
        headers={'Authorization': 'JWT {}'.format(token)},
    )
    return res

def post_task(base_url, token, project_id, data={}):
    url = f"{odmconfig.host}:{odmconfig.port}/api/projects/{project_id}/tasks/"
    headers = {'Authorization': 'JWT {}'.format(token)}
    res = requests.post(
        url,
        headers=headers,
        data=data,
    )
    return res

def post_upload(base_url, token, project_id, task_id, fields={}):
    url = f"{base_url}/api/projects/{project_id}/tasks/{task_id}/upload/"
    m = MultipartEncoder(
        fields=fields
        )
    headers = {
        'Authorization': 'JWT {}'.format(token),
        'Content-type': m.content_type,
    }
    res = requests.post(
        url,
        data=m,
        headers=headers,
    )
    return res


def post_commit(base_url, token, project_id, task_id):
    url = f"{base_url}/api/projects/{project_id}/tasks/{task_id}/commit/"
    headers = {'Authorization': 'JWT {}'.format(token)}
    res = requests.post(
        url,
        headers=headers,
    )
    return res