#!/usr/bin/python3

import sys, os
import fetch
import argparse
import threading

# TODO see if this can be empty without breaking shit
# import credentials

def grab_media(url, project, formID):
    att = fetch.attachment(base_url, projectId, formId, instanceId, filename, authtuple)
    return att

def grab_forms(url, aut, project):
    forms = fetch.forms(url, aut, project)
    return forms

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('-url', '--base_url', help = 'Server URL')
    p.add_argument('-u', '--user', help = 'ODK Central username (usually email)')
    p.add_argument('-pw', '--password', help = 'ODK Central password')
    p.add_argument('-p', '--project', help = 'the project in question')
    p.add_argument('-f', '--form', help = 'Unique name of the relevant form')
    #p.add_argument('-i', '--instance', help = 'Submission instance ID')

    args = p.parse_args()

    submissions = fetch.submissions(args.base_url,
                                    (args.user,
                                     args.password),
                                    args.project,
                                    args.form,
                                    )
                                    
    for submission in submissions.json():
        print(submission['instanceId'])
        atts = fetch.attachment_list(args.base_url,
                                     (args.user,
                                      args.password),
                                     args.project,
                                     args.form,
                                     submission['instanceId']
                                     )
        for attachment in atts.json():
            print(attachment['name'])

    
    threads = []

    for chunk in chunks:
        thread = threading.Thread(target=managechunk,
                                  args=(chunk, outdirpath, timeout))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
