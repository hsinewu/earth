from scipy.io.netcdf import netcdf_file
from PIL import Image
from json import loads as json_loads
from bisect import bisect_left

# read netcdf
with netcdf_file('r85.nc', 'r') as f:
	lats = f.variables['lat'][:]
	lons = f.variables['lon'][:]
	data = f.variables['temp2'][0] # (time, lat, lon)

# read color data
with open("heatColor.json") as f2:
	heatColor = json_loads(f2.read())

# draw png in palette mode with pillow
size = data.shape
im = Image.new("P", (size[1], size[0]))
im.putpalette(heatColor['palette'])

for lt,ln in [(lat,lon) for lat in range(size[0]) for lon in range(size[1])]:
	da = data[lt,ln] - 273.15 # K to Celsius
	# if data value is higher than specified color range, give it last color
	if da >= heatColor['stops'][-1]:
		stop_index = len(heatColor['palette']) - 1
	else:
		stop_index = bisect_left( heatColor['stops'], da)
	im.putpixel((ln,lt), stop_index)

im.save("_basic.png")