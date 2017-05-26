import csv
import json
import numpy as np
from palette import printPng

if __name__ == '__main__':
  import argparse
  argp = argparse.ArgumentParser()
  argp.add_argument('--json')
  argp.add_argument('input')
  args = argp.parse_args()

  name = args.input
  data = np.array(list(csv.reader(open(name))))
  data = data.astype(np.float)
  
  color = json.loads(open(args.json).read())
  printPng(data, color, name + '.png')
