"""
Python modules for making spatial plots of ELM outputs
"""
import os
import sys
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature

__author__ = 'Eva Sinha'
__email__  = 'eva.sinha@pnnl.gov'

plt.rc('figure', titlesize=15)
plt.rc('legend', fontsize=15)
plt.rc('axes',   labelsize=15, titlesize=15)
plt.rc('xtick',  labelsize=15)
plt.rc('ytick',  labelsize=15)
plt.rc('figure', figsize=(11, 8.5))

from util_myDict_labels import *

# -----------------------------------------------------------
def xr_plot_US_discreet_color(da_plot, plot_title, levels, colors, ticks, cbar_label, fig_wt, fig_ht, fig_extent, show_states, fname):

    # Change directory    
    os.chdir('../figures/')

    fig, axis = plt.subplots(1, 1, figsize=(fig_wt, fig_ht),
                             subplot_kw=dict(projection=ccrs.LambertConformal(central_longitude=-95, central_latitude=37.5)))

    fg = da_plot.plot(ax          = axis, 
                      transform   = ccrs.PlateCarree(),
                      cbar_kwargs = {'label':       cbar_label,
                                     'ticks':       ticks,
                                     'orientation': 'horizontal',
                                     'shrink':      0.8,
                                     'aspect':      30,
                                     'pad':         0.02, # fraction of original axes between colorbar and new image axes
                      },
                      levels      = levels,
                      colors      = colors)

    # Set aspect ratio
    fg.axes.set_aspect(1)

    # Add additional features like coastline, oceans, and lakes
    fg.axes.coastlines()
    fg.axes.add_feature(cfeature.OCEAN)
    fg.axes.add_feature(cfeature.LAND, facecolor ='gainsboro') # To add a background grey color
    fg.axes.add_feature(cfeature.LAKES, edgecolor='black')
    if(show_states):
       fg.axes.add_feature(cfeature.STATES, edgecolor='black')

    # Add title
    fg.axes.set_title(plot_title)

    # Define map extent
    plt.gca().set_extent(fig_extent)

    plt.savefig(fname, bbox_inches='tight')

    plt.close(fig=None)
    
    # Change directory    
    os.chdir('../workflow/')

# ---------------------------------

fpath = '../figures/'
fname = 'FluxCom_3sets.nc'

# Open a netcdf domain dataset
ds = xr.open_dataset(fpath + fname)

# Compute difference between FluxCom and simulated
ds['GPP'].loc['Composite',:,:] = ds['GPP'].loc['Composite',:,:] - ds['GPP'].loc['FluxCom',:,:]
ds['GPP'].loc['Set1',:,:]      = ds['GPP'].loc['Set1',:,:]      - ds['GPP'].loc['FluxCom',:,:]
ds['GPP'].loc['Set2',:,:]      = ds['GPP'].loc['Set2',:,:]      - ds['GPP'].loc['FluxCom',:,:]
ds['GPP'].loc['Set3',:,:]      = ds['GPP'].loc['Set3',:,:]      - ds['GPP'].loc['FluxCom',:,:]

# Create an empty dataset 
ds_new = ds

# Crate new 2d variable by copy existing variable and then drop it
ds_new['Min_Set'] = ds_new['GPP'].sel(Set='Composite')[:,:]
ds_new = ds_new.drop('GPP')

# Assign zero value to the new variable
ds_new['Min_Set'][:,:] = 0

# Iterate through all grid cells to identify Set with
# lowest absolute difference between Observations and Set
for i in range(len(ds.lat.values)):
    for j in range(len(ds.lon.values)):
        Comp_value = abs(ds['GPP'].sel(Set='Composite')[i, j].values)
        Set1_value = abs(ds['GPP'].sel(Set='Set1')[i, j].values)
        Set2_value = abs(ds['GPP'].sel(Set='Set2')[i, j].values)
        Set3_value = abs(ds['GPP'].sel(Set='Set3')[i, j].values)
        print(Comp_value, Set1_value, Set2_value, Set3_value)
        #if(Comp_value <= Set1_value and Comp_value <= Set2_value and Comp_value <= Set3_value):
        #    ds_new['Min_Set'][i, j] = 0
        #elif(Set1_value <= Set2_value and Set1_value <= Set3_value):
        if(Set1_value <= Set2_value and Set1_value <= Set3_value):
            ds_new['Min_Set'][i, j] = 1
        elif(Set2_value <= Set3_value):
            ds_new['Min_Set'][i, j] = 2
        else:
            ds_new['Min_Set'][i, j] = 3
        
#levels = [-0.5,0.5,1.5, 2.5, 3.5]
#colors = ['orange','red','blue','lightgreen']
#ticks  = [0,1,2,3]

levels = [0.5,1.5, 2.5, 3.5]
colors = ['red','blue','lightgreen']
ticks  = [1,2,3]

xr_plot_US_discreet_color(ds_new['Min_Set'], plot_title='', levels=levels,\
                 colors=colors, ticks=ticks, cbar_label='Set with minimum absolute difference', fig_wt=6.0, fig_ht=6.0, \
#                 fig_extent=fig_extent, show_states=True, fname='FluxCom_min_abs_diff_with_Composite.png')
                 fig_extent=fig_extent, show_states=True, fname='FluxCom_min_abs_diff.png')
