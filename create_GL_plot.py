#----------------------------------------------------------------
#
#  create_mqt_plot
#  Author: Marian Mateling (mateling@wisc.edu)
#
# ----------------------------------------------------------------
"""
  How to use:

     # plot pops up on screen: 'on' or 'off'
     ax, plt = setup_plot('on')

     cs = ax.pcolormesh(lons, lats, plot_data, \
       zorder = 12, transform = ccrs.PlateCarree(), \
       cmap = 'plasma', vmin = 0, vmax = 3000)

     cb = plt.colorbar(cs, ax = ax)
"""

import numpy as np
import matplotlib as matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from cartopy.mpl.ticker import (LongitudeFormatter,LatitudeFormatter,LatitudeLocator)
import cartopy.crs as ccrs		# For map projections
import cartopy.feature as cfeature	# For putting features on map
from matplotlib.cm import get_cmap	# For choosing color bar 
import matplotlib.colors as colors


# on_off_flag = 'on' or 'off'
def setup_plot(on_off_flag='on'):

	if on_off_flag == 'off':
		plt.ioff()
	elif on_off_flag == 'on':
		plt.show()

	fig = plt.figure(figsize=(8,6))
	
	mid_lat = 45
	mid_lon = -85

	# Project data/coordinates to this:
	proj = ccrs.Orthographic(central_longitude = mid_lon, \
		central_latitude = mid_lat)	
		
	# Original projection/coordinates for data and gridlines:
	platecar = ccrs.PlateCarree()
		
	states_provinces = cfeature.NaturalEarthFeature(
       		category = 'cultural',
       		name = 'admin_1_states_provinces_lines',
       		scale = '110m',
       		facecolor = 'none',
		edgecolor = 'gray')
		
	lakes_high_res = cfeature.NaturalEarthFeature(
		category = 'physical',
		name = 'lakes',
		scale = '50m',
		facecolor = 'none',
		edgecolor = 'black')
		
	land_high_res = cfeature.NaturalEarthFeature(
		category='physical',
		name='land',
		scale='50m', 
		facecolor='none',
		edgecolor='black')
		
	borders = cfeature.BORDERS
	
	#coastline = cfeature.COASTLINE	

     # Set boundaries for the map (not global)

	corners = [-95, -75, 38, 52] #x0, x1, y0, y1

    # Set up plot details
     # Set the projection for drawing
	ax = plt.axes(projection = proj)
		
	ax.set_extent(corners, crs=platecar)
		
	ax.add_feature(land_high_res, zorder=1)
	
	ax.add_feature(states_provinces, zorder = 2)	
	
	ax.add_feature(lakes_high_res, zorder = 3)
	
	ax.add_feature(cfeature.BORDERS, zorder = 4)
	
	# Works for cartopy 0.18 
	#ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True)
	
     # --> Gridlines
	gl = ax.gridlines(crs=platecar, draw_labels=False, \
		zorder=5, color = 'gray', linestyle = '--', \
		alpha = 0.9, x_inline=False, y_inline=False)
	
	gl.xlocator = mticker.FixedLocator([-95,-90,-85,-80,-75])
	gl.ylocator = mticker.FixedLocator([40, 45, 50])	
	
	gl.xlines = True
	gl.ylines = True

     # --> Labels
	gl = ax.gridlines(crs=platecar, draw_labels=True, \
		zorder=6, x_inline=False, y_inline=False)
	
	gl.ylocator = mticker.FixedLocator([40, 45, 50])
	gl.xlocator = mticker.FixedLocator([-95,-90,-85,-80])
	
	gl.top_labels = False; gl.right_labels = False
	
	gl.xlines = False; gl.ylines = False
	
	gl.xlabel_style = {'size': 15}
	gl.ylabel_style = {'size': 15}
	#gl.rotate_labels = False
	
	gl.yformatter = LatitudeFormatter()
	gl.xformatter = LongitudeFormatter()
	
	return ax, plt
