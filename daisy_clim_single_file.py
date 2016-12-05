#!/usr/bin/env python
"""
Open Daisy's file and show her how to plot it
"""

import glob
import os
import gdal
import sys
import numpy as np
import string
import matplotlib.pyplot as plt

__author__  = "Martin De Kauwe"
__version__ = "1.0 (05.12.2016)"
__email__   = "mdekauwe@gmail.com"


def main():

    ncols = 4790
    nrows = 3726
    ndays = 46

    out = np.zeros((nrows,ncols))

    fname = "modis_climatology.bin"
    data = np.fromfile(fname).reshape((ndays,nrows,ncols))
    data = np.where(data < -500, np.nan, data)

    data = np.ma.MaskedArray(data, mask=np.isnan(data))
    data = np.ma.average(data, axis=0)

    data = np.where(data <= 0.0, np.nan, data) # sea
    data = np.ma.fix_invalid(data, fill_value=-999.9) #remove masked array

    out[:,:] = data

    f = open("modis_climatology_avg_over_yr.bin", "wb")
    out.tofile(f)
    f.close()


if __name__ == "__main__":

    main()
