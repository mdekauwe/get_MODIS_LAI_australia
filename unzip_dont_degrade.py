#!/usr/bin/env python2.7
"""
Unzip all the .gz modis files, add the missing header file
"""

import gzip
import glob
import os
import sys
import shutil
from osgeo import gdal, gdalconst

__author__  = "Martin De Kauwe"
__version__ = "1.0 (05.12.2016)"
__email__   = "mdekauwe@gmail.com"


def main():

    out_fdir = "hdfs"
    for yr in range(2001, 2016):
        print( yr )
        fdir = "hdf_zipped/%s" % (str(yr))

        out_yr_dir = os.path.join(out_fdir, "%s" % (str(yr)))
        if not os.path.exists(out_yr_dir):
            os.makedirs(out_yr_dir)

        for fname in glob.glob(os.path.join(fdir, '*.gz')):
            in_file = gzip.open(fname, 'rb')

            try:
                s = in_file.read()
                in_file.close()

                # get the filename without gz.
                out_fname = os.path.basename(fname)[:-3]

                if not os.path.exists(out_fdir):
                    os.makedirs(out_fdir)

                open(os.path.join(out_yr_dir, out_fname), 'w').write(s)
            except IOError:
                # there are few bad files which we will need to skip later
                continue

            # Add the missing header information
            hdr_fn = "%s.hdr" % \
                     (os.path.splitext(os.path.basename(out_fname))[0])
            hdr_fn = os.path.join(out_yr_dir, hdr_fn)
            shutil.copy("ancillary_info/MODIS_ENVI.hdr", hdr_fn)


if __name__ == "__main__":

    main()
