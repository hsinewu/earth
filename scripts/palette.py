from Printer import Printer
from scipy.io.netcdf import netcdf_file
import argparse

if __name__ == '__main__':
	argp = argparse.ArgumentParser()
	argp.add_argument('-i', '--items', nargs='+', default=['temp2'], help="List of variables in netcdf to be printed.")
	argp.add_argument('-t', '--time', default='2016120100', help="yyyyMMddhh, also name of netcdf file")
	argp.add_argument('-d', '--dhour', type=int, default=6, help="time interval of data")
	argp.add_argument('-f', '--force', dest='force', action='store_true', help="overwites if images already exists")
	argp.set_defaults(force=False)
	argp.add_argument('--src', default='.', help="optional")
	argp.add_argument('--dest', default='.', help="optional")
	args = argp.parse_args()

	# print a netcdf
	printer = Printer()
	printer.outdir = args.dest
	nc = '%s/%s.nc' % (args.src, args.time)
	with netcdf_file(nc, 'r') as f1:
		varis = {k:f1.variables[k][:] for k in args.items}
		printer.printgrids( varis, args.time, args.dhour, args.force)

