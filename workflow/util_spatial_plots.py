"""
Python modules for plotting time series
"""

import os
import matplotlib as mpl
mpl.use('agg')
import pandas as pd
import geopandas
import xarray as xr
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
from mapclassify import UserDefined

__author__ = 'Eva Sinha'
__email__  = 'eva.sinha@pnnl.gov'

plt.rc('figure', titlesize=15)
plt.rc('legend', fontsize=15)
plt.rc('axes',   labelsize=15, titlesize=15)
plt.rc('xtick',  labelsize=15)
plt.rc('ytick',  labelsize=15)
plt.rc('figure', figsize=(11, 8.5))

# -----------------------------------------------------------
# Make spatial plot of xarray dataset showing boundaries of lakes and states
def xr_plot(da_plot, cbar_label, fname, xy_df=pd.DataFrame()):

    # Change directory    
    os.chdir('../figures/')

    cust_cmap = ListedColormap(['mistyrose','lightyellow','lightcyan'], name='from_list', N=None)

    fig, axis = plt.subplots(1, 1, figsize=(8, 8), 
                             subplot_kw=dict(projection=ccrs.LambertConformal(central_longitude=-95, central_latitude=37.5)))

    da_plot.plot(ax           = axis, 
                 add_colorbar = False,
                 transform    = ccrs.PlateCarree(),
                 cmap         = cust_cmap)

    if(xy_df.empty == False):
       for index, row in xy_df.iterrows():
          if(row['carbon_flux'] == True):
             plt.plot(row['lon'], row['lat'], 
                      markersize = 6,  
                      marker     = 'o',
                      color      = 'red',
                      transform  = ccrs.PlateCarree())

             plt.text(row['lon']+0.1, row['lat']+0.1, row['SiteID'], 
                      horizontalalignment = 'left', 
                      color               = 'red',
                      size                = 16, 
                      transform           = ccrs.PlateCarree())
          elif(row['carbon_flux'] == False):
             plt.plot(row['lon'], row['lat'], 
                      markersize = 6,  
                      marker     = 'o',
                      color      = 'darkgreen',
                      transform  = ccrs.PlateCarree())

             plt.text(row['lon']+0.1, row['lat']-0.2, row['SiteID'], 
                      horizontalalignment = 'left', 
                      color               = 'darkgreen',
                      size                = 16, 
                      transform           = ccrs.PlateCarree())

    # Add additional features like coastline, oceans, and lakes
    axis.add_feature(cfeature.LAKES,  edgecolor='black')
    axis.add_feature(cfeature.STATES, edgecolor='black')

    # Add gridlines
    gl = axis.gridlines(crs         = ccrs.PlateCarree(),
                        draw_labels = False,
                        color       = 'gray',
                        alpha       = 0.25)
    gl.xlocator = mticker.FixedLocator(np.arange(-99, -81.5, 0.5))
    gl.ylocator = mticker.FixedLocator(np.arange(37,  47.5,  0.5))
    plt.savefig(fname, bbox_inches='tight')

    plt.close(fig=None)
    
    # Change directory    
    os.chdir('../workflow/')

# -----------------------------------------------------------
def xr_plot_US(da_plot, plot_title, cmap_col, cbar_label, fig_wt, fig_ht, fig_extent, show_states, fname):

    # Change directory    
    os.chdir('../figures/')

    fig, axis = plt.subplots(1, 1, figsize=(fig_wt, fig_ht),
                             subplot_kw=dict(projection=ccrs.LambertConformal(central_longitude=-95, central_latitude=37.5)))

    fg = da_plot.plot(ax          = axis, 
                      transform   = ccrs.PlateCarree(),
                      cbar_kwargs = {'label':       cbar_label,
                                     'orientation': 'horizontal',
                                     'shrink':      0.8,
                                     'aspect':      20,
                                     'pad':         0.02, # fraction of original axes between colorbar and new image axes
                      },
                      cmap        = cmap_col)

    # Set aspect ratio
    fg.axes.set_aspect(1)

    # Add additional features like coastline, oceans, and lakes
    fg.axes.coastlines()
    fg.axes.add_feature(cfeature.OCEAN)
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

