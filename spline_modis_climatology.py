#!/usr/bin/env python
"""
Fit spline to MODIS LAI to get 365 days from 8-day product
"""

import glob
import os
import sys
import numpy as np
import string
import matplotlib.pyplot as plt
from scipy import interpolate

__author__  = "Martin De Kauwe"
__version__ = "1.0 (10.03.2016)"
__email__   = "mdekauwe@gmail.com"


def main():

    ncols = 841
    nrows = 681
    ndays = 46

    f = open("modis_climatology.bin", "r")
    data = np.fromfile(f).reshape((ndays,nrows,ncols))
    f.close()

    xnew = np.arange(1.,361)
    xdays = np.arange(1, 361+8, 8)

    outdays = 360
    out = np.zeros((outdays,nrows,ncols))
    
    for i in xrange(nrows):
        for j in xrange(ncols):
            print "%d/%d : %d/%d" % (i, nrows, j, ncols)
            #f = interpolate.interp1d(xdays, data[:,i,j], kind='linear')
            #ynew = f(xnew)

            tck = interpolate.splrep(xdays, data[:,i,j],s=0.2)
            ynew = interpolate.splev(xnew, tck, der=0)

            out[:,i,j] = ynew


    of = open("modis_climatology_splined.bin", "wb")
    out.tofile(of)
    of.close()


if __name__ == "__main__":

    main()
