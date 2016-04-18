#!/usr/bin/env python

"""
Extract a sub-sample of met pixels for Remko to run MAESPA

That's all folks.
"""
__author__ = "Martin De Kauwe"
__version__ = "1.0 (13.04.2016)"
__email__ = "mdekauwe@gmail.com"


import sys
import os
import shutil
import tarfile

row_st = 411
row_en = 461
col_st = 570
col_en = 840
print float(col_en - col_st)

#print float(row_en - row_st) / 5
#print float(col_en - col_st) / 25
#sys.exit()

idir = "pixels"
odir = "files_for_remko_LAI"
otar = odir + ".tar"

if os.path.exists(odir):
    shutil.rmtree(odir)

if not os.path.exists(odir):
    os.makedirs(odir)

# Extract roughly 20-25 by 20-25 pixels sq.
for r in xrange(row_st, row_en, 5):
    print r, row_en
    for c in xrange(col_st, col_en, 25):
        fn = "%d_%d_LAI.bin" % (r, c)
        ofn = os.path.join(odir, fn)
        try:
            shutil.copy(os.path.join(idir, fn), ofn)
        except:
            print "missing file"


tar = tarfile.open(otar, "w")
tar.add(odir)
tar.close()