# -----------------------------------------------------------
def facet_plot(da_plot, colplot, colwrap, fig_wt, fig_ht, fname):

    # Change directory    
    os.chdir('../figures/')
 
    # facetting using xarray
    fg = da_plot.plot(
        col         = colplot,
        col_wrap    = colwrap,  # max columns in each row
        transform   = ccrs.PlateCarree(), # coordinate system of data
        subplot_kws = {'projection': ccrs.Robinson(central_longitude=0)}, # projection of resulting plot
        cmap        = 'bwr',
        cbar_kwargs = {
            'orientation': 'horizontal',
            'shrink': 0.8,
            'aspect': 40,
            'pad':    0.02, # fraction of original axes between colorbar and new image axes
        },
        figsize     = (fig_wt, fig_ht)
    )

    # Add additional features like coastline and oceans
    fg.map(lambda: plt.gca().coastlines())
    fg.map(lambda: plt.gca().add_feature(cfeature.OCEAN))

    plt.savefig(fname, bbox_inches='tight')

    plt.close(fig=None)
    
    # Change directory    
    os.chdir('../workflow/')

# -----------------------------------------------------------
def facet_plot_US(da_plot, subplot_titles, colplot, colwrap, cmap_col, cbar_label, fig_wt, fig_ht, fig_extent, show_states, fname, main_title=''):

    # Change directory
    os.chdir('../figures/')

    if(fig_wt < 6):
       cbar_aspect = 25
    else:
       cbar_aspect = 60

    # facetting using xarray
    fg = da_plot.plot(
        col         = colplot,
        col_wrap    = colwrap,
        transform   = ccrs.PlateCarree(), # coordinate system of data
        subplot_kws = {'projection': ccrs.LambertConformal(central_longitude=-95, central_latitude=37.5)},
        cmap        = cmap_col,
        cbar_kwargs = {
            'label':       cbar_label,
            'orientation': 'horizontal',
            'shrink':      0.8,
            'aspect':      cbar_aspect,
            'pad':         0.02, # fraction of original axes between colorbar and new image axes
        },
        figsize     =  (fig_wt, fig_ht)
        #aspect      = 1,
        #size        = 5
    )

    plt.suptitle(main_title, y=0.99)

    for ax, title in zip(fg.axes.flat, subplot_titles):
       ax.set_title(title)

    # Iterate thorugh each axis
    for ax in fg.axes.flat:

       # Modify column title
       if (colplot in ['month', 'Set', 'pft', 'col']):
           if ax.get_title():
               tmp = ax.get_title().split('=')[1]
               if(colplot in ['month', 'pft', 'col']):
                   # Add original title to the right of the plot as text
                   ax.text(1.0, 0.5, tmp.title(), transform=ax.transAxes, rotation=-90,fontsize=15)
                   # Remove the original title
                   ax.set_title(label='')
               else:
                   if (tmp == ' No_rot_Composite'):
                      ax.set_title('Composite (no rotation)', fontsize=15)
                   else:
                      ax.set_title(tmp.title(), fontsize=15)
 
    # Define map extent
    fg.map(lambda: plt.gca().set_extent(fig_extent))

    # Add additional features like coastlines, ocean, and lakes
    fg.map(lambda: plt.gca().coastlines())
    fg.map(lambda: plt.gca().add_feature(cfeature.OCEAN))
    fg.map(lambda: plt.gca().add_feature(cfeature.LAKES, edgecolor='black'))
    if(show_states):
       fg.map(lambda: plt.gca().add_feature(cfeature.STATES, edgecolor='black'))

    plt.savefig(fname, bbox_inches='tight')

    plt.close(fig=None)

    # Change directory
    os.chdir('../workflow/')

