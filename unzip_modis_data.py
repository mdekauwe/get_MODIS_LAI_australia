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
    out_fdir = "hdf"
    for fname in glob.glob(os.path.join(fdir, '*.gz')):

        in_file = gzip.open(fname, 'rb')
        s = in_file.read()
        in_file.close()

        # get the filename without gz.
        gzip_fname = os.path.basename(gzip_path)
        out_fname = gzip_fname[:-3]

        if not os.path.exists(out_fdir):
            os.makedirs(out_fdir)

        open(out_fdir, 'w').write(s)

if __name__ == "__main__":

    unzip_data()
