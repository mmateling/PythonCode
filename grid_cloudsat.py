# --------------------------------------------------------------------------------
#
#  grid_cloudsat
#
# --------------------------------------------------------------------------------

import numpy as np
import sys
from datetime import datetime, timedelta

import readin_2csnow as cloudsat
import readin_2bcldclass as cldclass

# ---------------------------------------------------------------------------------------------

def get_monthly_cloudsat(year, month):

	print('Getting CloudSat')

	num_days = get_num_days(year, month)

	all_snow = []; all_lats = []; all_lons = []; all_times = []
	all_cth = []; all_conf = []

	for days in range(1, num_days+1):
		print(days)
	
		snow, lat, lon, time, opass_name, conf = \
			cloudsat.readin_file(year, month, days)
			
		cth, clouds, lat_2b, lon_2b = cldclass.readin_file(year, \
			month, days, snow, opass_name)	
			
		all_snow.append(snow)
		all_conf.append(conf)
		all_cth.append(cth)
		all_lats.append(lat)
		all_lons.append(lon)
		all_times.append(time)

	return all_snow, all_cth, all_lats, all_lons, all_times, all_conf

# ---------------------------------------------------------------------------------------------

def grid_cloudsat(snow, cth, lat, lon, time, datetimes):

	print('Gridding CloudSat')

	# Flatten list of lists (collapses first 2 dimensions)
	flat_snow = [item for sublist in snow for item in sublist]
	flat_cth = [item for sublist in cth for item in sublist]
	flat_lat = [item for sublist in lat for item in sublist]
	flat_lon = [item for sublist in lon for item in sublist]
	flat_time = [item for sublist in time for item in sublist]
		
	# 1x2 DEGREES
	step_lat = 1
	step_lon = 2
			
	# Atlantic basin: 76 W to 40 E, 45 N to 82 N
	gridded_lats = np.arange(45, 82+step_lat, step_lat)
	gridded_lons = np.arange(-76, 40+step_lon, step_lon)
	
	# for Atlantic basin, this is 37x58
	n_lats = len(gridded_lats) - 1
	n_lons = len(gridded_lons) - 1
		
	# lat x lon
	gridded_snow = np.ma.zeros([len(flat_snow),n_lats,n_lons]) -999.
	gridded_cth = np.ma.zeros([len(flat_snow),n_lats,n_lons]) -999.
	gridded_time = np.zeros([len(flat_snow),n_lats,n_lons]) -999.
	grid_counts = np.zeros([len(flat_snow),n_lats,n_lons])
	grid_gr0_counts = np.zeros([len(flat_snow),n_lats,n_lons])
	grid_gr01_counts = np.zeros([len(flat_snow),n_lats,n_lons])
	grid_gr5_counts = np.zeros([len(flat_snow),n_lats,n_lons])
	
	# Using this to help figure out how many pixels per grid box...
	#hist_this = []
	
	for i in range(len(gridded_lats)-1):
		for j in range(len(gridded_lons)-1):
			for k in range(len(flat_snow)):
				
				# Creates a mask for all lats/lons inside of grid box
				
				lat_mask = np.logical_and(flat_lat[k] >= gridded_lats[i], \
					flat_lat[k] < gridded_lats[i+1])
				
				lon_mask = np.logical_and(flat_lon[k] >= gridded_lons[j], \
					flat_lon[k] < gridded_lons[j+1])
				
				inds = np.where(np.logical_and(lat_mask, lon_mask))[0]
		
				# If inds is a valid array, then there are 
				#	CloudSat obs in grid box 
				
				if len(inds) > 0:
				
					gr_eq_0_snow = np.ma.masked_less(flat_snow[k][inds], 0)
					gr0_cth = np.ma.masked_less_equal(flat_cth[k][inds], 0)
										
					# Absolute snowfall mean: mean includes 0 mm/hr values
					gridded_snow[k][i][j] = np.ma.mean(gr_eq_0_snow)
					
					gridded_cth[k][i][j] = np.ma.mean(gr0_cth)
					
					grid_counts[k][i][j] = np.ma.count(flat_snow[k][inds])
					
					grid_gr0_counts[k][i][j] = \
						np.ma.count(np.ma.where(flat_snow[k][inds]>0))
					grid_gr01_counts[k][i][j] = \
						np.ma.count(np.ma.where(flat_snow[k][inds]>=0.01))
					grid_gr5_counts[k][i][j] = \
						np.ma.count(np.ma.where(flat_snow[k][inds]>=0.5))
				
					# Grab the mid-point in time for all obs in the grid box
					
					start_time = min(flat_time[k][inds])
					end_time = max(flat_time[k][inds])
					
					midtime = start_time + (end_time - start_time) /2
					
					gridded_time[k][i][j] = \
						int(datetime.strftime(find_nearest(datetimes, \
						midtime), '%Y%m%d%H%M'))	
					
						
	return np.ma.masked_invalid(np.ma.masked_less(gridded_snow, 0)), \
		np.ma.masked_invalid(np.ma.masked_less(gridded_cth, 0)), \
		gridded_time, gridded_lats[:-1], gridded_lons[:-1], \
		grid_counts, grid_gr0_counts, grid_gr01_counts, grid_gr5_counts

# ---------------------------------------------------------------------------------------------
	
def find_nearest(array, value):

	array = np.asarray(array)
	idx = (np.abs(array - value)).argmin()

	return array[idx]

# ---------------------------------------------------------------------------------------------

def get_num_days(year, month):

	num_days = 31
	if month == 2 and year == 2008:
		num_days = 29
	elif month == 2:
		num_days = 28
	elif month == 4 or month == 6 or month == 9 \
		or month == 11:
		num_days = 30
		
	return num_days
