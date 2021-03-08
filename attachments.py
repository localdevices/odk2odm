#!/usr/bin/python3

import sys, os
import fetch
import argparse
import threading
import csv

def threaded_download():
    """Grab lots of photos using threaded concurrent download"""
    # NOT DONE
    
    threads = []

    for chunk in chunks:
        thread = threading.Thread(target=managechunk,
                                  args=(chunk, outdirpath, timeout))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def all_attachments_from_form(url, aut, project, form, outdir):
     submissions = fetch.submissions(url, aut, project, form)

     for submission in submissions.json():
         print(submission['instanceId'])
         atts = fetch.attachment_list(url, aut, project, form,
                                      submission['instanceId'])
         for attachment in atts.json():
             print(attachment['name'])
            
if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('-url', '--base_url',
                   help = 'Server URL')
    p.add_argument('-u', '--user',
                   help = 'ODK Central username (usually email)')
    p.add_argument('-pw', '--password',
                   help = 'ODK Central password')
    p.add_argument('-p', '--project',
                   help = 'the project in question')
    p.add_argument('-f', '--form',
                   help = 'Unique name of the relevant form')
    p.add_argument('-i', '--instance',
                   help = 'Submission instance ID')
    p.add_argument('-od', '--output_directory',
                   help = 'Directory to write output files')
    p.add_argument('-t', '--threads',
                   help = 'Maximum number of download threads', default = 10)

    args = p.parse_args()

    all_attachments_from_form(args.bas_url, (args.user, args.password),
                              args.project, args.form, args.output_directory)
                              
