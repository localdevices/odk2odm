#!/usr/bin/python3

import os
from odk2odm import odk_api
import argparse
import csv
import json


def csv_from_odata(url, aut, project, form, outdir, gc):
    """Write a CSV to a specified directory using odata for a specified form"""
    response = odk_api.odata_submissions(url, aut, project, form)
    submissions = response.json()['value']
    # Making the unsafe assumption that all rows have the same headers
    # and simply grabbing the headers from the first row
    geocol = int(gc)
    headers = [x for x in submissions[0]]
    newheaders = (headers[: geocol] +
                  ['lat', 'lon', 'elevation', 'accuracy'] +
                  headers[geocol :])
    outfilename = os.path.join(outdir, f'{form}.csv')
    with open(outfilename, 'w') as outfile:
        w = csv.writer(outfile, delimiter = ';')
        w.writerow(newheaders)
        for submission in submissions:
            row = []
            for header in headers:
                row.append(submission[header])
            gc_contents = row[geocol - 1]
            geolist = jsonpoint_to_list(gc_contents)
            w.writerow(row[: geocol] + geolist + row[geocol :])


def jsonpoint_to_list(po):
    """ODK Central returnt point in what is almost a JSON string, 
    except that it is single-quoted instead of double-quoted, 
    so Python's JSON module freaks out. This ingests that string and
    returns a tuple of (lat, lon, elevation, accuracy)"""
    try:
        doublequotedpointstring = po.replace("'", '"')
        jsonpoint = json.loads(doublequotedpointstring)
        lat = jsonpoint['coordinates'][1]
        lon = jsonpoint['coordinates'][0]
        ele = jsonpoint['coordinates'][2]
        acc = jsonpoint['properties']['accuracy']
        return [lat, lon, ele, acc]
    except Exception as e:
        #print(e)
        #print(po)
        try:
            lat = po['coordinates'][1]
            lon = po['coordinates'][0]
            ele = po['coordinates'][2]
            acc = po['properties']['accuracy']
            return [lat, lon, ele, acc]
            return ['', '', '', '']
        except Exception as f:
            #print(f)
            return ['', '', '', '']


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
    p.add_argument('-gc', '--geopoint_column',
                   help = 'Column containing the geopoint, 1-based')

    args = p.parse_args()

    csv_from_odata(args.base_url, (args.user, args.password), args.project,
                   args.form, args.output_directory, args.geopoint_column)

