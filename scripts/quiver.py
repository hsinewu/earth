import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from scipy.io.netcdf import netcdf_file
from mpl_toolkits.basemap import Basemap

step = 32
f = netcdf_file('ph1.nc', 'r')
lats = f.variables['lat'][::step]
lons = f.variables['lon'][::step]
u = f.variables['u'][0,0,::step,::step]
v = f.variables['v'][0,0,::step,::step]
speed = np.sqrt(u*u+v*v)
f.close()

xx, yy = np.meshgrid(lons, lats)
map = Basemap(resolution='l',lon_0=180)
map.quiver(xx, yy, u, v, speed, cmap=plt.cm.autumn)
plt.savefig('_quiver.png')
