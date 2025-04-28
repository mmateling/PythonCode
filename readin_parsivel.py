# ----------------------------------------------------------------------------
#
#  save_parsivel_cases
#
# ----------------------------------------------------------------------------

import numpy as np
from glob import glob
import zipfile
from datetime import datetime
import matplotlib.pyplot as plt
from netCDF4 import Dataset

def do_werk():

	#caselist = get_caselist()

	#filelists = get_filelists(caselist)
	
	#g = 0
	
	for case in filelists:
		data = read_files(case)
		
		time, sensor_status, temp, wx4680, wx4677 = get_vars(data)
		
		#plot_wxcodes(caselist[g], wx4677, wx4680, time)
		
		wx_flag = create_wxcode_flag(wx4677)
		print(wx_flag.max())
			
		save_nc(caselist[g], wx_flag, time)
		
		g += 1
		
		
	return case, wx_flag

# ----------------------------------------------------------------------------

def get_caselist():

	caselist = ['20170210', \
		#'20170222', Missing
		#'20170223', Missing
		#'20170427', \Missing
		#'20170428', Missing
		'20171024', '20171025', '20171102', '20171117', \
		'20171118', '20171205', '20180111', '20180112', \
		#'20181107', Corrupted?\
		#'20181108', Corrupted?
		'20181227', '20181228', '20181229', '20190411', \
		'20190412', '20191121','20200404']
	
	return caselist

# ----------------------------------------------------------------------------
	
def get_filelists(caselist):

	indir = '/data/LakeEffect/APU/APU12/'
	
	filelist = []
	
	for case in caselist:
	
		print(case)
			
		short_filelist = glob(indir + 'apu12_' + case + '*.zip')
		short_filelist.sort()
		
		for files in short_filelist:
			with zipfile.ZipFile(files, 'r') as zip_ref:
				zip_ref.extractall(indir)
		
			
		filelist.append(short_filelist)
		
	return np.asarray(filelist)
	
# ----------------------------------------------------------------------------

def read_files(filelist):

	indir = '/data/LakeEffect/APU/APU12/'

	data = []

	for files in filelist:

		x = []
		
		for line in open(files[:-3]+'dat', 'r'):
			x.append(line.split(',')[:9])
			
		data.append(x)
		
	flat_data = [item for sublist in data for item in sublist]
	
	return flat_data
	
# ----------------------------------------------------------------------------

def get_vars(data):



	time = []
	sensor_status = []
	temp = []
	n = []		# number of detected particles
	r = []		# rain intensity (32bit, mm/hr)
	z = []  	# reflectivity factor (16bit, dBZ)
	vis = [] 	# MOR visibility in the precipitation (m)
	wx4680 = []
	wx4677 = []
	raw_data = []

	for j in range(len(data)):
		
		time.append(datetime.strptime(data[j][0].split(';')[0], \
			'%Y%m%d%H%M%S'))
		# 0 = everything ok
		# 1 = laser glass dirty, but measurements still possible
		# 2 = laser glass dirty, no further measurements possible
		# 3 = laser damanged
		sensor_status.append(np.int(data[j][1]))
		
		temp.append(np.float(data[j][2]))
		
		n.append(.......
		
		wx4680.append(np.int(data[j][7]))
		
		wx4677.append(np.int(data[j][8]))
		
	return time, sensor_status, temp, wx4680, wx4677

# ----------------------------------------------------------------------------
		
def plot_wxcodes(case, wx4677, wx4680, time):

	plt.figure(figsize=(15, 3))
		
	plt.plot(time, wx4680, 'o', label='WX4680', zorder = 0)
		
	print('-----------------------------------------')
	print('Case ' + case)
	print('WX4680')
	print(np.unique(wx4680))
		
	plt.plot(time, wx4677, 'ro', label='WX4677', zorder = 1)
		
	print('WX4677')
	print(np.unique(wx4677))
		
	plt.title(case)
	
	plt.xlim(datetime(2017, 10, 24, 11, 0), \
		datetime(2017, 10, 24, 12, 0))
	
	plt.ylim(50, 80)
		
	plt.legend(loc = 'lower right')
		
	plt.grid(zorder=2)
	#plt.savefig('IMAGES/wxcode_' + case + '.png')
	
	return
		
# ----------------------------------------------------------------------------

def create_wxcode_flag(wxcode):

	# If missing, hail, drizzle, ice pellets.... leave as 0.
	wx_flag = np.zeros(len(wxcode))
	
	for x in range(len(wx_flag)):
	
	#	if wxcode[x] == 51 or wxcode[x] == 53 or wxcode[x] == 58 or \
	#		wxcode[x] == 59 or wxcode[x] == 87 or \
	#		wxcode[x] == 88 or wxcode[x] == 89 or \
	#		wxcode[x] == 90 or wxcode[x] == 69:
	#		
	#		# NaN
	#		wx_flag[x] = np.nan
			
		if wxcode[x] == 61 or wxcode[x] == 63 or wxcode[x] == 65:
			
			# Rain
			wx_flag[x] = 1
			
		elif wxcode[x] == 71 or wxcode[x] == 73 or wxcode[x] == 75:
		
			# Snow
			wx_flag[x] = 2
			
		elif wxcode[x] == 69:
		
			# Mixed
			wx_flag[x] = 3

	return wx_flag

# ----------------------------------------------------------------------------
"""	
def save_nc(case, wx_flag_, time_):

     # Convert datetime object
	str_dates = np.array([str(v) for v in time_])
	
      # Create seconds-from-epoch datelist
	d1 = datetime(1970, 1, 1)
	epoch_dates = np.array([(dt - d1).total_seconds() for dt in time_])
	
      # Set up data to save
	outdir = '/data/LakeEffect/APU/APU12/Precipitation_Type/'

	filename = outdir + 'Case_' + case + '_parsivel.nc'
	
	f = Dataset(filename, 'w', format='NETCDF4')
	
	f.createDimension('time', len(time_))
	f.createDimension('nchar', len(str_dates[0]))
	
	wx_flag = f.createVariable('wx_flag', 'f8', 'time')
	datestr = f.createVariable('datestr', str_dates.dtype, 'time')
	sec_from_epoch = f.createVariable('sec_from_epoch', 'f8', 'time')
	
	wx_flag[:] = wx_flag_
	datestr[:] = str_dates
	sec_from_epoch[:] = epoch_dates
	
	f.description = 'This file contains a snow/rain flag from the parsivel in Marquette, '\
		+'MI. Case: ' + case + '. Created by Marian Mateling (mateling@wisc.edu).'\

	wx_flag.description = 'Precip Accumulation'
	wx_flag.units = '0 = NaN or No Precip; 1 = Rain; 2 = Snow; 3 = Mixed'

	datestr.description = 'Time'
	datestr.units = 'YYYY-mm-dd HH:MM:SS'
	
	sec_from_epoch.description = 'Seconds from Unix Epoch'
	sec_from_epoch.units = 'Seconds'
	
	f.close()
"""
