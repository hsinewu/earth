from scipy.io.netcdf import netcdf_file
from PIL import Image
from json import loads as json_loads
from bisect import bisect_left
import numpy as np

colorFile = 'heatColor.json'
# outputSize = (512,256)

# read color data
with open(colorFile) as f:
	colorTable = json_loads(f.read())

# draw png in palette mode with pillow
def printPng(space, fileName, transform=lambda x:x):
	# map datas to indices according to colorTable
	vfunc = np.vectorize(lambda x: bisect_left( colorTable['stops'], transform(x) ) )
	arr = vfunc(space)

	im = Image.fromarray((arr).astype('uint8'), 'P')
	im.putpalette(colorTable['palette'])

	if 'outputSize' in globals():
		im = im.resize(outputSize)
	im.save(fileName)

if __name__ == '__main__':
	ncFile = 'r85.nc'
	vizItem = 'temp2'
	outputFile = '_scale.png'

	# read netcdf
	with netcdf_file(ncFile, 'r') as f:
		data = f.variables[vizItem] # (time, lat, lon)

	printPng(data[0], outputFile, lambda x: x-273.15)