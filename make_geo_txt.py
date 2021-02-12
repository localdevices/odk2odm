#! /usr/bin/python3
"""
Produces a geo.txt file for use by OpenDroneMap from a table of ODK 
form submissions.

Takes an input CSV file of submissions with multiple photos per survey 
point as a positional argument. 

Takes four flag arguments specifying the columns in the input file for lat, 
lon, elevation, and accuracy: -lat, -lon, -ele, and -acc.

Takes a flag argument, -r or --range, which specifies all of the columns where 
photos are found. For example, "15-26,28-39,41-52" will capture three sets of
12 consecutive columns. One-based column numbering to be consistent with a 
spreadsheet, which is the most likely place users will be counting columns.  

Takes and optional flag argument, -proj, with a Coordinate Reference System
string (which can be in whatever format ODM will accept; this script doesn't 
care).

"""
################################################################################
import sys, os
import csv
import re
import argparse
import string
    
def make_geo_txt(infile, colrange, lonc,
                 latc, elec, accc, proj):
    """
    make a list of photo locations so that ODM
    can process them efficiently.
    """
    latcol = col2num(latc)
    loncol = col2num(lonc)
    elecol = col2num(elec)
    acccol = col2num(accc)
    sites = list(csv.reader(open(infile)))[1:]
    cols = parse_range(colrange)
    outfile = os.path.join(os.path.dirname(infile), 'geo.txt')
    with (open(outfile, 'w')) as csvfile:
        w = csv.writer(csvfile, delimiter = ' ')
        w.writerow([proj])
        for site in sites:
            for col in cols:
                w.writerow([site[col-1],
                            site[int(loncol) - 1],
                            site[int(latcol) - 1],
                            site[int(elecol) - 1],
                            '0','0','0',
                            site[int(acccol) - 1],
                            site[int(acccol) - 1],
                            ])
                            

def col2num(col):
    """Excel column letters to 1-based column number"""
    if col.isdigit():
        return col
    else:
        colnum = 0
        for c in col:
            if c in string.ascii_letters:
                colnum = colnum * 26 + (ord(c.upper()) -
                                        ord('A')) + 1
        return colnum

def parse_range(instring):
    """
    Takes a string like '3-5, 13, 36-38'
    or 'c-e, m, aj-al' (spreadsheet column names)
    and returns a list of index integers like 
    [3,4,5,13,36,37,38]
    """
    rng = re.sub(r'\s+', '', instring.strip())
    parts = [s.split('-') for s in rng.split(',')]
    numparts = [[col2num(x) for x in i] for i in parts]
    l = ([range(int(i[0]), int(i[1]) + 1)
         if len(i) == 2
         else i[0] for i in numparts])
    
    return [int(item) for sublist in l for item in sublist]


if __name__ == "__main__":
    """

    """
    p = argparse.ArgumentParser(description =
                                ('Georeference attachments '
                                 'from ODK submissions using '
                                 'lat and lon columns.'))
    p.add_argument('inputfile', help = 'Input CSV file')
    p.add_argument('-r', '--range', required=True,
                   help = ('columns with attachments to be '
                           'georeferenced. Use format '
                           '"3-5,7,9-11" or "c-e,g,i-k" '
                           '(spreadsheet format). Use 1-based '
                           'column numbers'))
    p.add_argument('-lat', '--latitude',
                   help = ('Latitude column. Can be 1-based '
                           'column number or spreadsheet '
                           'column letters'))
    p.add_argument('-lon', '--longitude',
                   help = ('longitude column '
                           'can be 1-based column number or '
                           'spreadsheet column letters'))
    p.add_argument('-ele', '--elevation',
                   help = 'GPS elevation column')
    p.add_argument('-acc', '--accuracy',
                   help = 'Estimated GPS accuracy column')
    p.add_argument('-proj', '--projection',
                   help = 'Coordinate Reference System',
                   default = 'EPSG:4326')
    args = p.parse_args()

    make_geo_txt(args.inputfile, args.range,
                 args.longitude, args.latitude,
                 args.elevation, args.accuracy,
                 args.projection)
