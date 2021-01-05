#! /usr/bin/python3
"""
yah
"""

import sys, os
import csv
import re
import argparse
    
def make_geo_txt(infile, imagecolrange, **kwargs):
    """
    make a list of photo locations so that ODM
    can process them efficiently.

    Expects a csv and a directory
    and column indices for 
    image_name geo_x geo_y [geo_z] 
    [omega (degrees)] 
    [phi (degrees)] [kappa (degrees)] 
    [horz accuracy (meters)] 
    [vert accuracy (meters)] 
    [extras...]
    """
    sites = list(csv.reader(open(infile)))
    #for i, site in enumerate(sites[0]):
    #    print(i, site)
    with (open('out.csv', 'w')) as csvfile:
        w = csv.writer(csvfile)
        
        for site in sites:
            for col in imagecolrange:
                w.writerow([site[col-1], site[8], site[9]])


def parse_range(instring):
    """
    Takes a string like '3-5, 13, 36-38' and returns a list
    like [3,4,5,13,36,37,38]
    """
    rng = re.sub(r'\s+', '', instring.strip())
    parts = [s.split('-') for s in rng.split(',')]
    l = ([range(int(i[0]), int(i[1]) + 1)
         if len(i) == 2
         else i[0] for i in parts])
    
    return [int(item) for sublist in l for item in sublist]
        

if __name__ == "__main__":
    """

    """
#    p = argparse.ArgumentParser()
#    p.add_argument('-r', '--range', 
    make_geo_txt(sys.argv[1], parse_range(sys.argv[2]))
