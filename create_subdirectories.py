# ------------------------------------------------------------------------ #
#
#	create_subdirectories
#
# ------------------------------------------------------------------------ #

import os
import numpy as np
import shutil
from glob import glob
from datetime import datetime, timedelta
	
	
def do_work(year, var):

	var_direc = get_direc(year, var)

	julian_days = np.arange(1, 367)
	
	for jd in julian_days:
	
		file_str = str(year) + ('00'+str(jd))[-3:]
		
			# YEAR Directory
		try:
			files = glob(var_direc + file_str + '*.hdf')

			new_subdirec = var_direc + julian_str + '/'

			os.mkdir(new_subdirec)
			
			for f in files: shutil.move(f,new_subdirec)
			
			
			return
		except:
			print('Files dont exist')


		
	
	
def get_direc(year, var):	

	year_str = str(year)

	indir = '/ships19/cloud/archive/extern/cloudsat/'
	if var == 'snow': var_direc = '2C-SNOW-PROFILE.P1_R05/'+year_str+'/'
	elif var == 'cloud': var_direc = '2B-CLDCLASS-LIDAR.P1_R05/'+year_str+'/'

	return indir + var_direc
