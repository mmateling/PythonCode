# ---------------------------------------------------------------------------
#
#  create_subplot_maps
#
# ----------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs		# For map projections
import cartopy.feature as cfeature	# For putting features on map
from matplotlib.cm import get_cmap	# For choosing color bar 
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1 import AxesGrid

#import gridlines_with_labels as gd

"""
 Both input parameters are strings
    on_off_flag = 'on' will show plot
    num_axes = '1x1', '1x2' (default), '2x2', '2x3', '2x4', '4x4'
    
    Change middle points (mid_lat, mid_lon) depending on location
"""

def setup_subplots(on_off_flag = 'on', num_axes='1x2'):

   # Middle point (NE Atl ocean)
	mid_lat = 70
	mid_lon = 10
	
	if on_off_flag == 'off':
		plt.ioff()


	if num_axes == '1x1':
	
		fig = plt.figure(figsize=(8,6))

		ax = plt.axes(projection = ccrs.Orthographic(mid_lon,mid_lat))		

		plot_details(ax, 'left and bottom')
		
		return ax, plt, fig


	if num_axes == '1x2':
	
		fig = plt.figure(figsize=(8,12))
	
		ax1 = plt.subplot(2, 1, 1,\
			projection = ccrs.Orthographic(mid_lon,mid_lat)) 
		ax2 = plt.subplot(2, 1, 2,\
			projection = ccrs.Orthographic(mid_lon,mid_lat))
			
		axes = [ax1, ax2]
		
		for i in axes:
			if i == ax1:
				plot_details(i, 'left')
			elif i == ax2:
				plot_details(i, 'left and bottom')
		
		return ax1, ax2, plt, fig


	if num_axes == '2x2':
		fig = plt.figure(figsize=(12,12))
	
		ax1 = plt.subplot(2, 2, 1,\
			projection = ccrs.Orthographic(mid_lon,mid_lat)) 
		ax2 = plt.subplot(2, 2, 2,\
			projection = ccrs.Orthographic(mid_lon,mid_lat))
		ax3 = plt.subplot(2, 2, 3,\
			projection = ccrs.Orthographic(mid_lon,mid_lat)) 
		ax4 = plt.subplot(2, 2, 4,\
			projection = ccrs.Orthographic(mid_lon,mid_lat))
			
		axes = [ax1, ax2, ax3, ax4]
		
		
		for i in axes:
			plot_details(i, 'left and bottom')
			
		return ax1, ax2, ax3, ax4, plt, fig


	if num_axes == '2x3':
		fig = plt.figure(figsize=(18,12))
	
		ax1 = plt.subplot(2, 3, 1,\
			projection = ccrs.Orthographic(mid_lon,mid_lat)) 
		ax2 = plt.subplot(2, 3, 2,\
			projection = ccrs.Orthographic(mid_lon,mid_lat))
		ax3 = plt.subplot(2, 3, 3,\
			projection = ccrs.Orthographic(mid_lon,mid_lat)) 
		ax4 = plt.subplot(2, 3, 4,\
			projection = ccrs.Orthographic(mid_lon,mid_lat))
		ax5 = plt.subplot(2, 3, 5,\
			projection = ccrs.Orthographic(mid_lon,mid_lat)) 
		ax6 = plt.subplot(2, 3, 6,\
			projection = ccrs.Orthographic(mid_lon,mid_lat))
			
		axes = [ax1, ax2, ax3, ax4, ax5, ax6]
		
		
		for i in axes:
			plot_details(i, 'left and bottom')

		return ax1, ax2, ax3, ax4, ax5, ax6, plt, fig



	if num_axes == '2x4':
		fig = plt.figure(figsize=(24,12))
	
		ax1 = plt.subplot(2, 4, 1,\
			projection = ccrs.Orthographic(mid_lon,mid_lat)) 
		ax2 = plt.subplot(2, 4, 2,\
			projection = ccrs.Orthographic(mid_lon,mid_lat))
		ax3 = plt.subplot(2, 4, 3,\
			projection = ccrs.Orthographic(mid_lon,mid_lat)) 
		ax4 = plt.subplot(2, 4, 4,\
			projection = ccrs.Orthographic(mid_lon,mid_lat))
		ax5 = plt.subplot(2, 4, 5,\
			projection = ccrs.Orthographic(mid_lon,mid_lat)) 
		ax6 = plt.subplot(2, 4, 6,\
			projection = ccrs.Orthographic(mid_lon,mid_lat))
		ax7 = plt.subplot(2, 4, 7,\
			projection = ccrs.Orthographic(mid_lon,mid_lat)) 
		ax8 = plt.subplot(2, 4, 8,\
			projection = ccrs.Orthographic(mid_lon,mid_lat))
			
		axes = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8]
		
		
		for i in axes:
			plot_details(i, 'left and bottom')

		return ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, plt, fig

	if num_axes == '4x4':
		fig = plt.figure(figsize=(24,24))
	
		ax1 = plt.subplot(4, 4, 1,\
			projection = ccrs.Orthographic(mid_lon,mid_lat)) 
		ax2 = plt.subplot(4, 4, 2,\
			projection = ccrs.Orthographic(mid_lon,mid_lat))
		ax3 = plt.subplot(4, 4, 3,\
			projection = ccrs.Orthographic(mid_lon,mid_lat)) 
		ax4 = plt.subplot(4, 4, 4,\
			projection = ccrs.Orthographic(mid_lon,mid_lat))
		ax5 = plt.subplot(4, 4, 5,\
			projection = ccrs.Orthographic(mid_lon,mid_lat)) 
		ax6 = plt.subplot(4, 4, 6,\
			projection = ccrs.Orthographic(mid_lon,mid_lat))
		ax7 = plt.subplot(4, 4, 7,\
			projection = ccrs.Orthographic(mid_lon,mid_lat)) 
		ax8 = plt.subplot(4, 4, 8,\
			projection = ccrs.Orthographic(mid_lon,mid_lat))
		ax9 = plt.subplot(4, 4, 9,\
			projection = ccrs.Orthographic(mid_lon,mid_lat)) 
		ax10 = plt.subplot(4, 4, 10,\
			projection = ccrs.Orthographic(mid_lon,mid_lat))
		ax11 = plt.subplot(4, 4, 11,\
			projection = ccrs.Orthographic(mid_lon,mid_lat)) 
		ax12 = plt.subplot(4, 4, 12,\
			projection = ccrs.Orthographic(mid_lon,mid_lat))
		ax13 = plt.subplot(4, 4, 13,\
			projection = ccrs.Orthographic(mid_lon,mid_lat)) 
		ax14 = plt.subplot(4, 4, 14,\
			projection = ccrs.Orthographic(mid_lon,mid_lat))
		ax15 = plt.subplot(4, 4, 15,\
			projection = ccrs.Orthographic(mid_lon,mid_lat)) 
		ax16 = plt.subplot(4, 4, 16,\
			projection = ccrs.Orthographic(mid_lon,mid_lat))
	
		axes = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, \
			ax9, ax10, ax11, ax12, ax13, ax14, ax15, ax16]
		
		
		for i in axes:
			plot_details(i, 'left and bottom')

		return ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, \
		ax9, ax10, ax11, ax12, ax13, ax14, ax15, ax16, plt, fig
	
		
