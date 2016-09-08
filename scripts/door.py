#!/home/hsinewu/anaconda3/bin/python
import argparse
argp = argparse.ArgumentParser()
argp.add_argument( "time", help="specify the time of the day", type=int, choices=range(4))
argp.add_argument( "height", help="specify the height level", type=int, choices=range(16))
argp.add_argument( "kind", help="specify what kind of map to draw", choices=['pc', 'cnt', 'cntf'])
args = argp.parse_args()
print(args)

import numpy as np
from scipy.io.netcdf import netcdf_file
from mpl_toolkits.basemap import Basemap


import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

with netcdf_file('ph1.nc', 'r') as f:
	lats = f.variables['lat'][:]
	lons = f.variables['lon'][:]
	data = f.variables['t'][args.time, args.height]

fig = plt.figure(figsize=(15.36,7.68))
map = Basemap(resolution='l',lon_0=180)
xx, yy = np.meshgrid(lons, lats)

if args.kind == 'pc':
	map.pcolormesh(xx, yy, np.squeeze(data))
elif args.kind == 'cnt':
	map.contour(xx, yy, np.squeeze(data))
elif args.kind == 'cntf':
	map.contourf(xx, yy, np.squeeze(data))

fig.tight_layout()
fig.subplots_adjust(bottom = 0)
fig.subplots_adjust(top = 1)
fig.subplots_adjust(right = 1)
fig.subplots_adjust(left = 0)
plt.axis('off')
plt.savefig('output.png', bbox_inches='tight', pad_inches=0)
