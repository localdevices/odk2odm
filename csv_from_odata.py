#!/usr/bin/python3

import sys, os
import fetch
import argparse
import csv

def csv_from_odata(url, aut, project, form, outdir):
    """Write a CSV to a specified directory using odata for a specified form"""
    response = fetch.odata_submissions(url, aut, project, form)
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
    p.add_argument('-od', '--output_directory',
                   help = 'Directory to write output files')

    args = p.parse_args()

    csv_from_odata(args.base_url, (args.user, args.password), args.project,
           args.form, args.output_directory)
