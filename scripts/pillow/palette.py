from scipy.io.netcdf import netcdf_file
from PIL import Image
from json import loads as json_loads
from bisect import bisect_left

ncFile = 'r85.nc'
vizItem = 'temp2'
colorFile = 'heatColor.json'
outputFile = '_scale.png'
outputSize = (512,256)

# read netcdf
with netcdf_file(ncFile, 'r') as f:
	lats = f.variables['lat'][:]
	lons = f.variables['lon'][:]
	data = f.variables[vizItem] # (time, lat, lon)

# read color data
with open(colorFile) as f2:
	colorTable = json_loads(f2.read())

# draw png in palette mode with pillow
def printPng(space, fileName, transform=lambda x:x):
	size = space.shape
	im = Image.new("P", (size[1], size[0]))
	im.putpalette(colorTable['palette'])

	for lt,ln in ((lat,lon) for lat in range(size[0]) for lon in range(size[1])):
		da = transform( space[lt, ln])
		stop_index = bisect_left( colorTable['stops'], da)
		im.putpixel((ln,lt), stop_index)

	resizedImage = im.resize(outputSize)
	resizedImage.save(fileName)

printPng(data[0], outputFile, lambda x: x-273.15)