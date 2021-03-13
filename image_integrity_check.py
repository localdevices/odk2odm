#!/usr/bin/python3

import sys, os
from pathlib import Path
from PIL import Image

def checkimages(indir):
    """returns a list of image files that can be successfully opened by PIL"""
    filelist = []
    for path, dirs, files in os.walk(indir):
        for f in files:
            filelist.append(os.path.join(path, f))

    goodfiles = []
    badfiles = []
    for f in filelist:
        try:
            image = Image.open(f)
            goodfiles.append(f)
        except Exception as e:
            print(e)
            badfiles.append(f)

    return(goodfiles, badfiles)

def write_file_lists(indir):
    """Write two text files with the good and bad image files in the parent
    directory of the input directory"""
    path = Path(indir)
    parent = path.parent
    goodfilepath = Path.joinpath(parent, 'goodfiles.txt')
    badfilepath = Path.joinpath(parent, 'badfiles.txt')
    (goodfiles, badfiles) = checkimages(indir)
    with open(goodfilepath, 'w') as gf:
        for f in goodfiles:
            gf.write(f'{f}\n')
    with open(badfilepath, 'w') as bf:
        for f in badfiles:
            bf.write(f'{f}\n')
    

if __name__ == "__main__":
    """Checks a directory full of images. 1 argument, a directory. 
    Outputs two text files in the parent directory of the input directory."""
    
    write_file_lists(sys.argv[1])
