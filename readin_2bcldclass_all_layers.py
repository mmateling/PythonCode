# ----------------------------------------------------------------------
#
#  readin_2bcldclass_all_layers
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

def readin_file(year, month, day, save_flag = 'on'):

	date_str = get_date_str(year, month, day)

	indir = '/ships19/cloud/archive/extern/cloudsat/'+\
		'2B-CLDCLASS-LIDAR.P1_R05/'+date_str[:4]+'/'+\
		date_str[4:]+'/'
        
	filelist = glob(indir + date_str + '*.hdf')
	filelist.sort()

	cld_list = []; phase_list = []
	cth_list = []; cbh_list = []; sfc_flag_list = []
	lat_list = []; lon_list = []; time_list = []
	
	for file_ in filelist:
	
		f_SD_ptr = pyhdf.SD.SD(file_, pyhdf.SD.SDC.READ)
		f_VD_ptr = pyhdf.HDF.HDF(file_, pyhdf.HDF.HC.READ)
		
		#f = Dataset(file_, 'r')

		time = eos.get_profile_times(f_VD_ptr)
		
		cloud_type = eos.get_2D_var(f_SD_ptr, f_VD_ptr, 'CloudLayerType')
		
		
		"""
		
		--> Uncomment and use this code for only the top cloud in the
		     layer. Also, change the above 'cloud_type' variable to 
		     be 'cloud_type_0'
		
		# Save highest cloud in the column, index = -1. 
		#  If no clouds, set to 0.0
		
		#cloud_type = np.zeros(len(cloud_type_0))
		
		for v in range(len(cloud_type_0)):
			try:
			   positive_clouds = [y for y in cloud_type_0[v] if y > 0]
			   cloud_type[v] = np.copy(positive_clouds[-1])
			except:
			   cloud_type[v] = 0.0
		"""
			
		cloud_phase = eos.get_2D_var(f_SD_ptr, f_VD_ptr, 'CloudPhase')
		cloud_top = eos.get_2D_var(f_SD_ptr, f_VD_ptr, 'CloudLayerTop')
		cloud_base = eos.get_2D_var(f_SD_ptr, f_VD_ptr, 'CloudLayerBase')

		land_sea_flag = eos.get_1D_var(f_VD_ptr, \
			'Navigation_land_sea_flag')

		lat = eos.get_1D_var(f_VD_ptr, 'Latitude')
		lon = eos.get_1D_var(f_VD_ptr, 'Longitude')
		
		f_VD_ptr.close()
		f_SD_ptr.end()
		
	     # Adjust shape of surface flag and lat/lon variables 
		
		sfc_flag = land_sea_flag.T[0]
				
		lats = lat.T[0]
		lons = lon.T[0]		

		# Only keep data that falls in the Great Lakes region.

		lat_min = 41; lat_max = 49
		lon_min = -92; lon_max = -75
	
		inds = (lats >= lat_min) & (lats < lat_max) & \
			(lons >= lon_min) & (lons < lon_max)

		if len(np.where(inds == True)[0]) > 0:

			
			# Will this work even with a second dimension? 
			cld_list.append(np.array(cloud_type[inds]))
			
			phase_list.append(np.array(cloud_phase[inds]))
			cth_list.append(np.array(cloud_top[inds]))
			cbh_list.append(np.array(cloud_base[inds]))
			sfc_flag_list.append(np.array(sfc_flag[inds]))
			lat_list.append(lats[inds])
			lon_list.append(lons[inds])
			time_list.append(time[inds])
           
	save_flag = 'off'   
	
	if save_flag == 'off':
	
	    # Return lists for plotting vertical profiles
	
		return cld_list, phase_list, cth_list, \
		cbh_list, sfc_flag_list, lat_list, lon_list, time_list            
	else:
	
	    # Return flattened lists for saving data:
	    
		return flatten(cld_list), \
		flatten(phase_list), flatten(cth_list), flatten(cbh_list), \
		flatten(sfc_flag_list), flatten(lat_list), flatten(lon_list), \
		flatten(time_list)

# ------------------------------------------------------------------------------		
		
def get_date_str(year, month, day):

	dt = datetime(year, month, day)
	
	tt = dt.timetuple()
	
	julian_day = tt.tm_yday
			
	date_str = str(year) + ('00' + str(julian_day))[-3:]
	
	return date_str
	
# ------------------------------------------------------------------------------

def flatten(xss):
    return [x for xs in xss for x in xs]
