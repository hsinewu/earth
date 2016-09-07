import numpy as np
# import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

fig = plt.figure(figsize=(15.36,7.68))

bmap = Basemap(resolution='l')
bmap.drawlsmask(land_color='coral',ocean_color='aqua',lakes=True)
# bmap.bluemarble()

fig.tight_layout()
fig.subplots_adjust(bottom = 0)
fig.subplots_adjust(top = 1)
fig.subplots_adjust(right = 1)
fig.subplots_adjust(left = 0)
plt.axis('off')
plt.savefig('cart.png', bbox_inches='tight', pad_inches=0)

