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

    xnew = np.arange(1.,367)
    xdays = np.arange(1, 361+8, 8)

    outdays = 366
    ovars = 2
    out = np.zeros((ovars,outdays,nrows,ncols))

    for i in xrange(nrows):
        for j in xrange(ncols):

            #i = 400
            #j = 800
            # Interpolation does not allow for extrapolation, so we won't be
            # able to get LAI estimates beyond doy 361. To get around this
            # we are going to repeat the time series and spline that.

            # Save the raw data, incase we every which to check interpolated
            # climatologies in the future
            raw = np.zeros(outdays)
            for ii, doy in enumerate(xnew):
                if doy not in xdays:
                    raw[ii] = -999.9
                else:
                    idx = np.argwhere(xdays==doy)[0][0]
                    raw[ii] = data[idx,i,j]

            # repeat LAI x 3
            y_extend = np.tile(data[:,i,j], 3)
            x_extend = np.hstack((xdays-46*8, xdays, xdays+46*8))

            # interpolate the data
            tck = interpolate.splrep(x_extend, y_extend, s=0.7)
            ynew = interpolate.splev(xnew, tck, der=0)

            #tck = interpolate.splrep(xdays, data[:,i,j], s=0.2)
            #ynew = interpolate.splev(xnew, tck, der=0)

            #plt.plot(xnew, ynew, "r-")
            #plt.plot(xdays, data[:,400,800], "ko")
            #plt.show()
            #sys.exit()

            # replace nans with -999.9 for consistency
            idx = np.where(np.isnan(ynew))
            ynew[idx] = -999.9

            out[0,:,i,j] = ynew
            out[1,:,i,j] = raw


    of = open("modis_climatology_splined.bin", "wb")
    out.tofile(of)
    of.close()


if __name__ == "__main__":

    main()
