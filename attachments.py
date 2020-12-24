#! /usr/bin/python3

import sys, os
import fetch
import argparse

def grab_media(url, project, formID):
    at = fetch.attachment(base_url, projectId, formId, instanceId, filename, authtuple):
    return at
    
if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('-url', '--base_url' help='Server URL')
    p.add_argument('-p', '--project', help = 'the project in question')
    p.add_arbument('f', '--formID', help = 'Unique name of the relevant form')
    args = p.parse_args()
    grab_media(args['url'], args['project'], arggis['formID'])
    
