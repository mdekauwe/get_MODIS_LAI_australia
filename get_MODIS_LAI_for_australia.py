#!/usr/bin/env python
"""
Download the MODIS LAI data from the NCI websits
http://remote-sensing.nci.org.au/u39/public/html/modis/lpdaac-mosaics-cmar/

Notes:
-----
* Mosaiced and remapped data from the USGS LPDAAC for the Australian continent
  and Tasmania. Some products are also available for New Zealand.
* These products are produced from the original tiles downloaded from
  USGS (https://lpdaac.usgs.gov). The tiles are mosaiced and reprojected using
  the MODIS Reprojection Tool. Mosiacs are separated into individual bands for
  each product and reformatted from HDF-EOS to standard HDF4 with a consistent
  file, SDS and attribute naming scheme (see the documentation for details).

* NB. I say LAI, but the script is generic enough that it could be tweaked.
"""

import os
import sys
import urllib
import calendar
import datetime as dt

__author__  = "Martin De Kauwe"
__version__ = "1.0 (29.02.2016)"
__email__   = "mdekauwe@gmail.com"

def get_data(years, product_code, collection, label, band):

    out_fdir = "hdf_zipped"
    if not os.path.exists(out_fdir):
        os.makedirs(out_fdir)

    base_url = ("http://remote-sensing.nci.org.au/u39/public/data/modis/"
                "lpdaac-mosaics-cmar/v1-hdf4/aust/")

    for yr in years:
        for doy in xrange(001, 366, 8):
            # HTTP needs to know DOY and day, month, year, so figure it out
            d = dt.datetime.strptime("%s %s" % (str(yr), str(doy)), "%Y %j")
            date_str = d.strftime('%Y.%m.%d')

            url = base_url + "%s.%s/%s/"  % (product_code, collection, date_str)
            if doy < 10:
                fn = "%s.%s.00%s.aust.%s.%s.%s.hdf.gz" % (product_code, yr,
                                                          doy, collection,
                                                          band, label)
            elif doy > 10 and doy < 100:
                fn = "%s.%s.0%s.aust.%s.%s.%s.hdf.gz" % (product_code, yr,
                                                         doy, collection,
                                                         band, label)

            in_url = os.path.join(url, fn)
            out_path = os.path.join(out_fdir, fn)
            urllib.urlretrieve(in_url, out_path)


if __name__ == "__main__":

    years = [2014]
    dataset = "MOD15A2.005"
    product_code = "MOD15A2"
    collection = "005"

    band = "b02"
    label = "1000m_lai"
    get_data(years, product_code, collection, label, band)

    band = "b03"
    label = "1000m_quality"
    get_data(years, product_code, collection, label, band)

    band = "b06"
    label = "1000m_lai_stdev"
    get_data(years, product_code, collection, label, band)
