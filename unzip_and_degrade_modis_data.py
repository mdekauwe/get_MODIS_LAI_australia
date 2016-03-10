#!/usr/bin/env python
"""
Unzip all the .gz modis files, add the missing header file and degrade the
resolution to 10 km to match the AWAP data.
"""

import gzip
import glob
import os
import sys
import shutil
from osgeo import gdal, gdalconst

__author__  = "Martin De Kauwe"
__version__ = "1.0 (10.03.2016)"
__email__   = "mdekauwe@gmail.com"


def main():

    out_fdir = "hdfs"
    for yr in xrange(2001, 2016):
        print yr
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

            # degrade from 1km to 10km and match grid of AWAP data
            src_fn = os.path.join(out_yr_dir, out_fname)
            match_fn = "ancillary_info/19500101_tmax.flt"
            degraded_fn = os.path.join(out_yr_dir, "tmp.hdf")
            degrade_to_10km(src_fn, match_fn, degraded_fn)

            # overwrite the 1km file with the degraded file.
            dst_fn = os.path.join(out_yr_dir, out_fname)
            shutil.move(degraded_fn, dst_fn)

            degraded_fn_hdr = os.path.join(out_yr_dir, "tmp.hdr")
            shutil.move(degraded_fn_hdr, hdr_fn)


def degrade_to_10km(src_filename, match_filename, dst_filename):

    # Source
    src = gdal.Open(src_filename, gdalconst.GA_ReadOnly)
    src_proj = src.GetProjection()
    src_geotrans = src.GetGeoTransform()

    # We want a section of source that matches this:
    match_ds = gdal.Open(match_filename, gdalconst.GA_ReadOnly)
    match_proj = match_ds.GetProjection()
    match_geotrans = match_ds.GetGeoTransform()
    wide = match_ds.RasterXSize
    high = match_ds.RasterYSize

    # Output / destination
    dst = gdal.GetDriverByName('ENVI').Create(dst_filename, wide, high, 1,
                                              gdalconst.GDT_Float32)
    dst.SetGeoTransform(match_geotrans)
    dst.SetProjection(match_proj)

    # Do the work
    gdal.ReprojectImage(src, dst, src_proj, match_proj,
                        gdalconst.GRA_NearestNeighbour)
    #gdal.ReprojectImage(src, dst, src_proj, match_proj, gdalconst.GRA_Bilinear)

    del dst # Flush

if __name__ == "__main__":

    main()
