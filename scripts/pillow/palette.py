from scipy.io.netcdf import netcdf_file
from PIL import Image
from json import loads as json_loads
from bisect import bisect_left
from numpy import interp

ncFile = 'r85.nc'
vizItem = 'temp2'
colorFile = 'heatColor.json'
outputFile = '_scale.png'

# read netcdf
with netcdf_file(ncFile, 'r') as f:
	lats = f.variables['lat'][:]
	lons = f.variables['lon'][:]
	data = f.variables[vizItem][0] # (time, lat, lon)

# read color data
with open(colorFile) as f2:
	colorTable = json_loads(f2.read())

# draw png in palette mode with pillow
size = (512,256)
dsize = data.shape
im = Image.new("P", size)
im.putpalette(colorTable['palette'])

for px,py in [(x,y) for x in range(size[0]) for y in range(size[1])]:
	ln, lt = interp(px, [0, size[0]], [0, dsize[1]]), interp(py, [0, size[1]], [0, dsize[0]])
	da = data[int(lt), int(ln)] - 273.15 # K to Celsius
	# if data value is higher than specified color range, give it last color
	if da >= colorTable['stops'][-1]:
		stop_index = len(colorTable['palette']) - 1
	else:
		stop_index = bisect_left( colorTable['stops'], da)
	im.putpixel((px,py), stop_index)

im.save(outputFile)