#!/usr/bin/env python2.7
"""
Average over all DOYs across years and make a large MODIS climatology.
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

    # gdalinfo to get this info
    scale_factor = 0.1
    lai_valid_max = 100
    qa_valid_max = 254
    ncols = 4790
    nrows = 3726
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
                lai = np.where(lai == 0, np.nan, lai) # fill values top of image
                lai *= scale_factor

                qa_fname = string.replace(fname, "b02", "b03")
                qa_fname = string.replace(qa_fname, "1000m_lai","1000m_quality")
                qa = gdal.Open(qa_fname)
                qa = qa.ReadAsArray()
                qa = np.where(qa > qa_valid_max, np.nan, qa)
                qa = np.where(np.isnan(lai), np.nan, qa)

                # Just take best QA = 0
                lai = np.where(qa != 0, np.nan, lai)
            else:
                lai = np.ones((nrows,ncols)) * np.nan

            data[j,:,:] = lai

            # close dataset
            lai = None

        # average across years
        data_ma = np.ma.MaskedArray(data, mask=np.isnan(data))
        clim = np.ma.average(data_ma, axis=0)

        clim = np.where(clim <= 0.0, np.nan, clim) # sea
        clim = np.ma.fix_invalid(clim, fill_value=-999.9) #remove masked array
        big_data[i,:,:] = clim

        #if doy == 17:
        #    x = big_data[i,:,:]
        #    x = np.where(x < -500, np.nan, x)
        #    plt.imshow(x)
        #    plt.colorbar()
        #    plt.show()

    big_data.tofile(f)

    print(big_data.shape)
    
if __name__ == "__main__":

    main()
    """
    #echo "00000000" | gawk -f ~/bin/awk/bit2d.awk
    #echo "00100000" | gawk -f ~/bin/awk/bit2d.awk
    #echo "00011000" | gawk -f ~/bin/awk/bit2d.awk
    #echo "00111000" | gawk -f ~/bin/awk/bit2d.awk

    bit = ((0 * 2**7) +  # bit 7
           (0 * 2**6) +  # bit 6
           (0 * 2**5) +  # bit 5
           (0 * 2**4) +  # bit 4
           (0 * 2**3) +  # bit 3
           (0 * 2**2) +  # bit 2
           (0 * 2**1) +  # bit 1
           (0 * 2**0))   # bit 0

    print bit

    bit = ((0 * 2**7) +  # bit 7
           (0 * 2**6) +  # bit 6
           (0 * 2**5) +  # bit 5
           (1 * 2**4) +  # bit 4
           (1 * 2**3) +  # bit 3
           (0 * 2**2) +  # bit 2
           (0 * 2**1) +  # bit 1
           (0 * 2**0))   # bit 0

    print bit

    bit = ((0 * 2**7) +  # bit 7
           (0 * 2**6) +  # bit 6
           (1 * 2**5) +  # bit 5
           (0 * 2**4) +  # bit 4
           (0 * 2**3) +  # bit 3
           (0 * 2**2) +  # bit 2
           (0 * 2**1) +  # bit 1
           (0 * 2**0))   # bit 0

    print bit

    bit = ((0 * 2**7) +  # bit 7
           (0 * 2**6) +  # bit 6
           (1 * 2**5) +  # bit 5
           (1 * 2**4) +  # bit 4
           (1 * 2**3) +  # bit 3
           (0 * 2**2) +  # bit 2
           (0 * 2**1) +  # bit 1
           (0 * 2**0))   # bit 0

    print bit
    """
