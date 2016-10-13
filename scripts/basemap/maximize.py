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

fig = plt.figure(figsize=(15.36,7.68))
map = Basemap(resolution='l',lon_0=180)
xx, yy = np.meshgrid(lons, lats)
map.pcolormesh(xx, yy, np.squeeze(data))
fig.tight_layout()
fig.subplots_adjust(bottom = 0)
fig.subplots_adjust(top = 1)
fig.subplots_adjust(right = 1)
fig.subplots_adjust(left = 0)
plt.axis('off')
plt.savefig('_maximize.png', bbox_inches='tight', pad_inches=0)

