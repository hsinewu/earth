from yaml import load as yaml_load
from math import sqrt
import mysql.connector
import numpy as np
from palette import pringPng

with open('database.yaml') as f:
	db_cfg = yaml_load(f.read())

try:
	print("Connect to database...")
	db = mysql.connector.connect(**db_cfg)
	cursor = db.cursor(buffered=True)
	print("Execute query...")
	cursor.execute("select olr from %s;")
	data = cursor.fetchall()
	w = int( sqrt( len(data)/2))
	data = np.reshape( data, (w, w*2))

	print("Generate png...")
	printPng( data, "olr.png")
	db.close()
	print("Database closed successfully")

except mysql.connector.Error as err:
	print("Error occurs upon connection: ")
	print(err.msg)