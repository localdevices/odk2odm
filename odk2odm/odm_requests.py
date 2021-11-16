import json

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

ODM_TASK_DEFAULT_OPTIONS = {
    "dtm": True,
    "dsm": True,
    "feature-quality": "ultra",  # Set feature extraction quality. Higher quality generates better features, but requires more memory and takes longer
    "matcher-distance": 20,  # Good for street level photography. Will be changed when OpenSfM eventually is updated and has better defaults
    "matcher-neighbors": 800,  # Good Necessary for street level photography. Will be changed when OpenSfM eventually is updated and has better defaults
    "mesh-octree-depth": 14,  # Memory and CPU intensive but much nicer detail in meshes
    "mesh-size": 400000,  # Memory intensive. Could probably be turned up louder
    "min-num-features": 24000,  # One of the more important options: it improves matching significantly in complicated scenes.
    "pc-geometric": True,  # Cleans the final model a bit based on visibility tests
    "pc-quality": "ultra",  #Memory and CPU intensive but much nicer detail in point cloud
}
ODM_TASK_DEFAULT_OPTIONS_LIST = [{"name": k, "value": v} for k, v in ODM_TASK_DEFAULT_OPTIONS.items()]


def get_token_auth(base_url, username, password):
    """
    Retrieve a 24-hr valid access token for provided WebODM base_url
    :param base_url: str - base url of WebODM server
    :param username: str - user name
    :param password: str - password
    :return: http response
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


def get_options(base_url, token):
    """
    Get list of processing options for NodeODM
    :param base_url: str - base url of WebODM server
    :param token: str - 24-hr token (see token_auth)
    :return: http response

    """
    url = f"{base_url}/api/processingnodes/options/"
    res = requests.get(
        url,
        headers={'Authorization': 'JWT {}'.format(token)},
    )
    return res

def get_projects(base_url, token):
    """
    Get list of projects belonging to server / user
    :param base_url: str - base url of WebODM server
    :param token: str - 24-hr token (see token_auth)
    :return: http response

    """
    url = f"{base_url}/api/projects"
    res = requests.get(
        url,
        headers={'Authorization': 'JWT {}'.format(token)},
    )
    return res


def get_project(base_url, token, project_id):
    """
    Get details of specific project, including list of tasks
    :param base_url: str - base url of WebODM server
    :param token: str - 24-hr token (see token_auth)
    :param project_id: int - id of project
    :return: http response

    """
    url = f"{base_url}/api/projects/{project_id}"
    res = requests.get(
        url,
        headers={'Authorization': 'JWT {}'.format(token)},
    )
    return res


def post_project(base_url, token, data={}):
    """
    Post request for new project.
    :param base_url: str - base url of WebODM server
    :param token: str - 24-hr token (see token_auth)
    :param data: dict - must contain "name" and can contain "description" for the project (see https://docs.webodm.org/#create-a-project)
    :return: http response

    """
    url = f"{base_url}/api/projects/"
    res = requests.post(
        url,
        headers={'Authorization': 'JWT {}'.format(token)},
        data=data
    )
    return res

def get_task(base_url, token, project_id, task_id):
    """
    Get details of a task belonging to a project (See https://docs.webodm.org/#task)
    :param base_url: str - base url of WebODM server
    :param token: str - 24-hr token (see token_auth)
    :param project_id: int - id of project
    :param task_id: str (uuid) - the uuid belonging to the task to retrieve
    :return: http response

    """
    url = f"{base_url}/api/projects/{project_id}/tasks/{task_id}/"
    res = requests.get(
        url,
        headers={'Authorization': 'JWT {}'.format(token)},
    )
    return res

def get_thumbnail(base_url, token, project_id, task_id, filename):
    url = f"{base_url}/api/projects/{project_id}/tasks/{task_id}/images/thumbnail/{filename}"
    res = requests.get(
        url,
        headers={'Authorization': 'JWT {}'.format(token)},
    )
    return res

def get_image(base_url, token, project_id, task_id, filename):
    url = f"{base_url}/api/projects/{project_id}/tasks/{task_id}/images/download/{filename}"
    res = requests.get(
        url,
        headers={'Authorization': 'JWT {}'.format(token)},
    )
    return res

def get_options(base_url, token):
    url = f"{base_url}/api/processingnodes/options/"
    res = requests.get(
        url,
        headers={'Authorization': 'JWT {}'.format(token)},
    )
    return res

def patch_task(base_url, token, project_id, task_id, data={}, files={}):
    """
    Patch existing task settings in a project (See https://docs.webodm.org/#update-a-task)
    :param base_url: str - base url of WebODM server
    :param token: str - 24-hr token (see token_auth)
    :param project_id: int - id of project
    :param data: dict - contains details of task such as a "name", and a dict "options" to pass to NodeODM, pass "partial": True to only create an updateable task without submitting it
    :param files: list - contains files in multipart format, see https://docs.webodm.org/#how-to-process-images for an example, leave empty when you want to provide files one by one in a partial task
    :return: http response
    """
    url = f"{base_url}/api/projects/{project_id}/tasks/{task_id}/"
    if "options" in data:
        # serialize options before passing
        data["options"] = json.dumps(data["options"])
    res = requests.patch(
        url,
        headers={'Authorization': 'JWT {}'.format(token)},
        data=data,
        files=files,
    )
    return res


def post_task(base_url, token, project_id, data={}, files=[]):
    """
    Post a new task in a project (See https://docs.webodm.org/#create-a-task)
    :param base_url: str - base url of WebODM server
    :param token: str - 24-hr token (see token_auth)
    :param project_id: int - id of project
    :param data: dict - contains details of task such as a "name", and a dict "options" to pass to NodeODM, pass "partial": True to only create an updateable task without submitting it
    :param files: list - contains files in multipart format, see https://docs.webodm.org/#how-to-process-images for an example, leave empty when you want to provide files one by one in a partial task
    :return: http response

    """
    url = f"{base_url}/api/projects/{project_id}/tasks/"
    headers = {'Authorization': 'JWT {}'.format(token)}
    if not("options" in data):
        # set a good set of default options in case user does not provide these
        data["options"] = ODM_TASK_DEFAULT_OPTIONS_LIST
    # serialize options before passing
    data["options"] = json.dumps(data["options"])
    res = requests.post(
        url,
        headers=headers,
        data=data,
        files=files,
    )
    return res

def post_upload(base_url, token, project_id, task_id, fields={}):
    """
    Post a new upload of a photo (.JPG) in an existing task with "partial": True in a project. Undocumented in https://docs.webodm.org/
    :param base_url: str - base url of WebODM server
    :param token: str - 24-hr token (see token_auth)
    :param project_id: int - id of project
    :param task_id: str (uuid) - the uuid belonging to the task to retrieve
    :param fields: dict - must contain the following recipe: {"images": <name of image file.JPG>, <bytestream of image>, 'image/jpg')}
    :return: http response

    """
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

def get_asset(base_url, token, project_id, task_id, asset):
    url = f"{base_url}/api/projects/{project_id}/tasks/{task_id}/download/{asset}"
    res = requests.get(
        url,
        headers={'Authorization': 'JWT {}'.format(token)},
    )
    return res


def post_commit(base_url, token, project_id, task_id):
    """
    Post a commit for an existing task, with "partial": True, that already contains uploaded photos. Undocumented in https://docs.webodm.org/
    :param base_url: str - base url of WebODM server
    :param token: str - 24-hr token (see token_auth)
    :param project_id: int - id of project
    :param task_id: str (uuid) - the uuid belonging to the task to retrieve
    :return: http response

    """
    url = f"{base_url}/api/projects/{project_id}/tasks/{task_id}/commit/"
    headers = {'Authorization': 'JWT {}'.format(token)}
    res = requests.post(
        url,
        headers=headers,
    )
    return res


def post_restart(base_url, token, project_id, task_id):
    """
    Post a restart for an existing task. Undocumented in https://docs.webodm.org/
    :param base_url: str - base url of WebODM server
    :param token: str - 24-hr token (see token_auth)
    :param project_id: int - id of project
    :param task_id: str (uuid) - the uuid belonging to the task to retrieve
    :return: http response

    """
    url = f"{base_url}/api/projects/{project_id}/tasks/{task_id}/restart/"
    headers = {'Authorization': 'JWT {}'.format(token)}
    res = requests.post(
        url,
        headers=headers,
    )
    return res


def post_cancel(base_url, token, project_id, task_id):
    """
    Post a cancel for an existing running task
    :param base_url: str - base url of WebODM server
    :param token: str - 24-hr token (see token_auth)
    :param project_id: int - id of project
    :param task_id: str (uuid) - the uuid belonging to the task to retrieve
    :return: http response

    """
    url = f"{base_url}/api/projects/{project_id}/tasks/{task_id}/cancel/"
    headers = {'Authorization': 'JWT {}'.format(token)}
    res = requests.post(
        url,
        headers=headers,
    )
    return res


def delete_task(base_url, token, project_id, task_id):
    """
    Delete an existing task in existing project
    :param base_url: str - base url of WebODM server
    :param token: str - 24-hr token (see token_auth)
    :param project_id: int - id of project
    :param task_id: str (uuid) - the uuid belonging to the task to retrieve
    :return: http response
POST /api/projects/{project_id}/tasks/{task_id}/remove/
    """
    url = f"{base_url}/api/projects/{project_id}/tasks/{task_id}/remove/"
    headers = {'Authorization': 'JWT {}'.format(token)}
    res = requests.post(
        url,
        headers=headers,
    )
    return res

def delete_project(base_url, token, project_id):
    """
    Delete an existing project
    :param base_url: str - base url of WebODM server
    :param token: str - 24-hr token (see token_auth)
    :param project_id: int - id of project
    :return: http response
    DELETE /api/projects/{project_id}
    """
    url = f"{base_url}/api/projects/{project_id}"
    headers = {'Authorization': 'JWT {}'.format(token)}
    res = requests.delete(
        url,
        headers=headers,
    )
    return res
