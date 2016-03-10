#!/usr/bin/env python
"""
Average over all DOYs across years and make a large MODIS climatology
"""

import glob
import os
import gdal
import sys
import numpy as np
import string
import matplotlib.pyplot as plt

__author__  = "Martin De Kauwe"
__version__ = "1.0 (10.03.2016)"
__email__   = "mdekauwe@gmail.com"


def main():

    # gdalinfo to get this info
    scale_factor = 0.1
    lai_valid_max = 100
    qa_valid_max = 254
    ncols = 841
    nrows = 681
    ndays = 46
    nyears = 15

    big_data = np.zeros((ndays,nrows,ncols))
    data = np.zeros((nyears,nrows,ncols))

    f = open("modis_climatology.bin", "wb")

    for i, doy in enumerate(xrange(1, 361+8, 8)):
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
                lai = np.where(lai > lai_valid_max, np.nan, lai)
                lai *= scale_factor

                qa_fname = string.replace(fname, "b02", "b03")
                qa_fname = string.replace(qa_fname, "1000m_lai","1000m_quality")
                qa = gdal.Open(qa_fname)
                qa = qa.ReadAsArray()
                qa = np.where(qa > qa_valid_max, np.nan, qa)

                std_fn = string.replace(fname, "b02", "b06")
                std_fn = string.replace(std_fn, "1000m_lai","1000m_lai_stdev")
                lai_std = gdal.Open(unc_fn)
                lai_std = qa.ReadAsArray()
                lai_std = np.where(lai_std > lai_valid_max, np.nan, lai_std)

                # Just take best QA = 0
                lai = np.where(qa != 0, np.nan, lai)
                lai_std = np.where(qa != 0, np.nan, lai_std)
            else:
                lai = np.ones((nrows,ncols)) * np.nan

            data[j,:,:] = lai

            # close dataset
            lai = None

        # average across years
        #data = np.where(data < 0.0, np.nan, data)
        # big_data[i,:,:] = np.ma.average(data, weights=1.0 / lai_std**2, axis=0)
        big_data[i,:,:] = np.nanmean(data, axis=0)
    big_data.tofile(f)


if __name__ == "__main__":

    main()