# ----------------------------------------------------------------------------
	
# **** CHANGE FOR DIFFERENT MAP BOUNDARIES: ****

#	mid_lat, mid_lon, corners
	
def plot_details(ax, gridliner='left'):	

   # Middle point (NE Atl ocean)
	mid_lat = 70
	mid_lon = 10
	
   # Define projections
	
	proj = ccrs.Orthographic(central_longitude = mid_lon, \
		central_latitude = mid_lat)	
		
	platecar = ccrs.PlateCarree()
		
	states_provinces = cfeature.NaturalEarthFeature(
       		category='cultural',
       		name='admin_1_states_provinces_lines',
       		scale='110m',
       		facecolor='none')
		
	lakes_high_res = cfeature.NaturalEarthFeature('physical', \
		'lakes', '110m')
		
	land_high_res = cfeature.NaturalEarthFeature(
		category='physical',
		name='land',
		scale='50m', 
		facecolor='none',
		edgecolor='black')	

     # Set boundaries for the map (not global) x0 x1 y0 y1
	corners = [-20, 35, 58, 83]
	
    # Set up plot details
	
	ax.set_extent(corners, crs=ccrs.PlateCarree())
		
     # Create plot with coastlines
     
	ax.add_feature(land_high_res, zorder=1, facecolor='gray', \
		alpha = 0.5)
	
	ax.add_feature(states_provinces, edgecolor='black', zorder = 2)	
	
	ax.add_feature(lakes_high_res, edgecolor='black', zorder = 3)
	
	ax.add_feature(cfeature.BORDERS, zorder = 4)
	
	
	"""	
     # --> Gridlines
	gl = ax.gridlines(crs=platecar, draw_labels=False, \
		zorder=5, color = 'gray', linestyle = '--', alpha = 0.9)

	if basin == 'atlantic':
		gl.xlocator = mticker.FixedLocator([-100,-80,-60,-40,-20,0,20,40])
		gl.ylocator = mticker.FixedLocator([30,40,50,60,70])

	elif basin == 'pacific':
		gl.xlocator = mticker.FixedLocator([120,140,160,180,-160,-140,-120,-100])
		gl.ylocator = mticker.FixedLocator([30,40,50,60,70])

	gl.xlines = True
	gl.ylines = True

     # --> Labels
	gl = ax.gridlines(crs=platecar, draw_labels=True, \
		zorder=6, color = 'gray')
	
	# basin == 'atlantic'
	gl.ylocator = mticker.FixedLocator([30,40,50, 60])
	gl.xlocator = mticker.FixedLocator([-60,-40,-20,0])
	
	
	gl.top_labels = False; gl.right_labels = False
	
#	if ax_num == 0 or ax_num == 1:
#		gl.bottom_labels = False
	if ax_num == 1 or ax_num == 3:
		gl.left_labels = False

	gl.xlines = False; gl.ylines = False

	gl.xlabel_style = {'size': 15}
	gl.ylabel_style = {'size': 15}
	#gl.rotate_labels = False

	gl.yformatter = LatitudeFormatter()
	gl.xformatter = LongitudeFormatter()	
	"""
	
	
	
	return 

