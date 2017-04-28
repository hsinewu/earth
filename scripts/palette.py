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

def timeStr(tstr, h=0):
	import datetime
	d0 = datetime.datetime.strptime(tstr, '%Y%m%d%H')
	dh = datetime.timedelta(hours=1)
	return (d0+dh*h).strftime("%Y%m%d%H")

def mkdir(dp, force):
	if exists(dp): # .nc
		if not force:
			log.warn("Folder %s exists, skipped" % dp)
			return 1
	else:
		log.info("Creating %s" % dp)
		makedirs(dp)
	log.info("Write to %s" % dp)

def printFile(ncdir, tstr, dh, items, outdir, force=False):
	nc = '%s/%s.nc' % (ncdir, tstr)
	with netcdf_file(nc, 'r') as f1:
		for item in items:
			dir2 = "%s/%s/%s"%(outdir, tstr, item)
			if mkdir(dir2, force):
				continue
			vari3 = f1.variables[item]
			json1 = 'json/%s.json' % item
			if exists(json1):
				with open(json1) as f2:
					color = loads(f2.read())
			else:
					from make_json import parseColor
					color = parseColor(vari3[:])
			for i in range(len(vari3[:])):
				ofn = '%s/%s.png' % ( dir2, timeStr(tstr, i*dh))
				printPng( vari3[i], color, ofn)

def batchPng(opt, dh=6):
	# TODO: adapt to cli option change
	if opt.verbose:
		log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
	
	for m, d in [ (x, y) for x in opt.months for y in opt.dates ]:
		ifn = '2016%02d%02d00.nc' % (m, d)
		dir1 = opt.dest + '/' + ifn[:-3]
		if mkdir(dir1, opt.force): # .nc
			continue
		printFile(opt.src+'/'+ifn, m, d, dh, opt.items, dir1, opt.force)

if __name__ == '__main__':
	from scipy.io.netcdf import netcdf_file
	from json import loads
	from os import makedirs
	from os.path import exists
	import logging as log

	import argparse
	argp = argparse.ArgumentParser()
	argp.add_argument('-i', '--items', nargs='+', default=['temp2'])
	argp.add_argument('-t', '--time', default='2016120100')
	# argp.add_argument('-d', '--dates', nargs='+', type=int, default=[1])
	argp.add_argument('-d', '--dhour', type=int, default=6)
	argp.add_argument('-f', '--force', dest='force', action='store_true')
	argp.add_argument('-v', '--verbose', dest='verbose', action='store_true')
	argp.set_defaults(verbose=False, force=False)
	argp.add_argument('--src', default='.')
	argp.add_argument('--dest', default='.')
	args = argp.parse_args()
	printFile(args.src, args.time, args.dhour, args.items, args.dest, args.force)
