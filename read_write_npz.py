# ------------------------------------------------------------------------------
#
#  read_write_npz
#
#   Author: Marian Mateling (mateling@wisc.edu)
#
#   Last updated: Apr 15 2025
#
# ------------------------------------------------------------------------------

import numpy as np
import sys
import os

# ------------------------------------------------------------------------------

"""

Example template for reading and writing data to npz files.

Input: year (int), month (int)

To automatically run this from command line,

  > python read_write_npz.py (_year_) (_month_)

To run this while in python,

  > read_monthly_npz_files(year, month)

"""

def read_monthly_npz_file(year, month):

    # npz filename
    
    datestr = str(year) + ('0'+str(month))[-2:]
    filename = 'npz_files/filename_' + datestr+'.npz'
    



  # If the file already exists...

    if os.path.isfile(filename):

        cloud_type, sfc_type, lat, lon, time = read_files(datestr)
	
        return cloud_type, sfc_type, lat, lon, time




  # If the npz file does *not* already exist, create it: 

    # *****************************************************
    # ((Insert your CODE to read data from original files & 
    #     turn into arrays or lists))
    # *****************************************************

    # Save arrays or lists to npz
    
    # npz doesn't like datetime objects, so convert to string (if needed)
    time_str = [str(x) for x in time]

    # MOST IMPORTANT LINE: SAVE DATA TO NPZ 
    #    ("new npz file var name" = "variable to assign")
    
    np.savez(filename, cloud_type = cloud_type, sfc_type = sfc_flag, \
        time = time, lat = lat, lon = lon)


   
    return cloud_type, sfc_flag, lat, lon, time_str
    
# ------------------------------------------------------------------------------


def read_files(datestr):

    cloud_type = []; sfc_flag = []; lat = []; lon = []; time = []
    
    filename = 'npz_files/filename_' + datestr+'.npz'

    data = np.load(filename)

    cloud_type = data['cloud_type'][:]

    sfc_type = data['sfc_flag'][:]

    time = data['time'][:]

    lat = data['lat'][:]

    lon = data['lon'][:]
    
    data.close()

    return cloud_type, sfc_type, lat, lon, time

# ------------------------------------------------------------------------------

if __name__=='__main__':

    year = int(sys.argv[1])
    month = int(sys.argv[2])

    read_monthly_npz_files(year, month)
