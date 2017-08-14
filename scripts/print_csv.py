import csv
import numpy as np
from Printer import Printer

if __name__ == '__main__':
  import sys

  name = sys.argv[2]
  with open(name) as f:
    data = f.read().split('\n')
    data = [ x.split(' ') for x in data]
    data = np.array(data)
  data = data.astype(np.float)
  
  printer = Printer()
  printer.setcolor( sys.argv[1])
  printer.printpng(data, name + '.png')
