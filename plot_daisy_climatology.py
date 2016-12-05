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

    fname = "modis_climatology.bin"
    data = np.fromfile(fname).reshape((ndays,nrows,ncols))
    data = np.where(data < -500, np.nan, data)

    # there are 46 timesteps with 8 day gaps
    # for i in range(1, 366, 8): print(i)

    plt.imshow(data[0,:,:])
    plt.colorbar()
    plt.show()


if __name__ == "__main__":

    main()
