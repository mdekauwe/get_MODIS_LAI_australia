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
from mpl_toolkits.basemap import Basemap
import gdal
from mpl_toolkits.axes_grid1 import AxesGrid
import matplotlib.cm as cm
import string

import seaborn as sns
sns.set(style="white")


def cmap_discretize(cmap, N):
    """Return a discrete colormap from the continuous colormap cmap.

        cmap: colormap instance, eg. cm.jet.
        N: number of colors.

    Example
        x = resize(arange(100), (5,100))
        djet = cmap_discretize(cm.jet, 5)
        imshow(x, cmap=djet)
    """

    if type(cmap) == str:
        cmap = get_cmap(cmap)
    colors_i = np.concatenate((np.linspace(0, 1., N), (0.,0.,0.,0.)))
    colors_rgba = cmap(colors_i)
    indices = np.linspace(0, 1., N+1)
    cdict = {}
    for ki,key in enumerate(('red','green','blue')):
        cdict[key] = [ (indices[i], colors_rgba[i-1,ki], colors_rgba[i,ki]) \
                        for i in xrange(N+1) ]
    # Return colormap object.
    return matplotlib.colors.LinearSegmentedColormap(cmap.name + \
                                                     "_%d"%N, cdict, 1024)

def colorbar_index(cax=None, ncolours=None, cmap=None, orientation=None,
                   vmin=None, vmax=None):
    cmap = cmap_discretize(cmap, ncolours)
    mappable = cm.ScalarMappable(cmap=cmap)
    mappable.set_array([])
    mappable.set_clim(-0.5, ncolours+0.5)
    colorbar = plt.colorbar(mappable, cax=cax, orientation=orientation)
    colorbar.set_ticks(np.linspace(0, ncolours, ncolours))
    colorbar.set_ticklabels(np.linspace(vmin, vmax, ncolours))
    colorbar.set_label("LAI anomaly (yr-clim)", fontsize=16)




def main():

    ncols = 841
    nrows = 681
    ndays = 366

    f = open("modis_climatology_splined.bin", "r")
    data = np.fromfile(f).reshape((ndays,nrows,ncols))
    f.close()

    ncolours = 9
    vmin = -3
    vmax = 3

    cmap = sns.blend_palette(["#762a83", "white", "#1b7837"], ncolours, as_cmap=True)
    #cmap = sns.blend_palette(["white", "#1b7837"], ncolours, as_cmap=True)

    sns.set(style="white")

    fig = plt.figure(figsize=(10, 6))
    grid = AxesGrid(fig, [0.05,0.05,0.9,0.9], nrows_ncols=(1,1), axes_pad=0.1,
    		        cbar_mode='single', cbar_pad=0.4, cbar_size="7%",
		            cbar_location='bottom', share_all=True)
	# 111.975 + (841. * 0.05)
    # -44.025 + (681. * 0.05)
    m = Basemap(projection='cyl', llcrnrlon=111.975, llcrnrlat=-44.025, \
                urcrnrlon=154.025, urcrnrlat=-9.974999999999994, resolution='h')


    ax = grid[0]
    m.ax = ax


    shp_info = m.readshapefile('/Users/mdekauwe/research/Drought_linkage/'
                               'Bios2_SWC_1979_2013/'
                               'AUS_shape/STE11aAust',
                               'STE11aAust', drawbounds=True)


    #m.drawrivers(linewidth=0.5, color='k')

    ax.set_xlim(140.5, 154)
    ax.set_ylim(-38, -28)

    #cmap = cmap_discretize(plt.cm.YlGnBu, ncolours)



    climatology = data[24,:,:]
    scale_factor = 0.1
    lai_valid_max = 100
    qa_valid_max = 254
    ncols = 841
    nrows = 681

    fname = "hdfs/2003/MOD15A2.2003.025.aust.005.b02.1000m_lai.hdf"
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
    good_QA = np.array([0, 32])
    lai[qa != good_QA] = np.nan
    lai_std[qa != good_QA] = np.nan


    anomaly = lai-climatology



    m.imshow(anomaly, cmap,
             colors.Normalize(vmin=vmin, vmax=vmax, clip=True),
             origin='upper', interpolation='nearest')


    cbar = colorbar_index(cax=grid.cbar_axes[0], ncolours=ncolours, cmap=cmap,
                          orientation='horizontal', vmin=vmin, vmax=vmax)

    fig.savefig("/Users/mdekauwe/Desktop/LAI_anomaly.png", bbox_inches='tight',
                pad_inches=0.1, dpi=300)



    plt.show()


if __name__ == "__main__":

    main()
