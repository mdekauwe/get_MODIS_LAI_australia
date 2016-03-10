# Get MODIS LAI data for Australia

[Martin De Kauwe](https://mdekauwe.github.io/)

Get the MODIS LAI (or any...) data for Australia from the [NCI website] (http://remote-sensing.nci.org.au/u39/public/html/modis/lpdaac-mosaics-cmar/)

- get the data: download_MODIS_LAI_for_australia.py

- unzip files & degrade to 10 km to match AWAP: unzip_and_degrade_modis_data.py

- build climatology, weighting day sample by stdev layer: build_modis_climatology.py

- put a spline thought each pixel and extraplote to get 365 days of data: spline_modis_climatology.py
