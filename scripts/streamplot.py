import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from scipy.io.netcdf import netcdf_file
from mpl_toolkits.basemap import Basemap

f = netcdf_file('ph1.nc', 'r')
lats = f.variables['lat'][:]
lons = f.variables['lon'][:]
u = f.variables['u'][0,0]
v = f.variables['v'][0,0]
speed = np.sqrt(u*u+v*v)
f.close()

xx, yy = np.meshgrid(lons, lats)
map = Basemap(resolution='l',lon_0=180)
map.streamplot(xx, yy, u, v, color=speed, cmap=plt.cm.autumn, linewidth=0.5*speed)
plt.savefig('_streamplot.png')
