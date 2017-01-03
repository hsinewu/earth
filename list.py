from os import listdir as os_listdir
from json import dumps as json_dumps
import pprint


if __name__ == '__main__':
	dataset = {}
	for report in os_listdir('data'):
		items = os_listdir('data/'+report)
		files = os_listdir('data/%s/%s' % (report, items[0]))
		dataset[report] = {'items': items}
		dataset[report]["length"] = len( [ x for x in files if x.endswith('.png')])
	pprint.pprint(dataset)

	with open('_dataset.json', mode='x') as f:
		f.write( json_dumps( dataset))