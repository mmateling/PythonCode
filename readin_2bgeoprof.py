# ----------------------------------------------------------------------
#
#  readin_2bgeoprof
#
# ----------------------------------------------------------------------

import numpy as np
from netCDF4 import Dataset
from glob import glob
from datetime import datetime
import pyhdf.SD
import pyhdf.HDF
import read_var_eos as eos
import matplotlib.pyplot as plt

"""
Karissa's email 2/10/22

ynn case (September 8, 2008)
'2008252014301_12578_CS_2C-SNOW-PROFILE_GRANULE_P1_R05_E02_F00.h5'
I graphed from (-60.08, -18.05) to (-71.44, -28.55)

virga case with (August 28, 2008)
 '2008241065806_12421_CS_2C-SNOW-PROFILE_GRANULE_P1_R05_E02_F00.h5'
I graphed from (-79.47, -134.66) to (-81.79, -170.38)

virga case (August 12, 2008)
 '2008225065756_12188_CS_2C-SNOW-PROFILE_GRANULE_P1_R05_E02_F00.h5'
I graphed from (-74.89, -115.69) to (-81.79, -170.40)
"""

# ----------------------------------------------------------------------

def do_work(case_num):

	filename = get_case(case_num)

	z, lat, lon, clutter, sfc_bin = readin_file(filename)

	inds = index_data(lat, lon, case_num)

	plot_z(z[inds], lat[inds], lon[inds], sfc_bin[inds], case_num)

def get_case(case_num):
		
	indir = '/thermal/data/CloudSat/2b-geoprof/P1_R05/'

	if case_num == '1':
		filename = indir + \
		'2008252014301_12578_CS_2B-GEOPROF_GRANULE_P1_R05_E02_F00.hdf'
	elif case_num == '2':
		filename = indir + \
		'2008241065806_12421_CS_2B-GEOPROF_GRANULE_P1_R05_E02_F00.hdf'
	elif case_num == '3':
		filename = indir + \
		'2008225065756_12188_CS_2B-GEOPROF_GRANULE_P1_R05_E02_F00.hdf'

	return filename

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
			
	return z, lats, lons, clutters, height_bins
	
def index_data(lat, lon, case_num):

	if case_num == '1':
		# latlon = lat max, lon max, lat min, lon min
		latlon = [-60.08, -18.05, -71.44, -28.55]
	elif case_num == '2':
		latlon = [-79.47, -134.66, -81.79, -170.38]
	elif case_num == '3':
		latlon = [-74.89, -115.69, -81.79, -170.40]

	inds = np.where(np.logical_and(np.logical_and(lat >= latlon[2], \
	lat < latlon[0]), np.logical_and(lon >= latlon[3], lon < latlon[1])))[0]
	
	return inds

def plot_z(z, lat, lon, sfc_bin, case_num):
	
	# Flip the value of the surface bin; bin 104 is surface, not 125!
	surface_line = np.asarray([int(105 - x) for x in sfc_bin])

	plt.figure(figsize=(16,8))

	cmap = plt.get_cmap('gist_ncar')	
	cmap.set_bad(color='white')	# For masked values (< -25 dbz)
	cmap.set_over(color='darkgrey')	# For values "over" colorbar range

	z = np.ma.masked_less(z, -25)

	cs = plt.pcolormesh(np.flipud(z.T)[21:47], cmap = cmap, \
		vmin=-25, vmax=20)

	plot_xy_labels(lat, lon, plt)
	
	plt.plot(surface_line, color='k', linewidth=2)

	cb = plt.colorbar(cs)

	cb.set_label('dBZe')

	cb.set_ticks(np.arange(-25, 25, 5))

	save_name = plot_details(case_num, plt)

	plt.show()

	plt.savefig(save_name, bbox_inches='tight')

def plot_xy_labels(lat, lon, plt):

	deg = u"\N{DEGREE SIGN}"

	xx = len(lat)/2

	x_labels = [str(lat[0])[:6]+deg+', '+str(lon[0])[:6]+deg, \
	str(lat[xx])[:6]+deg+', '+str(lon[xx])[:6]+deg, \
	str(lat[-1])[:6]+deg+', '+str(lon[-1])[:6]+deg]

	plt.xticks([0, xx, len(lat)-1], x_labels)

	plt.xlabel(deg + 'Lat, ' + deg + 'Lon')

	heights = get_vert_bins()

	#plt.yticks([0, 25, 50], [str(heights[0]), \
	#	str(heights[25]), str(heights[50])])

	inds = [0, 5, 9, 13, 17, 21, 25]

	plt.yticks(inds, [str(heights[x]) for x in inds])

	plt.ylabel('Km')

	plt.ylim([-1, 26])

	return

def plot_details(case_num, plt):
	if case_num == '1':
		plt.title('Sep 8 2008 CPR Reflectivity')		
		save_name = 'cpr_z_sep08_2008_v2.png'
	if case_num == '2':
		plt.title('Aug 28 2008 CPR Reflectivity')		
		save_name = 'cpr_z_aug28_2008_v2.png'
	if case_num == '3':
		plt.title('Aug 12 2008 CPR Reflectivity')		
		save_name = 'cpr_z_aug12_2008_v2.png'

	return save_name

# CloudSat vertical bin range is 239.829071045 meters...
def get_vert_bins():
	
	# bin 104 = surface
	heights = (np.arange(-21, 104)*240)/1000.

	#return heights[21:72]
	return heights[21:47]
	
