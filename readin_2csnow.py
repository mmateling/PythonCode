# ------------------------------------------------------------------------------
#
#  readin_2csnow
#
#  Author: Marian Mateling (mateling@wisc.edu)
#
# ------------------------------------------------------------------------------

import numpy as np
from netCDF4 import Dataset
from glob import glob
from datetime import datetime
import pyhdf.SD
import pyhdf.HDF

# Script written and provided by Norm Wood (norman.wood@ssec.wisc.edu)
import read_var_eos as eos

# ------------------------------------------------------------------------------

def readin_file(year, month, day):


	date_str = get_date_str(year, month, day)

	indir = '/data/CLOUDSAT/2c-snow-profile/'

	filelist = glob(indir + date_str + '*.hdf')
	
	snow_list = []; lat_list = []; lon_list = []; time_list = []
	overpass_name = []; conf_list = []
	
	for file_ in filelist:
	
		f_SD_ptr = pyhdf.SD.SD(file_, pyhdf.SD.SDC.READ)
		f_VD_ptr = pyhdf.HDF.HDF(file_, pyhdf.HDF.HC.READ)
		
		time = eos.get_profile_times(f_VD_ptr)
		snow = eos.get_1D_var(f_VD_ptr, 'snowfall_rate_sfc')
		conf = eos.get_1D_var(f_VD_ptr, 'snowfall_rate_sfc_confidence')
		lat = eos.get_1D_var(f_VD_ptr, 'Latitude')
		lon = eos.get_1D_var(f_VD_ptr, 'Longitude')
		f_VD_ptr.close()
		f_SD_ptr.end()

		lats = lat.T[0]
		lons = lon.T[0]		

		# Only append data that falls inside the basin.
		# Atlantic: Lat 45 to 82, Lon -76 to 40
		lat_min = 45; lat_max = 82
		lon_min = -76; lon_max = 40

		inds = np.where(np.logical_and(np.logical_and(lats >= lat_min, \
		lats < lat_max), np.logical_and(lons >= lon_min, lons < lon_max)))[0]
				
		if len(inds) > 0:
			# Fix the shape of this, because it is shape=(len(), 1)
			reshape_snow = np.reshape(snow[inds], len(snow[inds]))
			reshape_conf = np.reshape(conf[inds], len(conf[inds]))

			# Only keep data when confidence flag >= 3			
			snow_list.append(np.ma.masked_where(reshape_conf < 3, \
				reshape_snow))
			conf_list.append(np.ma.masked_where(reshape_conf < 3, \
				reshape_conf))
				
			lat_list.append(lats[inds])
			lon_list.append(lons[inds])
			time_list.append(time[inds])

			overpass_name.append(file_.split('/')[4].split('_')[0])
		
	return snow_list, lat_list, lon_list, time_list, overpass_name, conf_list
		
# ------------------------------------------------------------------------------		
		
def get_date_str(year, month, day):

	dt = datetime(year, month, day)
	
	tt = dt.timetuple()
	
	julian_day = tt.tm_yday
			
	date_str = str(year) + ('00' + str(julian_day))[-3:]
	
	return date_str
