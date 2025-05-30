# ----------------------------------------------------------------------
#
#  readin_2bcldclass_match_2csnow
#
#   Author: Marian Mateling (mateling@wisc.edu)
#
# ----------------------------------------------------------------------

# Depends on 2C-SNOW input for matching data in time/space

import numpy as np
from netCDF4 import Dataset
from glob import glob
from datetime import datetime
import pyhdf.SD
import pyhdf.HDF

# Script written and provided by Norm Wood (norman.wood@ssec.wisc.edu)
import read_var_eos as eos

# ----------------------------------------------------------------------

def readin_file(year, month, day, snow_2c, opass, region):

	date_str = get_date_str(year, month, day)
	indir = '/ships19/cloud/archive/extern/cloudsat/'+\
		'2B-CLDCLASS-LIDAR.P1_R05/'+date_str[:4]+'/'+\
		date_str[4:]+'/'
        
	filelist = glob(indir + date_str + '*.hdf')
	filelist.sort()

	cth_list = []; cld_list = []; flag = []
	lat_list = []; lon_list = []; time_list = []
	
	# For looping through 2c filelist, which is shorter than 2b
	j = 0
	
	for g in range(len(filelist)):
	
		if filelist[g].split('/')[-1].split('_')[0] == opass[j]:
					
			flag.append('match')
		
			f_SD_ptr = pyhdf.SD.SD(filelist[g], pyhdf.SD.SDC.READ)
			f_VD_ptr = pyhdf.HDF.HDF(filelist[g], pyhdf.HDF.HC.READ)

			time = eos.get_profile_times(f_VD_ptr)
		
			cloud_top = eos.get_2D_var(f_SD_ptr, \
				f_VD_ptr, 'CloudLayerTop')
			
			cloud_type = eos.get_2D_var(f_SD_ptr, \
				f_VD_ptr, 'CloudLayerType')
					
			lat = eos.get_1D_var(f_VD_ptr, 'Latitude')
			lon = eos.get_1D_var(f_VD_ptr, 'Longitude')
			f_VD_ptr.close()
			f_SD_ptr.end()
					
			lats = lat.T[0]
			lons = lon.T[0]		

			# Only append data that falls inside the basin.
			if region == 'atlantic':
				# Atlantic: Lat 45 to 82, Lon -76 to 40
				lat_min = 45; lat_max = 82
				lon_min = -76; lon_max = 40
			elif region == 'greatlakes':
				lat_min = 40; lat_max = 50
				lon_min = -95; lon_max = -75

			inds = np.where(np.logical_and(np.logical_and(lats >= lat_min, \
			lats < lat_max), np.logical_and(lons >= lon_min, lons < lon_max)))[0]

			if len(inds) > 0:
				cth_list.append(cloud_top[inds])
				cld_list.append(cloud_type[inds])
				lat_list.append(lats[inds])
				lon_list.append(lons[inds])
			
			j += 1
		if j == len(opass): break
		

    # Mask cloud data where not snowing (snow2c == 0):

	#new_cth, new_cld = mask_nonzero_snow(cth_list, \
		#cld_list, snow_2c, flag)
		
	return cth_list, cld_list, lat_list, lon_list

def mask_nonzero_snow(cth, cld, snow, flag):

	new_cth = []; new_cld = []
	count = 0

	# For each overpass
	for i in range(len(cth)):
	
		sub_cth_list = []; sub_cld_list = []
		
		# For each pixel in the overpass
		for j in range(len(cth[i])):
	
			# If the file names b/w 2c and 2b match
			if snow[i][j] > 0 and flag[i] == 'match':
			
				# For every level in vertical profile (10 long)
				for k in range(len(cth[i][j])):
					if cth[i][j][k] > 0:
						sub_cth_list = np.ma.append(sub_cth_list,\
							cth[i][j][k])
						sub_cld_list = np.ma.append(sub_cld_list,\
							cld[i][j][k])
						break
					else:
						count += 1
				if count == 10:
					#print('No CTH for snow here')
					sub_cth_list = np.ma.append(sub_cth_list, -999)
					sub_cld_list = np.ma.append(sub_cld_list, -999)
				
				count = 0
						
						
			else:
				sub_cth_list = np.ma.append(sub_cth_list, -999)
				sub_cld_list = np.ma.append(sub_cld_list, -999)
				
		#print(len(sub_cth_list))		
		new_cth.append(np.ma.masked_less(sub_cth_list, 0))		
		new_cld.append(np.ma.masked_less(sub_cld_list, 0))		
	
	return new_cth, new_cld
	

# ------------------------------------------------------------------------------		
		
def get_date_str(year, month, day):

	dt = datetime(year, month, day)
	
	tt = dt.timetuple()
	
	julian_day = tt.tm_yday
			
	date_str = str(year) + ('00' + str(julian_day))[-3:]
	
	return date_str
