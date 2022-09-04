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
from datetime import tzinfo, datetime


class OdkCentral(object):
    def __init__(self, url=None, user=None, passwd=None):
        """A Class for accessing an ODK Central server via it's REST API"""
        self.url = url
        self.user = user
        self.passwd = passwd
        # These are settings used by ODK Collect
        self.general = {
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

        # Authentication data
        self.auth = HTTPBasicAuth(self.user, self.passwd)

        # Use a persistant connect, better for multiple requests
        self.session = requests.Session()

        # These are just cached data from the queries
        self.projects = dict()
        self.users = None

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
        """Fetch a list of projects from an ODK Central server, and
        store it as an indexed list."""
        logging.info("Getting a list of projects from %s" % self.url)
        url = self.base + "projects"
        result = self.session.get(url, auth=self.auth)
        projects = result.json()
        for project in projects:
            self.projects[project['id']] = project
        return result

    def createProject(name=None):
        """Create a new project on an ODK Central server"""
        url = f'{self.base}/v1/projects'
        result = self.session.post(url, auth=self.auth, json={'name': name})

    def listUsers(self):
        """Fetch a list of users on the ODK Central server"""
        logging.info("Getting a list of users from %s" % self.url)
        url = self.base + "users"
        result = self.session.get(url, auth=self.auth)
        self.users = result.json()
        return result
        
    def dump(self):
        """Dump internal data structures, for debugging purposes only"""
        # print("URL: %s" % self.url)
        # print("User: %s" % self.user)
        # print("Passwd: %s" % self.passwd)
        print("REST URL: %s" % self.base)
        print("There are %d projects on this server" % len(self.projects))
        for id, data in self.projects.items():
            print("\t %s: %s" % (id, data['name']))
        if self.users:
            print("There are %d users on this server" % len(self.users))
            for data in self.users:
                print("\t %s: %s" % (data['id'], data['email']))
        else:
            print("There are no users on this server")


class OdkProject(OdkCentral):
    """Class to manipulate a project on an ODK Central server"""
    def __init__(self, data=None):
        super().__init__()
        self.forms = None
        self.submissions = None
        self.data = None
        self.appusers = None
        if not data:
            self.data = data

    def getData(self, keyword):
        return self.data[keyword]

    def listForms(self, id=None):
        """Fetch a list of forms in a project on an ODK Central server."""
        url = self.base + f'projects/{id}/forms'
        result = self.session.get(url, auth=self.auth)
        self.forms = result.json()
        return result

    def listSubmissions(self, projectId, formId):
        """Fetch a list of submission instances for a given form."""
        url = self.base + f'projects/{projectId}/forms/{formId}/submissions'
        result = self.session.get(url, auth=self.auth)
        self.submissions = result.json()
        return result
    
    def getSubmission(self, projectId=None, formId=None, disk=False):
        """Fetch a CSV file of the submissions without media to a survey form."""
        url = self.base + f'projects/{projectId}/forms/{formId}/submissions.csv'
        result = self.session.get(url, auth=self.auth)
        if result.status_code == 200:
            if disk:
                now = datetime.now()
                timestamp = f'{now.year}_{now.hour}_{now.minute}'
                id = self.forms[0]['xmlFormId']
                filespec = f'{id}_{timestamp}.csv'
                try:
                    file = open(filespec, "xb")
                    file.write(result.content)
                except FileExistsError:
                    file = open(filespec, "wb")
                    file.write(result.content)
                logging.info("Wrote CSV file %s" % filespec)
                file.close()
            return result.content
        else:
            logging.error(f'Submissions for {projectId}, Form {formId}' + "doesn't exist")
            return None

    def getSubmissionMedia(self, projectId, formId):
        """Fetch a ZIP file of the submissions with media to a survey form."""
        url = self.base + f'projects/{projectId}/forms/{formId}/submissions.csv.zip'
        result = self.session.get(url, auth=self.auth)
        return result

    def listAppUsers(self, projectId=None):
        """Fetch a list of app users for a project on an ODK Central server."""
        url = f'{self.base}projects/{projectId}/app-users'
        result = self.session.get(url, auth=self.auth)
        self.appusers = result.json()
        return result

    def dump(self):
        """Dump internal data structures, for debugging purposes only"""
        super().dump()
        print("There are %d forms in this project" % len(self.forms))
        if self.data:
            print("Project ID: %s" % self.data['id'])
        for data in self.forms:
            print("\t %s(%s): %s" % (data['xmlFormId'], data['version'], data['name']))
        print("There are %d submissions in this project" % len(self.submissions))
        for data in self.submissions:
            print("\t%s: %s" % (data['instanceId'], data['createdAt']))
        print("There are %d app users in this project" % len(self.appusers))
        for data in self.appusers:
            print("\t%s: %s" % (data['id'], data['displayName']))

class OdkForm(OdkCentral):
    """Class to manipulate a from on an ODK Central server"""
    def __init__(self, data=None):
        super().__init__()
        self.name = None
        self.attach = list()
        self.publish = True
        self.media = dict()
        self.xml = None

    def getDetails(self, projectId=None, xmlFormID=None):
        # GET
        # https://mock.com/v1/projects/projectId/forms/xmlFormId
        url = f'{self.base}/v1/projects/{projectId}/forms/{formId}'
        result = self.session.get(url, auth=self.auth)
        self.media = result.json()
        return result
        
    def addMedia(self, media=None, filespec=None):
        """Add a data file to this form"""
        # FIXME: this also needs the data
        self.media[filespec] = media

    def addXMLForm(self, projectId=None, formId=None, xform=None):
        """Add an XML file to this form"""
        self.xml = xform

    def listMedia(self, projectId=None, formId=None, instanceId=None):
        """List all the attchements for this form"""
        # GET
        # https://mock.com/v1/projects/projectId/forms/xmlFormId/attachments
        url = f'{self.base}/v1/projects/{projectId}/forms/{formId}/submissions/{instanceId}/attachments'
        result = self.session.get(url, auth=self.auth)
        self.media = result.json()
        return result
        
    def getMedia(self, projectId=None, formId=None, instanceId=None, filename=None):
        """Fetch a specific attachment by filename from a submission to a form."""
        # GET
        # https://mock.com/v1/projects/projectId/forms/xmlFormId/attachments/filename
        url = f'{self.base}/v1/projects/{projectId}/forms/{formId}/submissions/{instanceId}/attachments/{filename}'
        result = self.session.get(url, auth=self.auth)
        self.media = result.content()
        return result

    def createForm(self, projectId=None, xform=None):
        """Create a new form on an ODK Central server"""
        # base_name = os.path.basename(path2Form)
        # file_name = os.path.splitext(base_name)[0]
        # form_file = open(path2Form, 'rb')
        #sheet = form_file.active
        # POST
        # headers = {
        #     'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        #     f'X-XlsForm-FormId-Fallback': name
        # }
        url = f'{self.base}/v1/projects/{projectId}/forms?ignoreWarnings=true&publish=true'
        # From the requests, gives the same error
        result = self.session.post(url, auth=self.auth,  data=xform, headers=headers)
        # FIXME: should update self.forms with the new form
        return result

    def deleteForm(self, projectId=None, formId=None):
        # If your goal is to prevent it from showing up on survey clients like ODK Collect, consider
        # setting its state to closing or closed
        # DELETE
        url = f'{self.base}/v1/projects/{projectId}/forms/{xmlFormId}'
        result = self.session.delete(url, auth=self.auth)
        return result

    def createDraft(self, projectId=None, xmlFormId=None):
        url = f'{self.base}projects/{projectId}/forms/{xmlFormId}/draft?ignoreWarnings='
        result = self.session.get(url, auth=self.auth, data=values, headers=headers)
        return result        

    def listDraftMedia(self, projectId=None, xmlFormId=None):
        url = f'{self.base}projects/{projectId}/forms/{xmlFormId}/draft/attachments'
        result = self.session.get(url, auth=self.auth, data=values, headers=headers)
        return result        

    def uploadMedia(self, projectId=None, xmlFormId=None):
        url = f'{self.base}projects/{projectId}/forms/{xmlFormId}/draft/attachments/filename'
        result = self.session.get(url, auth=self.auth, data=values, headers=headers)
        return result        

    def publishDraft(self):
        url = f'{self.base}projects/{projectId}/forms/{xmlFormId}/draft/publish?version='
        result = self.session.get(url, auth=self.auth, data=values, headers=headers)
        return result

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

    # Gotta start somewhere...
    project = OdkProject()
    # Start the persistent HTTPS connection to the ODK Central server
    project.authenticate()
    # Get a list of all the projects on this ODK Central server
    project.listProjects()
    # List all the users on this ODK Central server
    project.listUsers()
    # List all the forms for this project. FIXME: don't hardcode the project ID
    project.listForms(4)
    # List all the app users for this project. FIXME: don't hardcode the project ID
    project.listAppUsers(4)
    # List all the submissions for this project. FIXME: don't hardcode the project ID ad form name
    project.listSubmissions(4, "cemeteries")
    project.getSubmission(4, "cemeteries", True)
    # Dump all the internal data
    project.dump()

    # Form management
    form = OdkForm()
    form.authenticate()
    form.listMedia(4, "waterpoints")
    # Make a new form
    # xml = "/home/rob/projects/HOT/odkconvert.git/XForms/cemeteries.xml"
    # form.addXMLForm(xml)
    # csv1 = "/home/rob/projects/HOT/odkconvert.git/XForms/municipality.csv"
    # csv2 = "/home/rob/projects/HOT/odkconvert.git/XForms/towns.csv"
    # form.addMedia(csv1)
    # form.addMedia(csv2)
    form.dump()
              

