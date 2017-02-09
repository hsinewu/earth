import mysql.connector
from os import fork
import pprint

db_cfg = {
	'host': '',
	'database': '',
	'user': '',
	'password': ''
}
try:
	db = mysql.connector.connect(**db_cfg)
	cursor = db.cursor( buffered=True)

	print( "Execute query...")
	elm, tbl = 'BlkTableName, HostName', 'slpBlockList'
	cursor.execute( "select %s from %s;" % (elm, tbl))
	data = cursor.fetchall()
	pprint.pprint(data)

	db.close()
except mysql.connector.Error as err:
	print( "Error occurs upon connection: ")
	print( err.msg)
	