#!/home/hsinewu/anaconda3/bin/python
import numpy as np
from scipy.io.netcdf import netcdf_file
from mpl_toolkits.basemap import Basemap
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

if len(sys.argv) != 3 :
	print( "Hsine is expecting len(argv) == 3)")
	exit()
time, height = int( sys.argv[1]), int( sys.argv[2])

with netcdf_file('ph1.nc', 'r') as f:
	lats = f.variables['lat'][:]
	lons = f.variables['lon'][:]
	data = f.variables['t'][time, height]

map = Basemap(resolution='l',lon_0=180)
xx, yy = np.meshgrid(lons, lats)
map.pcolormesh(xx, yy, np.squeeze(data))
map.drawcoastlines()
map.drawcountries()
plt.savefig('output.png')
