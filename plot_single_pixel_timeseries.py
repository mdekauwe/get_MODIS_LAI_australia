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


ncols = 841
nrows = 681
ndays = 366

f = open("modis_climatology_splined.bin", "r")
data = np.fromfile(f).reshape((ndays,nrows,ncols))
f.close()

ncols = 841
nrows = 681
ndays = 46

f = open("modis_climatology.bin", "r")
raw_data = np.fromfile(f).reshape((ndays,nrows,ncols))
f.close()

plt.plot(np.arange(1.,367), data[:,413,749], "k-")
plt.plot(np.arange(1, 361+8, 8), raw_data[:,413,749], "ro")
plt.ylim(0, 1.3)



plt.show()
