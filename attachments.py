#!/usr/bin/python3

import sys, os
import fetch
import argparse
import threading
import csv

def csv_from_odata(url, aut, project, form, outdir):
    response = fetch.odata_submissions(url, aut, project, formID)
    submissions = response.json()['value']
    # Making the unsafe assumption that all rows have the same headers
    # and simply grabbing the headers from the first row
    headers = [x for x in submissions[0]]
    outfilename = os.path.join(outdir, f'{form}.csv')
    with open(outfilename, 'w') as outfile:
        w = csv.writer(outfile, delimiter = ';')
        w.writerow(headers)
        for submission in submissions:
            row = []
            for header in headers:
                # TODO: expand geo column to lat, lon, elevation, accuracy
                row.append(submission[header])
            w.writerow(row)

def all_attachments_from_form(url, aut, project, formID):
     submissions = fetch.submissions(args.base_url,
                                     (args.user, args.password),
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

    
    threads = []

    for chunk in chunks:
        thread = threading.Thread(target=managechunk,
                                  args=(chunk, outdirpath, timeout))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
