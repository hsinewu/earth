from PIL import Image
from bisect import bisect_left
from json import loads
from os import makedirs
from os.path import exists
import datetime
import numpy as np

class Printer:
  def __init__(self):
    self.outputSize = None
    self.outdir = '.'
    self.color = None

  def setcolor(self, json):
    with open(json) as f: # WARN: unhandled non-exist file
      self.color = loads(f.read())

  def printpng(self, space, ofn):
    if self.color is None:
      raise NameError('Color uninitialized')
    f = (lambda x: x+self.color['offset']) if 'offset' in self.color else lambda x:x
    # map datas to indices according to self.color
    vfunc = np.vectorize(lambda x: bisect_left( self.color['stops'], f(x) ) )
    arr = vfunc(space)

    im = Image.fromarray((arr).astype('uint8'), 'P')
    im.putpalette(self.color['palette'])

    if self.outputSize:
      im = im.resize(outputSize)
    im.save(ofn)

  def __timestr__(self, tstr, h=0):
    d0 = datetime.datetime.strptime(tstr, '%Y%m%d%H')
    dh = datetime.timedelta(hours=1)
    return (d0+dh*h).strftime("%Y%m%d%H")

  def __mkdir__(self, dp, force):
    if exists(dp): # .nc
      if not force:
        print("Skip existing folder %s, use -f" % dp)
        return 1
    else:
      makedirs(dp)

  def printgrids(self, grids, tstr, dh, force=False):
    for item, vari in grids.items():
      dir2 = "%s/%s/%s" % (self.outdir, tstr, item)
      if self.__mkdir__(dir2, force):
        continue
      json1 = 'json/%s.json' % item
      self.setcolor( json1)
      for i in range(len(vari)):
        ofn = '%s/%s.png' % ( dir2, self.__timestr__(tstr, i*dh))
        self.printpng( vari[i], ofn)
