#!/bin/python3

# Copyright (c) 2022 Humanitarian OpenStreetMap Team
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     Odkconvert is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with Odkconvert.  If not, see <https:#www.gnu.org/licenses/>.
#

import logging
import epdb
import argparse
import sys, os
import requests
from requests.auth import HTTPBasicAuth
import json
import zlib
import codecs
import urllib

general = {
    "form_update_mode": "match_exactly",
    "autosend": "wifi_and_cellular",
}


class OdkCentral(object):
    def __init__(self, url=None, user=None, passwd=None):
        """A Class for accessing an ODK Central server via it's REST API"""
        self.url = url
        self.user = user
        self.passwd = passwd
        # These are settings used by ODK Collect
        self. general = {
            "form_update_mode": "match_exactly",
            "autosend": "wifi_and_cellular",
        }
        # If their is a config file with authentication setting, use that
        # so we don't have to supply this all the time.
        home = os.getenv("HOME")
        config = ".odkcentral"
        filespec = home + "/" + config
        if os.path.exists(filespec):
            file = open(filespec, "r")
            for line in file:
                # Support embedded comments
                if line[0] == "#":
                    continue
                # Read the config file for authentication settings
                tmp = line.split("=")
                if tmp[0] == "url":
                    self.url = tmp[1].strip ('\n')
                if tmp[0] == "user":
                    self.user = tmp[1].strip ('\n')
                if tmp[0] == "passwd":
                    self.passwd = tmp[1].strip ('\n')
        # Base URL for the REST API
        self.version = "v1"
        self.base = self.url + "/" + self.version + "/"

        self.auth = HTTPBasicAuth(self.user, self.passwd)
        # self.auth = (self.user, self.passwd)
        # self.login = {'email': self.user, 'password': self.passwd}

        # Use a persistant connect, better for multiple requests
        self.session = requests.Session()

    def authenticate(self, url=None, user=None, passwd=None):
        """Setup authenticate to an ODK Central server"""
        if not self.url:
            self.url = url
        if not self.user:
            self.user = user
        if not self.passwd:
            self.passwd = passwd
        # Enable persistent connection, create a cookie for this session
        self.session.headers.update({'accept': 'odkcentral'})

        # Connect to the server
        return self.session.get(self.url, auth=self.auth)    

    def listProjects(self):
        """Fetch a list of projects on an ODK Central server."""
        url = self.base + "projects"
        print(url, self.auth)
        return self.session.get(url, auth=self.auth)   

    def dump(self):
        """Dump interbal data structures, for debugging purposes only"""
        print("URL: %s" % self.url)
        print("User: %s" % self.user)
        print("Passwd: %s" % self.passwd)
        print("REST URL: %s" % self.base)


class OdkProject(OdkCentral):
    """Class to manipulate a project on an ODK Central server"""
    def __init__(self):
        super().__init__()
        self.id = None

    def listForms(self):
        """Fetch a list of forms in a project on an ODK Central server."""
        return self.session.get(self.base, auth=self.auth)

    def listAppUsers(self):
        """Fetch a list of app users in a project on an ODK Central server."""
        return self.session.get(self.base, auth=self.auth)

    def getSubmissions(self, projectId, formId):
        """Fetch a list of submission instances for a given form."""
        url = f'{self.base}/v1/projects/{projectId}/forms/{formId}/submissions'


# This following code is only for debugging purposes, since his is easier
# to use a debugger with instead of pytest.
if __name__ == '__main__':
    # Enable logging to the terminal by default
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)

    # odk = OdkCentral()
    # odk.dump()

    project = OdkProject()
    au = project.authenticate()
    print(au)
    pr = project.listProjects()
    print(pr)

