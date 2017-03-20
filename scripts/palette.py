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

def batchPng(opt, dh=6):
	import logging as log
	if opt.verbose:
		log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
	
	for m, d in [ (x, y) for x in opt.months for y in opt.dates ]:
		ifn = '2016%02d%02d00.nc' % (m, d)
		dir1 = ifn[:-3]
		if exists(dir1): # .nc
			if not opt.force:
				log.warn("Folder %s exists, skipped" % dir1)
				continue
		else:
			log.info("Creating %s" % dir1)
			makedirs(dir1)
		log.info("Write to %s" % dir1)

		with netcdf_file(ifn, 'r') as f1:
			for item in opt.items:
				dir2 = "%s/%s"%(dir1, item)
				if exists(dir2):
					if not opt.force:
						log.warn("Sub folder %s exists, skipped" % dir2)
						continue
				else:
					log.info("Creating %s" % dir2)
					makedirs(dir2)
				log.info("Write to %s" % dir2)
				vari3 = f1.variables[item]
				json1 = 'json/%s.json'%item
				json1 = json1 if exists(json1) else 'json/_%s.json'%item
				with open(json1) as f2:
					color = loads(f2.read())
				for i in range(opt.length):
					ofn = '%s/%s/%s.png' % ( dir1, item, timeStr(2016, m, d, i*dh))
					printPng( vari3[i], color, ofn)

if __name__ == '__main__':
	from scipy.io.netcdf import netcdf_file
	from json import loads
	from os import makedirs
	from os.path import exists

	import argparse
	argp = argparse.ArgumentParser()
	argp.add_argument('-i', '--items', nargs='+', default=['temp2'])
	argp.add_argument('-m', '--months', nargs='+', type=int, default=[12])
	argp.add_argument('-d', '--dates', nargs='+', type=int, default=range(1,11))
	argp.add_argument('-f', '--force', dest='force', action='store_true')
	argp.add_argument('-v', '--verbose', dest='verbose', action='store_true')
	argp.set_defaults(verbose=False, force=False)
	argp.add_argument('-l', '--length', type=int, default=181)
	args = argp.parse_args()
	batchPng(args)