from PIL import Image
from bisect import bisect_left
import numpy as np

def printPng(space, colorTable, ofn, outputSize=None):
	f = (lambda x: x+colorTable['offset']) if 'offset' in colorTable else lambda x:x
	# map datas to indices according to colorTable
	vfunc = np.vectorize(lambda x: bisect_left( colorTable['stops'], f(x) ) )
	arr = vfunc(space)

	im = Image.fromarray((arr).astype('uint8'), 'P')
	im.putpalette(colorTable['palette'])

	if outputSize:
		im = im.resize(outputSize)
	im.save(ofn)

def timeStr(y, m, d, h=0):
	import datetime
	d0 = datetime.datetime(y, m, d)
	dh = datetime.timedelta(hours=1)
	return (d0+dh*h).strftime("%Y%m%d%H")


if __name__ == '__main__':
	from scipy.io.netcdf import netcdf_file
	from json import loads
	from os import makedirs
	from os.path import exists
	
	items = ['temp2', 'slp', 'aprs', 'slm', 'tsw', 'precip', 'ws', 'qvi', 'disch', 'seaice', 'sn']

	for m, d in [ (x, y) for x in [12] for y in range(1,11) ]:
		ifn = '2016%02d%02d00.nc' % (m, d)
		if exists(ifn[:-3]): # .nc
			print("Folder exists, skip")
			continue
		makedirs(ifn[:-3])

		with netcdf_file(ifn, 'r') as f1:
			for item in items:
				print("%s/%s"%(ifn[:-3], item))
				makedirs("%s/%s"%(ifn[:-3], item))
				vari3 = f1.variables[item]
				with open('json/%s.json'%item) as f2:
					color = loads(f2.read())
				for i in range(181):
					ofn = '%s/%s/%s.png' % ( ifn[:-3], item, timeStr(2016, m, d, i*6))
					printPng( vari3[i], color, ofn)
