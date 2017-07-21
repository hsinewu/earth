import csv
import json
import numpy as np
from palette import printPng

if __name__ == '__main__':
  import sys

  name = sys.argv[2]
  with open(name) as f:
    data = f.read().split('\n')
    data = [ x.split(' ') for x in data]
    print( [len(data), len(data[0])])
    data = np.array(data)
  data = data.astype(np.float)
  
  color = json.loads(open( sys.argv[1] ).read())
  printPng(data, color, name + '.png')
