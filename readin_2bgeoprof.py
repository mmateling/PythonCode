# ----------------------------------------------------------------------
#
#  readin_plot_2bgeoprof_vertZ
#
#   Author: Marian Mateling (mateling@wisc.edu)
#
# ----------------------------------------------------------------------

import numpy as np
from netCDF4 import Dataset
from glob import glob
from datetime import datetime
import matplotlib.pyplot as plt
import pyhdf.SD
import pyhdf.HDF

# Script written and provided by Norm Wood (norman.wood@ssec.wisc.edu)
import read_var_eos as eos

# ----------------------------------------------------------------------

def do_work(filename):

	z, lat, lon, clutter, sfc_bin, datestr = readin_file(filename)

	inds = index_data(lat, lon)

	plot_z(z[inds], lat[inds], lon[inds], sfc_bin[inds], datestr)
	
# ----------------------------------------------------------------------

def readin_file(filename):
	
	f_SD_ptr = pyhdf.SD.SD(filename, pyhdf.SD.SDC.READ)
	f_VD_ptr = pyhdf.HDF.HDF(filename, pyhdf.HDF.HC.READ)
	
	z = eos.get_2D_var(f_SD_ptr, f_VD_ptr, 'Radar_Reflectivity')
	clutter = eos.get_1D_var(f_VD_ptr, 'Clutter_reduction_flag')
	print(eos.get_0D_var(f_VD_ptr, 'Vertical_binsize'))
	#height = 0	
	#height = eos.get_1D_var(f_VD_ptr, 'height')
	height_bin = eos.get_1D_var(f_VD_ptr, 'SurfaceHeightBin')
	lat = eos.get_1D_var(f_VD_ptr, 'Latitude')
	lon = eos.get_1D_var(f_VD_ptr, 'Longitude')
	f_VD_ptr.close()
	f_SD_ptr.end()

	# Atlantic: Lat 45 to 82, Lon -76 to 40
	lats = lat.T[0]
	lons = lon.T[0]
	height_bins = height_bin.T[0]
	clutters = clutter.T[0]
	
	datestr = str(datetime.strptime(filename[:7], '%Y%j').date())
			
	return z, lats, lons, clutters, height_bins, datestr
	
# ----------------------------------------------------------------------
	
def index_data(lat, lon):

	# latlon = lat max, lon max, lat min, lon min
	latlon = [-60.08, -18.05, -71.44, -28.55]

	inds = np.where(np.logical_and(np.logical_and(lat >= latlon[2], \
	lat < latlon[0]), np.logical_and(lon >= latlon[3], lon < latlon[1])))[0]
	
	return inds
	
# ----------------------------------------------------------------------

def plot_z(z, lat, lon, sfc_bin, datestr):
	
	# Flip the value of the surface bin; bin 104 is surface, not 125!
	surface_line = np.asarray([int(105 - x) for x in sfc_bin])

	plt.figure(figsize=(16,8))

	cmap = plt.get_cmap('gist_ncar')
		
	# For masked values (< -25 dbz)
	cmap.set_bad(color='white')
	
	# For values exceeding ("over") colorbar range
	cmap.set_over(color='darkgrey')

	z = np.ma.masked_less(z, -25)

	cs = plt.pcolormesh(np.flipud(z.T)[21:47], cmap = cmap, \
		vmin=-25, vmax=20)

	plot_xy_labels(lat, lon, plt)
	
	plt.plot(surface_line, color='k', linewidth=2)

	cb = plt.colorbar(cs)

	cb.set_label('dBZe')

	cb.set_ticks(np.arange(-25, 25, 5))

	save_name = plot_details(plt, datestr)

	plt.show()

	plt.savefig(save_name, bbox_inches='tight')
	
# ----------------------------------------------------------------------

def plot_xy_labels(lat, lon, plt):

	deg = u"\N{DEGREE SIGN}"

	xx = len(lat)/2

	x_labels = [str(lat[0])[:6]+deg+', '+str(lon[0])[:6]+deg, \
	str(lat[xx])[:6]+deg+', '+str(lon[xx])[:6]+deg, \
	str(lat[-1])[:6]+deg+', '+str(lon[-1])[:6]+deg]

	plt.xticks([0, xx, len(lat)-1], x_labels)

	plt.xlabel(deg + 'Lat, ' + deg + 'Lon')

	heights = get_vert_bins()

	inds = [0, 5, 9, 13, 17, 21, 25]

	plt.yticks(inds, [str(heights[x]) for x in inds])

	plt.ylabel('km')

	plt.ylim([-1, 26])

	return
	
# ----------------------------------------------------------------------

def plot_details(plt, datestr):
	
	plt.title('CPR Reflectivity')		
	save_name = 'cpr_z_' + datestr + '.png'
	
	return save_name
	
# ----------------------------------------------------------------------	

# CloudSat vertical bin range is 239.829071045 meters
def get_vert_bins():
	
	# bin 104 = surface
	heights = (np.arange(-21, 104)*240)/1000.

	return heights[21:47]
	
