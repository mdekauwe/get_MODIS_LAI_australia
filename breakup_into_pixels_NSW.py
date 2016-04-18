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

def main():

    ncols = 841
    nrows = 681
    ndays = 366
    nvars = 2
    row_st = 360
    row_en = 560
    col_st = 570
    col_en = 840

    out_dirname = "pixels"
    if os.path.exists(out_dirname):
        shutil.rmtree(out_dirname)
        os.mkdir(out_dirname)

    f = open("modis_climatology_splined.bin", "r")
    data = np.fromfile(f).reshape((nvars,ndays,nrows,ncols))
    f.close()

    for row in xrange(row_st, row_en):
        for col in xrange(col_st, col_en):
            pixel = data[:,:,row,col]

            # i.e. don't write the bad pixels out
            if np.all(pixel[0,:] > -500.0):
                pixel.tofile("pixels/%d_%d_LAI.bin" % (row, col))

    out_fn = "NSW_LAI_pixels.tar.gz"
    with tarfile.open(out_fn, "w:gz") as tar:
        for name in glob.glob("pixels/*.bin"):
            tar.add(name)

    # clean up
    if os.path.exists(out_dirname):
        shutil.rmtree(out_dirname)

    """
    data = np.fromfile("pixels/%d_%d_LAI.bin" % (450, 717))

    data1 = data.reshape(nvars, ndays)[0,:]
    data2 = data.reshape(nvars, ndays)[1,:]

    x1 = np.arange(1.,367)
    x2 = np.arange(1, 361+8, 8)
    plt.plot(x1, data1, "r-")
    plt.plot(x2, data2[data2>-500.0], "ko")
    plt.show()
    """

if __name__ == "__main__":

    main()
