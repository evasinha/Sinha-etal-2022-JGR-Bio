"""
Python modules for plotting time series
"""

import os
import sys
import matplotlib as mpl
mpl.use('Agg')
import numpy as np
import xarray as xr
import netCDF4 as nc

__author__ = 'Eva Sinha'
__email__  = 'eva.sinha@pnnl.gov'

from util_spatial_plots import *
from util_myDict_labels import *

# -----------------------------------------------------------
# Create modified landuse timeseries with corn soybean rotation
# based on LUH2 tansition from c4 perennial to c3 n-fixing
def modify_landuse_ts(fpath, fname, hist_trans):

   filename_old = fpath + fname   
   ds_old       = nc.Dataset(filename_old)

   # Create new landuse timeseries netcdf file
   filename = '/compyfs/sinh210/user_inputdata/lnd/clm2/surfdata_map/landuse.timeseries_360x720cru_hist_50pfts_corn_soy_rot_c220216.nc'
   
   # ---------- Create netcdf file ----------
   if os.path.exists(filename):
      os.remove(filename)
    
   ds = nc.Dataset(filename, 'w', format='NETCDF3_64BIT')

   # ----- Copy dimensions -----
   # https://gist.github.com/guziy/8543562 
   for dname, the_dim in ds_old.dimensions.items():
      print (dname, len(the_dim))
      ds.createDimension(dname, len(the_dim) if not the_dim.isunlimited() else None)

   # ----- Copy variables -----
   for v_name, varin in ds_old.variables.items():
      print (v_name, varin.datatype, varin.dimensions) 
      
      outVar = ds.createVariable(v_name, varin.datatype, varin.dimensions)

      # ----- Copy variable attributes -----
      outVar.setncatts({k: varin.getncattr(k) for k in varin.ncattrs()})
    
      # ----- Copy variable values -----
      outVar[:] = varin[:]

      if (v_name == 'PCT_CFT'):
         # Grid cells where corn soybean rotation occurs
         # in even years (2000 2002 2004 2006 2008 2010 2012 2014)
         # corn should have sum of corn + rotat_frac*soybean area and soybean should have (1-rotat_frac)*soybean %
         # in odd years (2001 2003 2005 2007 2009 2011 2013 2015)
         # soybean should have sum of soybean + rotat_frac*corn area and corn should have (1-rotat_frac)*corn %
         for yr in range(2000, 2016, 2):
            for lat in hist_trans['lsmlat'].values:
               for lon in hist_trans['lsmlon'].values :  
                 # print(np.where(ds_old['time'][:] == yr))
                  time_inds = np.where(ds_old['time'][:] == yr)[0][0]
                  lat_inds  = np.where(ds_old['lsmlat'][:]  == lat)[0][0]
                  lon_inds  = np.where(ds_old['lsmlon'][:]  == lon)[0][0]
                  if(~np.isnan(hist_trans.sel(lsmlat= lat, lsmlon=lon).values)):
                     #print(hist_trans.sel(lsmlat= lat, lsmlon=lon).values)
                     #print(outVar[time_inds, 2, lat_inds, lon_inds], outVar[time_inds, 8, lat_inds, lon_inds])
                     outVar[time_inds, 2, lat_inds, lon_inds] = outVar[time_inds, 2, lat_inds, lon_inds] + hist_trans.sel(lsmlat= lat, lsmlon=lon).values * outVar[time_inds, 8, lat_inds, lon_inds]
                     outVar[time_inds, 8, lat_inds, lon_inds] = (1 - hist_trans.sel(lsmlat= lat, lsmlon=lon).values) * outVar[time_inds, 8, lat_inds, lon_inds]
                     #print(outVar[time_inds, 2, lat_inds, lon_inds], outVar[time_inds, 8, lat_inds, lon_inds])
         for yr in range(2001, 2016, 2):
            for lat in hist_trans['lsmlat'].values:
               for lon in hist_trans['lsmlon'].values :  
                  time_inds = np.where(ds_old['time'][:] == yr)[0][0]
                  lat_inds  = np.where(ds_old['lsmlat'][:]  == lat)[0][0]
                  lon_inds  = np.where(ds_old['lsmlon'][:]  == lon)[0][0]
                  if(~np.isnan(hist_trans.sel(lsmlat= lat, lsmlon=lon).values)):
                     outVar[time_inds, 8, lat_inds, lon_inds] = outVar[time_inds, 8, lat_inds, lon_inds] + hist_trans.sel(lsmlat= lat, lsmlon=lon).values * outVar[time_inds, 2, lat_inds, lon_inds]
                     outVar[time_inds, 2, lat_inds, lon_inds] = (1 - hist_trans.sel(lsmlat= lat, lsmlon=lon).values) * outVar[time_inds, 2, lat_inds, lon_inds]

   # ----- Close the output file -----
   ds.close()

