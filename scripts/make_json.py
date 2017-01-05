import numpy as np
import json

def printJson(data, name):
	stops = [ np.percentile(data, x) for x in [20, 40, 60, 80]]
	palette = np.repeat( [0, 63, 127, 191, 255], 3)

	obj = {'stops': stops, 'palette': palette.tolist()}
	with open( '%s.json'%name, 'x') as f:
		txt = json.dumps(obj)
		f.write(txt)

if __name__ == '__main__':
	fileName = 'file.nc'
	item = 'var'
	from scipy.io.netcdf import netcdf_file
	with netcdf_file( fileName, 'r') as f:
		data = f.variables[item]
		printJson(data[:], item)