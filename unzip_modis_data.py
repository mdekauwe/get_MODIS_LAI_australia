#!/usr/bin/env python
"""
Unzip all the .gz modis files
"""

import gzip
import glob
import os

__author__  = "Martin De Kauwe"
__version__ = "1.0 (07.03.2016)"
__email__   = "mdekauwe@gmail.com"


def unzip_data():
    fdir = "hdf_zipped"
    out_fdir = "hdfs"
    for fname in glob.glob(os.path.join(fdir, '*.gz')):
        print fname
        
        in_file = gzip.open(fname, 'rb')
        s = in_file.read()
        in_file.close()

        # get the filename without gz.
        out_fname = os.path.basename(fname)[:-3]

        if not os.path.exists(out_fdir):
            os.makedirs(out_fdir)

        open(os.path.join(out_fdir, out_fname), 'w').write(s)

if __name__ == "__main__":

    unzip_data()
