#!/usr/bin/env python
"""
Extract MODIS data...not sure what we are going to do with it yet.

HDF4 data are stored as tables rather than gridded (raster) data
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
    col = 4321
    row = 2478
    pixel = []
    dates = []

    fdir = "hdfs"
    for fname in glob.glob(os.path.join(fdir, '*.b02.*.hdf')):

        doy = os.path.basename(fname).split(".")[2]
        dates.append(doy)

        # Read LAI data
        lai = gdal.Open(fname)
        lai = lai.ReadAsArray()
        lai = np.where(lai > lai_valid_max, np.nan, lai)
        lai *= scale_factor

        # Read QA data
        qa_fname = string.replace(fname, "b02", "b03")
        qa_fname = string.replace(qa_fname, "1000m_lai", "1000m_quality")
        qa = gdal.Open(qa_fname)
        qa = qa.ReadAsArray()

        # Just take best QA = 0
        lai = np.where(qa != 0, np.nan, lai)
        pixel.append(lai[row,col])


        # plot all of Aus
        #plt.imshow(lai, interpolation='nearest')
        #plt.colorbar()
        #plt.show()
        #sys.exit()

    plt.plot(dates, pixel)
    plt.show()

if __name__ == "__main__":

    main()
