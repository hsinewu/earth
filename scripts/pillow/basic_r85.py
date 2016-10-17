from scipy.io.netcdf import netcdf_file
from PIL import Image
import json
from bisect import bisect_left

# read netcdf
with netcdf_file('r85.nc', 'r') as f:
	lats = f.variables['lat'][:]
	lons = f.variables['lon'][:]
	data = f.variables['temp2'][0] # (time, lat, lon)

# read color data
with open("heatColor.json") as f2:
	heatColor = json.loads(f2.read())

# draw png in palette mode with pillow
size = (len(lons), len(lats))
im = Image.new("P", size)
im.putpalette(heatColor['palette'])

for px,py in [(x,y) for x in range(size[0]) for y in range(size[1])]:
	da = data[py,px] - 273.15 # K to Celsius
	# if data value is higher than specified color range, give it last color
	if da >= heatColor['stops'][-1]:
		stop_index = len(heatColor['palette']) - 1
	else:
		stop_index = bisect_left( heatColor['stops'], da)
	im.putpixel((px,py), stop_index)	# check color literal format

im.save("_basic.png")