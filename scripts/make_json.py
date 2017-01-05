import numpy as np
import json
from os.path import exists

def printJson(vari, ofn):
	if exists(ofn):
		return print("%s file exist"%ofn)

	stops = [ np.percentile(vari, x) for x in [20, 40, 60, 80]]
	palette = np.repeat( [0, 63, 127, 191, 255], 3)

	obj = {'stops': stops, 'palette': palette.tolist()}
	with open( ofn, 'x') as f:
		txt = json.dumps(obj)
		f.write(txt)

if __name__ == '__main__':
	ifn = 'file.nc'
	items = ['var1', 'var2']

	from scipy.io.netcdf import netcdf_file
	with netcdf_file( ifn, 'r') as f:
		for itm in items:
			data = f.variables[itm]
			printJson(data[:], itm+'.json')
