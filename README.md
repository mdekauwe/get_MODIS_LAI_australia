# Get MODIS LAI data for Australia

[Martin De Kauwe](https://mdekauwe.github.io/)

Get the MODIS LAI (or any...) data for Australia from the [NCI website] (http://remote-sensing.nci.org.au/u39/public/html/modis/lpdaac-mosaics-cmar/)

- get the data: download_MODIS_LAI_for_australia.py

- unzip files & degrade to 10 km to match AWAP: unzip_and_degrade_modis_data.py

- build climatology, weighting day sample by stdev layer: build_modis_climatology.py

- put a spline though each pixel and extraplote to get 366 days of data: spline_modis_climatology.py

- break the Australia climatology file into individual pixels covering NSW. Each binary file will contain nvars=2, ndays=366, where nvar=0 is the interpolated data and nvar=1 is the climatology data (8 days, gaps=-999.9) before the interpolation: breakup_into_pixels_NSW.py
