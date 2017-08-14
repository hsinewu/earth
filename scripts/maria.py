from yaml import load as yaml_load
from math import sqrt
import mysql.connector
import numpy as np
from Printer import Printer

def printFromDatabase(db_cfg):
	try:
		db = mysql.connector.connect(**db_cfg)
		cursor = db.cursor( buffered=True)

		print( "Execute query...")
		elm, tbl = 'olr', ''
		cursor.execute( "select %s from %s;" % (elm, tbl))
		data = cursor.fetchall()
		w = int( sqrt( len(data)/2))
		data = np.reshape( data, (w, w*2))

		print( "Generate png...")
		printer = Printer()
		printer.setcolor('json/olr.json')
		printer.printpng( data, "olr.png")
		db.close()

	except mysql.connector.Error as err:
		print( "Error occurs upon connection: ")
		print( err.msg)

if __name__ == '__main__':
	with open('database.yaml') as f:
		cfg = yaml_load( f.read())
	printFromDatabase( cfg)
