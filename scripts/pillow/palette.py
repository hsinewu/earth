from scipy.io.netcdf import netcdf_file
from PIL import Image
from json import loads as json_loads
from bisect import bisect_left
import numpy as np

colorFile = 'heatColor.json'
# outputSize = (512,256)

def printPng(space, colorTable, ofn, transform=lambda x:x):
	# map datas to indices according to colorTable
	vfunc = np.vectorize(lambda x: bisect_left( colorTable['stops'], transform(x) ) )
	arr = vfunc(space)

	im = Image.fromarray((arr).astype('uint8'), 'P')
	im.putpalette(colorTable['palette'])

	if 'outputSize' in globals():
		im = im.resize(outputSize)
	im.save(ofn)

if __name__ == '__main__':
	ncFile = 'file.nc'
	items = ['var1', 'var2']

	with netcdf_file(ncFile, 'r') as f1:
		for item in items:
			vari3 = f1.variables[item]
			with open('json/%s.json'%item) as f2:
				color = json_loads(f2.read())
			for i in range(181):
				printPng( vari3[i], color, '%s/%d.png'%(item,i))