# -----------------------------------------------------------
def facet_grid_plot_US(da_plot, colplot, rowplot, cmap_col, cbar_label, fig_wt, fig_ht, fig_extent, show_states, fname):

    # Change directory    
    os.chdir('../figures/')

    # facetting using xarray
    fg = da_plot.plot(
        col         = colplot,
        row         = rowplot,
        transform   = ccrs.PlateCarree(), # coordinate system of data
        subplot_kws = {'projection': ccrs.LambertConformal(central_longitude=-95, central_latitude=37.5)}, # projection of resulting plot
        cmap        = cmap_col,
        add_colorbar=False,
        figsize     =  (fig_wt, fig_ht)
        #aspect      = 1,
        #size        = 5
    )

    # https://cduvallet.github.io/posts/2018/11/facetgrid-ylabel-access
    # Iterate thorugh each axis
    for ax in fg.axes.flat:

        # Modify column title
        if (colplot in ['month', 'Set']):
            if ax.get_title():
                tmp = ax.get_title().split('=')[1]
                if (tmp == ' No_rot_Composite'):
                    ax.set_title('Composite (no rotation)', fontsize=15)
                else:
                    ax.set_title(tmp.title(), fontsize=15)
        else:
            if ax.get_title():
                tmp = ax.get_title().split('=')[1]
                tmp = tmp.split('_')[0] + ' ' + tmp.split('_')[1]
                ax.set_title(tmp.title(), fontsize=15)

        # Modify right ylabel more human-readable and larger
        # Only the 2nd and 4th axes have something in ax.texts
        if ax.texts:
            # This contains the right ylabel text
            txt = ax.texts[0]
            ax.text(txt.get_unitless_position()[0], txt.get_unitless_position()[1],
                    txt.get_text().split('=')[1].title(),
                    transform = ax.transAxes,
                    va        = 'center',
                    fontsize  = 15,
                    rotation  = -90)
            # Remove the original text
            ax.texts[0].remove()

    # Add colorbar at bottom
    fg.add_colorbar(orientation='horizontal', label=cbar_label, shrink=0.8, aspect=60, pad=0.02)

    # Define map extent
    fg.map(lambda: plt.gca().set_extent(fig_extent))
    
    # Add additional features like coastlines, ocean, and lakes
    fg.map(lambda: plt.gca().coastlines())
    fg.map(lambda: plt.gca().add_feature(cfeature.OCEAN))
    fg.map(lambda: plt.gca().add_feature(cfeature.LAKES, edgecolor='black'))
    if(show_states):
        fg.map(lambda: plt.gca().add_feature(cfeature.STATES, edgecolor='black'))

    plt.savefig(fname, bbox_inches='tight')

    plt.close(fig=None)
    
    # Change directory    
    os.chdir('../workflow/')

# -----------------------------------------------------------
def plot_xa_gpd(da_plot, geo_data, cmap_col, cbar_label, fig_wt, fig_ht, fname):

   # Change directory
   os.chdir('../figures/')

   # User specified bins
   #usr_bins_corn = [0, 5, 10, 15]
   #usr_bins_soy  = [0, 1, 2, 3, 4]

   fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, figsize=(fig_wt, fig_ht),
                                           subplot_kw=dict(projection=ccrs.PlateCarree()))

   da_plot.isel(pft=0).plot(ax          = ax1,
                            transform   = ccrs.PlateCarree(),
                            #levels      = usr_bins_corn,
                            #cbar_kwargs = {'ticks':       usr_bins_corn,
                            cbar_kwargs = {'label':       cbar_label,
                                           'orientation': 'horizontal',
                                           'shrink':      0.8,
                                           'aspect':      40,
                                           'pad':         0.02},
                            vmin        = 0,
                            vmax        = geo_data.Corn_ton_ha.max(),
                            cmap        = cmap_col)

   da_plot.isel(pft=1).plot(ax          = ax3,
                            transform   = ccrs.PlateCarree(),
                            #levels      = usr_bins_soy,
                            #cbar_kwargs = {'ticks':       usr_bins_soy,
                            cbar_kwargs = {'label':       cbar_label,
                                           'orientation': 'horizontal',
                                           'shrink':      0.8,
                                           'aspect':      40,
                                           'pad':         0.02},
                            vmin        = 0,
                            vmax        = geo_data.Soy_ton_ha.max(),
                            cmap        = cmap_col)

   # Transform projection
   crs_proj4 = ccrs.PlateCarree().proj4_init
   geo_data  = geo_data.to_crs(crs_proj4)

   geo_data.plot(ax          = ax2,
                 column      = 'Corn_ton_ha',
                 cmap        = cmap_col,
                 edgecolor   = None,
                 #scheme      = 'userdefined',
                 #classification_kwds={'bins':usr_bins},
                 legend      = True,
                 legend_kwds = {'fmt':        '{:.0f}',
                                'label':       cbar_label,
                                'orientation': 'horizontal',
                                'shrink':     0.8,
                                'aspect':     40,
                                'pad':        0.02})
                                #'title':      cbar_label,
                                #'loc':        'center left',
                                #'interval':   True})

   geo_data.plot(ax          = ax4,
                 column      = 'Soy_ton_ha',
                 cmap        = cmap_col,
                 edgecolor   = None,
                 #scheme      = 'userdefined',
                 #classification_kwds={'bins':usr_bins},
                 legend      = True,
                 legend_kwds = {'fmt':        '{:.0f}',
                                'label':       cbar_label,
                                'orientation': 'horizontal',
                                'shrink':     0.8,
                                'aspect':     40,
                                'pad':        0.02})
                                #'title':      cbar_label,
                                #'loc':        'center left',
                                #'interval':   True})

   ax2.set_title('Corn')
   ax4.set_title('Soybean')

   # Add additional features like coastline, oceans, and lakes
   for i, ax in enumerate([ax1, ax3]):
      ax.coastlines()
      ax.add_feature(cfeature.LAKES, edgecolor='black')
      ax.add_feature(cfeature.STATES, edgecolor='black')

   # ----- Load states and lakes shapefile -----
   natearth_states = geopandas.read_file(shpreader.natural_earth(resolution='10m', category='cultural', name='admin_1_states_provinces'))
   natearth_lakes  = geopandas.read_file(shpreader.natural_earth(resolution='10m', category='physical', name='lakes'))

   for i, ax in enumerate([ax2, ax4]):
      # Add states and lakes layer
      natearth_states.geometry.boundary.plot(ax=ax, color=None, edgecolor='black')
      natearth_lakes.geometry.boundary.plot(ax=ax, facecolor=([0.59375, 0.71484375, 0.8828125 ]), edgecolor='black')

      # Modify x and y limit
      ax.set_xlim(-99, -82)
      ax.set_ylim(37, 47)
      ax.set_axis_off()

   plt.savefig(fname, bbox_inches='tight')

   os.chdir('../workflow/')

