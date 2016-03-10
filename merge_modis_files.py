#!/usr/bin/env python
"""
Average over all DOYs across years and make a large MODIS binary file
"""

import glob
import os
import gdal
import sys
import numpy as np
import string
import matplotlib.pyplot as plt

__author__  = "Martin De Kauwe"
__version__ = "1.0 (07.03.2016)"
__email__   = "mdekauwe@gmail.com"


def main():

    # gdalinfo to get this info
    scale_factor = 0.1
    lai_valid_max = 100
    qa_valid_max = 254
    ncols = 4790
    nrows = 3726
    ndays = 46
    nyears = 15

    big_data = np.zeros((ndays,nrows,ncols))
    ata = np.zeros((nyears,nrows,ncols))

    f = open("all_modis_data.bin", "wb")

    for i, doy in enumerate(xrange(1, 336, 8)):
        print doy
        if doy < 10:
            doy_st = "00%s" % (str(doy))
        elif doy < 100:
            doy_st = "0%s" % (str(doy))
        else:
            doy_st = "%s" % (str(doy))

        for j,yr in enumerate(xrange(2001, 2016)):
            fdir = "hdfs/%s" % (str(yr))

            fname = "MOD15A2.%s.%s.aust.005.b02.1000m_lai.hdf" % \
                    (str(yr), doy_st)

            fname = os.path.join(fdir, fname)
            if os.path.exists(fname):

                lai = gdal.Open(fname)

                lai = lai.ReadAsArray()
                lai = np.where(lai > lai_valid_max, -999.9, lai)
                lai *= scale_factor

                qa_fname = string.replace(fname, "b02", "b03")
                qa_fname = string.replace(qa_fname, "1000m_lai", "1000m_quality")
                qa = gdal.Open(qa_fname)
                qa = qa.ReadAsArray()

                # Just take best QA = 0
                lai = np.where(qa != 0, -999.9, lai)

            else:
                lai = np.ones((nrows,ncols)) * -999.9

            yrs_data[j,:,:] = lai

        # average across years
        data = np.where(yrs_data < 0.0, np.nan, yrs_data)
        big_data[:,:,:] = data.nanmean(axis=0)
        big_data.tofile(f)


if __name__ == "__main__":

    main()
