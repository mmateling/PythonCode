# -------------------------------------------------------------------------------------------
#
# read_write_netCDF
#
#	Example of how to read and write netCDFs using the netCDF4 package in python.
#	Used the ARM dataset from Barrow, AK (previously /boltzmann, RIP)
#	Helpful resource: http://pyhogs.github.io/intro_netcdf4.html
#
# Author: Marian Mateling (mateling@wisc.edu)
#
# Last updated: Apr 14 2025
#
# -------------------------------------------------------------------------------------------

import numpy as np
from netCDF4 import Dataset

# -------------------------------------------------------------------------------------------

def do_work():

	datestring = '20141010'

	temp, swc, snow, time, height = readin_netcdf(datestring)

	write_netcdf(temp, swc, snow, time, height, datestring)

# -------------------------------------------------------------------------------------------

def readin_netcdf(datestring):

	# No longer available here; change to your data product
	indir = '/boltzmann/data6/norm/ASR/Snow_retrieval_product_testing/BRW/Product/2014/'

	fname = indir + 'nsa1snowprofC1.c1.' + datestring + '.000000.cdf'

	# 'f' is my netCDF object, or 'root group'
	f = Dataset(fname, 'r')

	temp = f['T'][:]

	swc = f['swc'][:]

	snow = f['srate_sfc'][:]

	time = f['time'][:]

	height = f['height'][:]

	f.close()

	return temp, swc, snow, time, height

# -------------------------------------------------------------------------------------------

def write_netcdf(temp, swc, snow, time, height, datestring):

	new_netcdf = 'filename-for-data_' + datestring + '.nc'

	# Create root group
	f = Dataset(new_netcdf, 'w', format = 'NETCDF4')

	# Create dimensions (used below for creating variables)
	f.createDimension('time', len(time))		# Time dimension
	f.createDimension('height', len(height))	# Height dimension
	
	# Time variable may not be 'ints' or 'floats', so convert it to a string
	# --> for original dataset ARM used here, time variable *is* either ints or floats
	str_dates = np.array([str(v) for v in time])
	timestep = f.createVariable('Time', str_dates.dtype, 'time')

	# Create variables: f.createVariable(new variable name, data type, dimensions)
	#    If dimensions are more than 1-D: (dimension 1, dimension 2)
	temperature = f.createVariable('Temperature', 'f4', ('time', 'height'))
	snow_wc = f.createVariable('SnowWaterContent', 'f4', ('time', 'height'))
	snow_rate = f.createVariable('SnowfallRate', 'f4', 'time')
	timestep = f.createVariable('Timestep', 'f8', 'time')
	altitudes = f.createVariable('Height', 'f4', 'height')

	# Assign data passed to function to the variables we just created.
	temperature[:] = temp
	snow_wc[:] = swc
	snow_rate[:] = snow
	timestep[:] = time
	altitudes[:] = height

	# Add attributes for root group and/or even individual variables.
	
	# Root group
	f.description = 'My newly created netCDF'

	# Individual variables
	temperature.description = 'Temperature data'
	temperature.units = 'Degrees Celsius'
	temperature..missing_value = -9999
	
	f.close()
