import cdsapi

import itertools, shutil, os, tempfile, datetime, copy

## EDIT HERE: adjust time range of daily file downloads.
start_day = datetime.datetime(2022,6,20).toordinal()
stop_day = datetime.datetime(2023,1,1).toordinal()

## EDIT HERE: set destination dir.
default_dst_dir = '/data/Reanalyses/ERA5/daily/'

## EDIT Here: the output filename format
## {0:s} is for the YMD string, {1:s} is for the data source (sfc or pl)
target_fmt = 'ERA5_{0:s}_{1:s}.nc'

##
## Remaining keywords should not be modified unless you want
## different data.
##

# kw applying to both surface and pressure-level
# note the lat/lon area box: North/West/South/East
rkw_base = {
    'product_type':'reanalysis',
    'format':'netcdf',
    'time':['{0:02d}:00'.format(t) for t in range(24)],
    'area':'90/-180/0/180',
    }

# add'l params, divided by pl and sfc
# PRESSURE LEVELS
plev_var_list = [
    'geopotential','relative_humidity','specific_humidity',
    'specific_rain_water_content','temperature','u_component_of_wind',
	'v_component_of_wind','vertical_velocity']
plev_rkw = {
    'pressure_level':['200','250','500','700','850','900','1000'],
    'variable':plev_var_list}
plev_datasource_name = 'reanalysis-era5-pressure-levels'

# SURFACE
single_var_list = [
    '10m_u_component_of_wind','10m_v_component_of_wind','2m_temperature',\
    'mean_sea_level_pressure','surface_pressure','total_column_rain_water',\
	'total_column_snow_water','total_column_supercooled_liquid_water',\
	'total_column_water','total_column_water_vapour','total_precipitation',\
	'vertical_integral_of_divergence_of_cloud_frozen_water_flux',\
	'vertical_integral_of_divergence_of_cloud_liquid_water_flux',\
	'vertical_integral_of_divergence_of_moisture_flux',\
	'vertical_integral_of_eastward_cloud_frozen_water_flux',\
	'vertical_integral_of_eastward_cloud_liquid_water_flux',\
	'vertical_integral_of_eastward_water_vapour_flux',\
	'vertical_integral_of_northward_cloud_frozen_water_flux',\
	'vertical_integral_of_northward_cloud_liquid_water_flux',\
	'vertical_integral_of_northward_water_vapour_flux','vertically_integrated_moisture_divergence']
single_var_rkw = {
    'variable':single_var_list}
single_var_datasource_name = 'reanalysis-era5-single-levels'


##############
# Do The Work. Note this is done in a tmp dir and then copied into a
# final destination dir.
#

# converts start/stop day into a list of string YMD
datestr_list = [datetime.datetime.fromordinal(s).strftime('%Y%m%d')
                for s in range(start_day, stop_day)]


def _download_helper(c, datasource_name, rkw, tgt_file, dst_dir):
    """helper to wrap the API retrieve call in a try/except, and also checks
    if the file already exists in the destination.
    """

    dst_file = os.path.join(dst_dir, tgt_file)
    if os.access(dst_file, os.F_OK):
        print('**** Skipping file: ', tgt_file, ' already exists ****')

    else:
        print('**** Downloading file: ', tgt_file, ' ****')

        try:
            c.retrieve(datasource_name, rkw, tgt_file)
        except AssertionError as theError:
            print('AssertionError occured at file: ')
            print(tgt_file)
            print(str(theError))
        else:
            shutil.move(tgt_file, dst_file)


def _date_rkw_helper(datestr):
    """splits out the YMD string (old method) into year, month, day
    dictionary key/values (new method)"""
    rkw = {'year': datestr[:4], 'month':datestr[4:6], 'day':datestr[6:]}
    return rkw


def run_download_loop(datestr_list, dst_dir):
    """ main function to run CDS download over a list of YMD strings.
    """

    tmp_dl_dir = tempfile.gettempdir()
    os.chdir(tmp_dl_dir)

    c = cdsapi.Client()

    print("Starting download loop for " + str(len(datestr_list)) + " ymds")

    for datestr in datestr_list:

        # splits out the YMD into individual KW inputs.
        date_rkw = _date_rkw_helper(datestr)

        rkw = copy.copy(rkw_base)
        rkw.update(plev_rkw)
        rkw.update(date_rkw)
        tgt_file = target_fmt.format(datestr, 'pl')
        _download_helper(c, plev_datasource_name, rkw, tgt_file, dst_dir)

        rkw = copy.copy(rkw_base)
        rkw.update(single_var_rkw)
        rkw.update(date_rkw)
        tgt_file = target_fmt.format(datestr, 'sfc')
        _download_helper(c, single_var_datasource_name, rkw, tgt_file, dst_dir)



if __name__ == "__main__":
    
    run_download_loop(datestr_list, default_dst_dir)
