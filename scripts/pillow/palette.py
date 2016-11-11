from scipy.io.netcdf import netcdf_file
from PIL import Image
from json import loads as json_loads
from bisect import bisect_left
import numpy as np

ncFile = 'r85.nc'
vizItem = 'temp2'
colorFile = 'heatColor.json'
outputFile = '_scale.png'
outputSize = (512,256)

# read netcdf
with netcdf_file(ncFile, 'r') as f:
	data = f.variables[vizItem] # (time, lat, lon)

# read color data
with open(colorFile) as f2:
	colorTable = json_loads(f2.read())

# draw png in palette mode with pillow
def printPng(space, fileName, transform=lambda x:x):
	# map datas to indices according to colorTable
	vfunc = np.vectorize(lambda x: bisect_left( colorTable['stops'], transform(x) ) )
	arr = vfunc(space)

	im = Image.fromarray((arr).astype('uint8'), 'P')
	im.putpalette(colorTable['palette'])

	resizedImage = im.resize(outputSize)
	resizedImage.save(fileName)

printPng(data[0], outputFile, lambda x: x-273.15)