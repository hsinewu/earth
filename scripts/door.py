#!/home/hsinewu/anaconda3/bin/python
import argparse
argp = argparse.ArgumentParser()
argp.add_argument( "time", help="specify the time of the day", type=int, choices=range(4))
argp.add_argument( "height", help="specify the height level", type=int, choices=range(16))
argp.add_argument( "kind", help="specify what kind of map to draw", choices=['cnt', 'cntf', 'pc', 'qv', 'sp'])
args = argp.parse_args()
print(args)

import numpy as np
from scipy.io.netcdf import netcdf_file
from mpl_toolkits.basemap import Basemap


import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

with netcdf_file('ph1.nc', 'r') as f:
	if args.kind in ['qv', 'sp']:
		step = 32
		lats = f.variables['lat'][::step]
		lons = f.variables['lon'][::step]
		u = f.variables['u'][0,0,::step,::step]
		v = f.variables['v'][0,0,::step,::step]
		speed = np.sqrt(u*u+v*v)
	else:
		lats = f.variables['lat'][:]
		lons = f.variables['lon'][:]
		data = f.variables['t'][args.time, args.height]

fig = plt.figure(figsize=(15.36,7.68))
bmap = Basemap(resolution='l',lon_0=179.9)
xx, yy = np.meshgrid(lons, lats)

if args.kind == 'cnt':
	bmap.contour(xx, yy, np.squeeze(data))
elif args.kind == 'cntf':
	bmap.contourf(xx, yy, np.squeeze(data))
elif args.kind == 'pc':
	bmap.pcolormesh(xx, yy, np.squeeze(data))
elif args.kind == 'qv':
	bmap.quiver(xx, yy, u, v, speed, cmap=plt.cm.autumn)
elif args.kind == 'sp':
	bmap.streamplot(xx, yy, u, v, color=speed, cmap=plt.cm.autumn, linewidth=0.5*speed)

fig.tight_layout()
fig.subplots_adjust(bottom = 0)
fig.subplots_adjust(top = 1)
fig.subplots_adjust(right = 1)
fig.subplots_adjust(left = 0)
plt.axis('off')
plt.savefig('output.png', bbox_inches='tight', pad_inches=0)
