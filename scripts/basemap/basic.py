import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from scipy.io.netcdf import netcdf_file
from mpl_toolkits.basemap import Basemap

f = netcdf_file('ph1.nc', 'r')
lats = f.variables['lat'][:]
lons = f.variables['lon'][:]
data = f.variables['t'][0,0]
f.close()

map = Basemap(resolution='l',lon_0=180)
xx, yy = np.meshgrid(lons, lats)
map.pcolormesh(xx, yy, np.squeeze(data))
plt.savefig('_basic.png')
