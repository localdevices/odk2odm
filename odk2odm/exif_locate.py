#! /usr/bin/python3
"""
yah
"""

import sys, os
import csv
from PIL import ExifTags
    
def overwrite_location(infile, lat, lon, **kwargs):
    """Replace GPS info in EXIF of image"""
    pass
    
if __name__ == "__main__":
    """Expects a csv and a directory"""
    create_geotag_list(sys.argv[1])