# -----------------------------------------------------------
# ----- Open landuse timeseries netcdf file -----
fpath_surf  = '/compyfs/inputdata/lnd/clm2/surfdata_map/'
fname_surf  = 'landuse.timeseries_360x720cru_hist_50pfts_simyr1850-2015_c220216.nc'
landuse_ts = xr.open_dataset(fpath_surf + fname_surf, decode_times=False)

# Plotting multiple DataArrays in a Dataset
landuse_ts = landuse_ts['PCT_CFT'].isel(time=160)

# Replace zero values with nan
landuse_ts.values[landuse_ts.values == 0] = np.nan

# ----- Open coasened LUH2 historical transitions netcdf file -----
fpath_luh2  = '/qfs/people/sinh210/wrk/luh2/360x720/'
fname_luh2  = 'c4ann_to_c3nfx_360x720.nc'
hist_trans = xr.open_dataset(fpath_luh2 + fname_luh2, decode_times=False)

# Convert from -180 to 180 to 0 to 360
hist_trans.coords['lon'] = (hist_trans.coords['lon'] + 360) % 360
hist_trans = hist_trans.sortby(hist_trans.lon)

# Rename coordinates
hist_trans = hist_trans.rename({'lat': 'lsmlat', 'lon': 'lsmlon'})

# Make spatial plot for year 1160
hist_trans = hist_trans['c4ann_to_c3nfx'].isel(time=1160)

# Identify grid cells where c4ann_to_c3nfx is greater than 5% of the grid cell
hist_trans = hist_trans.where(hist_trans > 0.05)
xr_plot_global(hist_trans, fig_wt=11, fig_ht=8.5, fname='hist_trans_c4ann_to_c3nfx_gt_5per.png')

# Subset LUH2 data to US extent
hist_trans = hist_trans.sel(lsmlon=slice(240, 290), lsmlat=slice(50,25))
cmap_col = 'jet'
plot_title = 'Corn soybean rotation'
xr_plot_US(hist_trans, plot_title=plot_title, cmap_col=cmap_col, cbar_label='Fraction of grid with crop rotation', \
           fig_wt=6.0, fig_ht=6.0, fig_extent=fig_extent, show_states=True, fname='hist_trans_US_c4ann_to_c3nfx_gt_5per.png')

# Identify grid cells where c4ann_to_c3nfx transition is greater than 5%
landuse_ts = landuse_ts.where(hist_trans > 0.05, drop=True)

# Create facet plot showing summer months in different columns
plot_data = landuse_ts.sel(cft = landuse_ts.cft.isin([17, 23]))
plot_data = plot_data.assign_coords(cft = ['corn','soybean'])
facet_plot_US(plot_data, subplot_titles='', colplot='cft', colwrap=2, cmap_col=cmap_col, cbar_label='% area within cropland unit',\
              fig_wt=5*2, fig_ht=8, fig_extent=fig_extent, show_states=True, fname='corn_soybean_cft_percent.png')

# Plot PCT_CROP
cmap_col = 'jet'
plot_title = 'Percent cropland'
landuse_ts = xr.open_dataset(fpath_surf + fname_surf, decode_times=False)
landuse_ts = landuse_ts['PCT_CROP']

# Replace zero values with nan
landuse_ts.values[landuse_ts.values == 0] = np.nan

# Plot PCT_CROP for 1850 and 2010
xr_plot_US(landuse_ts.isel(time=0), plot_title=plot_title, cmap_col=cmap_col, cbar_label='% of grid with cropland', \
           fig_wt=6.0, fig_ht=6.0, fig_extent=fig_extent, show_states=True, fname='landuse_ts_PCT_CROP_1850.png')
xr_plot_US(landuse_ts.isel(time=160), plot_title=plot_title, cmap_col=cmap_col, cbar_label='% of grid with cropland', \
           fig_wt=6.0, fig_ht=6.0, fig_extent=fig_extent, show_states=True, fname='landuse_ts_PCT_CROP_2010.png')

# Create modified landuse timeseries with corn soybean rotation
modify_landuse_ts(fpath_surf, fname_surf, hist_trans)
