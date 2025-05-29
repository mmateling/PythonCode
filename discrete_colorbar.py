# -----------------------------------------------------------------------------------------
#
# discrete_colorbar
#
#   Author: Marian Mateling (mateling@wisc.edu)
#
# -----------------------------------------------------------------------------------------

import numpy as np

import matplotlib as matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.cm import get_cmap

# ----------------------------------------------------------

if __name__=='__main__':

    # Creates an array (50x50) of random data b/w 200 and 300 (temp K)
    sample_data = np.random.uniform(low=200.0, high=300.0, size=(50,50))
    
    # Set data from 200 - 250 K to 1
    sample_data[(sample_data >= 200) & (sample_data < 250)] = 1
    
    # Set data from 250 - 273 K to 2
    sample_data[(sample_data >= 250) & (sample_data < 273)] = 2
    
    # Set data from 273 - 300 K to 3
    sample_data[(sample_data >= 273) & (sample_data < 300)] = 3   


  # PLOT DATA

    
    # Pick out colormap ('cool') and include number of levels (3)
    cmap = plt.get_cmap('cool', 3)

    cs = plt.contourf(lon, lat, sample_data, cmap = cmap, vmin = 1, vmax = 3)
    
    cb = plt.colorbar(cs, ticks = range(1,4), \
    	format=mticker.FixedFormatter(['Coldest', 'Cold', 'Warm']), shrink = 0.6)
    
    # Set tick locations to the middle of the colors on colorbar
    tick_locations = [(4/3.), 2, (8/3.)]
    
    cb.set_ticks(tick_locations)
    
    plt.show()