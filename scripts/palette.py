from Printer import Printer

def printFile(ncdir, tstr, *args):
	printer = Printer()
	nc = '%s/%s.nc' % (ncdir, tstr)
	with netcdf_file(nc, 'r') as f1:
		printer.printsource(f1.variables, tstr, *args)

# def batchPng(opt, dh=6):
# 	# TODO: adapt to cli option change
# 	if opt.verbose:
# 		log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
	
# 	for m, d in [ (x, y) for x in opt.months for y in opt.dates ]:
# 		ifn = '2016%02d%02d00.nc' % (m, d)
# 		dir1 = opt.dest + '/' + ifn[:-3]
# 		if mkdir(dir1, opt.force): # .nc
# 			continue
# 		printFile(opt.src+'/'+ifn, m, d, dh, opt.items, dir1, opt.force)

if __name__ == '__main__':
	from scipy.io.netcdf import netcdf_file
	# import logging as log

	import argparse
	argp = argparse.ArgumentParser()
	argp.add_argument('-i', '--items', nargs='+', default=['temp2'], help="List of variables in netcdf to be printed.")
	argp.add_argument('-t', '--time', default='2016120100', help="yyyyMMddhh, also name of netcdf file")
	# argp.add_argument('-d', '--dates', nargs='+', type=int, default=[1])
	argp.add_argument('-d', '--dhour', type=int, default=6, help="time interval of data")
	argp.add_argument('-f', '--force', dest='force', action='store_true', help="overwites if images already exists")
	# argp.add_argument('-v', '--verbose', dest='verbose', action='store_true')
	argp.set_defaults(verbose=False, force=False)
	argp.add_argument('--src', default='.', help="optional")
	argp.add_argument('--dest', default='.', help="optional")
	args = argp.parse_args()
	printFile(args.src, args.time, args.dhour, args.items, args.dest, args.force)
