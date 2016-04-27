#!/usr/bin/env python
"""
Check our output
"""

__author__  = "Martin De Kauwe"
__version__ = "1.0 (10.03.2016)"
__email__   = "mdekauwe@gmail.com"


import matplotlib.colors as colors
import matplotlib
from matplotlib import ticker
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import re
import tarfile
import glob
import shutil
import gdal
import string

def main():

    # gdalinfo to get this info
    scale_factor = 0.1
    lai_valid_max = 100
    qa_valid_max = 254
    ncols = 841
    nrows = 681
    ndays = 46
    nyears = 1


    latitude = -35.65572222
    longitude = 148.1520833

    cellsize = 0.05
    yurcorner = -9.975
    xllcorner = 111.975
    #latitude = yurcorner - (float(row - 1) * cellsize);
    #longitude = xllcorner + (float(col - 1) * cellsize);


    row = int( (yurcorner - latitude) / cellsize )
    col = int( (longitude - xllcorner) / cellsize )

    yr = 2001
    lai_store = []
    for i, doy in enumerate(xrange(1, 361+8, 8)):

        if doy < 10:
            doy_st = "00%s" % (str(doy))
        elif doy < 100:
            doy_st = "0%s" % (str(doy))
        else:
            doy_st = "%s" % (str(doy))


        fdir = "hdfs/%s" % (str(yr))

        fname = "MOD15A2.%s.%s.aust.005.b02.1000m_lai.hdf" % \
                (str(yr), doy_st)


        fname = os.path.join(fdir, fname)
        if os.path.exists(fname):

            lai = gdal.Open(fname)
            lai = lai.ReadAsArray()
            lai = np.where(lai > lai_valid_max, np.nan, lai)
            lai = np.where(lai == 0, np.nan, lai) # fill values top of image
            lai *= scale_factor


            qa_fname = string.replace(fname, "b02", "b03")
            qa_fname = string.replace(qa_fname, "1000m_lai","1000m_quality")
            qa = gdal.Open(qa_fname)
            qa = qa.ReadAsArray()
            qa = np.where(qa > qa_valid_max, np.nan, qa)
            qa = np.where(np.isnan(lai), np.nan, qa)

            std_fn = string.replace(fname, "b02", "b06")
            std_fn = string.replace(std_fn, "1000m_lai","1000m_lai_stdev")
            lai_std = gdal.Open(std_fn)
            lai_std = lai_std.ReadAsArray()
            lai_std = np.where(lai_std > lai_valid_max, np.nan, lai_std)
            lai_std = np.where(lai_std == 0, np.nan, lai_std)
            lai_std *= scale_factor

            # Just take best QA = 0
            #lai = np.where(qa != 0, np.nan, lai)
            #lai_std = np.where(qa != 0, np.nan, lai_std)

            # Relax QA, take saturation data too.
            # echo "00000000" | gawk -f ~/bin/awk/bit2d.awk
            # echo "00100000" | gawk -f ~/bin/awk/bit2d.awk
            good_QA = np.array([0,32])
            lai[qa != good_QA] = np.nan
            lai_std[qa != good_QA] = np.nan



            lai_store.append(lai[row,col])

    plt.plot(np.arange(1, 361, 8), lai_store, "ro-")
    plt.show()

    experiment_id = "Tumbarumba"

    ncols = 841
    nrows = 681
    ndays = 366
    nvars = 2

    latitude = -35.6566
    longitude = 148.152

    cellsize = 0.05
    yurcorner = -9.975
    xllcorner = 111.975
    #latitude = yurcorner - (float(row - 1) * cellsize);
    #longitude = xllcorner + (float(col - 1) * cellsize);
    row = int( (yurcorner - latitude) / cellsize )
    col = int( (longitude - xllcorner) / cellsize )

    lai_fname = "%s_LAI.bin" % (experiment_id)
    if not os.path.exists(lai_fname):


        fdir = "/Users/%s/research/get_MODIS_LAI_australia" % (os.getlogin())
        f = open(os.path.join(fdir, "modis_climatology_splined.bin"), "r")
        data = np.fromfile(f).reshape((nvars,ndays,nrows,ncols))
        f.close()

        pixel = data[:,:,row-1,col-1]
        # i.e. don't write the bad pixels out
        if np.all(pixel[0,:] > -500.0):
            pixel.tofile(lai_fname)
        else:
            print "PROBLEM!"

    data = np.fromfile("Tumbarumba_LAI.bin")

    data1 = data.reshape(nvars, ndays)[0,:]
    data2 = data.reshape(nvars, ndays)[1,:]

    x1 = np.arange(1.,367)
    x2 = np.arange(1, 361+8, 8)
    plt.plot(x1, data1, "r-")
    plt.plot(x2, data2[data2>-500.0], "ko")
    plt.plot(np.arange(1, 361, 8), lai_store, "ro")

    plt.show()


if __name__ == "__main__":

    main()
