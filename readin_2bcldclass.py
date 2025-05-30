# ----------------------------------------------------------------------
#
#  readin_2bcldclass
#
#   Author: Marian Mateling (mateling@wisc.edu)
#
# ----------------------------------------------------------------------

import numpy as np
from netCDF4 import Dataset
from glob import glob
from datetime import datetime
import pyhdf.SD
import pyhdf.HDF

# Script written and provided by Norm Wood (norman.wood@ssec.wisc.edu)
import read_var_eos as eos

# ----------------------------------------------------------------------

def readin_file(year, month, day, region):

	date_str = get_date_str(year, month, day)

	indir = '/ships22/cloud/archive/extern/cloudsat/'+\
		'2B-CLDCLASS-LIDAR.P1_R05/'+date_str[:4]+'/'+\
		date_str[4:]+'/'
        
	filelist = glob(indir + date_str + '*.hdf')
	filelist.sort()

	cld_list = []; sfc_flag_list = []
	lat_list = []; lon_list = []; time_list = []
	
	for file_ in filelist:
	
		f_SD_ptr = pyhdf.SD.SD(file_, pyhdf.SD.SDC.READ)
		f_VD_ptr = pyhdf.HDF.HDF(file_, pyhdf.HDF.HC.READ)
		
		time = eos.get_profile_times(f_VD_ptr)
		
		cloud_type = eos.get_2D_var(f_SD_ptr, f_VD_ptr, 'CloudLayerType')
		
		#cloud_type = np.zeros(len(cloud_type_0))

		# Save highest cloud in the column, index = -1. 
		#  If no clouds, set to 0.0
		
		"""
		IF ONLY USING/SAVING THE HIGHEST CLOUD IN THE LAYER, ...
		
		for v in range(len(cloud_type_0)):
			try:
			   positive_clouds = [y for y in cloud_type_0[v] if y > 0]
			   cloud_type[v] = np.copy(positive_clouds[-1])
			except:
			   cloud_type[v] = 0.0
		"""

		land_sea_flag = eos.get_1D_var(f_VD_ptr, \
			'Navigation_land_sea_flag')

		lat = eos.get_1D_var(f_VD_ptr, 'Latitude')
		lon = eos.get_1D_var(f_VD_ptr, 'Longitude')
		
		f_VD_ptr.close()
		f_SD_ptr.end()
		
		sfc_flag = land_sea_flag.T[0]
				
		lats = lat.T[0]
		lons = lon.T[0]		

		# Only append data that falls inside the region.

		if region == 'atlantic':
			# Atlantic: Lat 45 to 82, Lon -76 to 40
			lat_min = 45; lat_max = 82
			lon_min = -76; lon_max = 40
		elif region == 'greatlakes':
			lat_min = 41; lat_max = 49
			lon_min = -92; lon_max = -75
	
			# Larger window
			#lat_min = 40; lat_max = 50
			#lon_min = -95; lon_max = -75

		inds = np.where(np.logical_and(np.logical_and(lats >= lat_min, \
		lats < lat_max), np.logical_and(lons >= lon_min, lons < lon_max)))[0]

		if len(inds) > 0:
			cld_list.append(np.array(cloud_type[inds]))
			sfc_flag_list.append(np.array(sfc_flag[inds]))
			lat_list.append(lats[inds])
			lon_list.append(lons[inds])
			time_list.append(time[inds])
                    
	# Return irregularly-shaped lists:
	#return cld_list, sfc_flag_list, lat_list, lon_list, time_list

	# Return flattened lists for saving data:
	return [item for sublist in cld_list for item in sublist], \
	[item for sublist in sfc_flag_list for item in sublist], \
	[item for sublist in lat_list for item in sublist], \
	[item for sublist in lon_list for item in sublist], \
	[item for sublist in time_list for item in sublist]

# ------------------------------------------------------------------------------		
		
def get_date_str(year, month, day):

	dt = datetime(year, month, day)
	
	tt = dt.timetuple()
	
	julian_day = tt.tm_yday
			
	date_str = str(year) + ('00' + str(julian_day))[-3:]
	
	return date_str