# -----------------------------------------------------------
def plot_xa_model_obs(da_plot, da_obs, cbar_label, fig_wt, fig_ht, fname):

   # Change directory
   os.chdir('../figures/')

   fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(fig_wt, fig_ht),
                                           subplot_kw=dict(projection=ccrs.PlateCarree()))

   da_obs.plot(ax         = ax1,
               transform   = ccrs.PlateCarree(),
               cbar_kwargs = {'label':       cbar_label,
                              'orientation': 'horizontal',
                              'shrink':      0.8,
                              'aspect':      40,
                              'pad':         0.02},
               cmap        = 'jet')
   
   da_plot.plot(ax          = ax2,
               transform   = ccrs.PlateCarree(),
               cbar_kwargs = {'label':       cbar_label,
                              'orientation': 'horizontal',
                              'shrink':      0.8,
                              'aspect':      40,
                              'pad':         0.02},
               cmap        = 'jet')

   # Estimate difference between observed and modeled
   diff = da_plot - da_obs

   diff.plot(ax          = ax3,
             transform   = ccrs.PlateCarree(),
             cbar_kwargs = {'label':       cbar_label,
                            'orientation': 'horizontal',
                            'shrink':      0.8,
                            'aspect':      40,
                            'pad':         0.02},
             cmap        = 'bwr')

   # Add additional features like coastline, oceans, and lakes
   for i, ax in enumerate([ax1, ax2, ax3]):
       ax.coastlines()
       ax.add_feature(cfeature.LAKES, edgecolor='black')
       ax.add_feature(cfeature.STATES, edgecolor='black')

   ax1.set_title('Observed - FluxCom')
   ax3.set_title('Model -  Observed')

   plt.savefig(fname, bbox_inches='tight')

   os.chdir('../workflow/')

# -----------------------------------------------------------
def xr_plot_global(da_plot, fig_wt, fig_ht, fname):

    # Change directory    
    os.chdir('../figures/')
    #print(np.nanmax(da_plot.values))
    #print(np.nanmin(da_plot.values))

    fig, axis = plt.subplots(1, 1, figsize=(fig_wt, fig_ht),
                             subplot_kw=dict(projection=ccrs.Robinson(central_longitude=0)))

    da_plot.plot(ax          = axis, 
                 transform   = ccrs.PlateCarree(),
                 cbar_kwargs = {'orientation': 'horizontal', 'shrink': 0.7, 'pad': 0.02},
                 cmap        = 'YlGnBu')

    # Add additional features like coastline and oceans
    axis.coastlines()
    axis.add_feature(cfeature.OCEAN)

    plt.savefig(fname, bbox_inches='tight')

    plt.close(fig=None)
    
    # Change directory    
    os.chdir('../')
