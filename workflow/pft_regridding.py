import os
import numpy as np
import xarray as xr
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

from util_pftname import *
from util_read_data import *
from util_spatial_plots import *
from util_myDict_labels import *

# ----------------------------------------------------
# Modified from PFT-Gridding.ipynb in ctsm_python_gallery
# https://github.com/NCAR/ctsm_python_gallery
# ----------------------------------------------------

# -----------------------------------------------------------
def convert_2D_to_5D(mod_ds, yr_start, yr_end, var, pftname):
    """ Convert 2D output to 5D output 
    :param mod_ds:   ELM h1 output in xarray format
    :param: yr_start start year for reading model output
    :param: yr_end   end year for reading model output
    :param varname:  ELM output variable name
    :param pftname:  pftnames
    :return:         regridded xarray [years * month * pft * lat * lon]
    """
    # Reading in variables from ELM output file
    years     = np.arange(yr_start, yr_end+1, 1)
    month     = np.arange(0, 12, 1)
    
    lat       = mod_ds.lat # For smallville - mod_ds.lat[0]
    lon       = mod_ds.lon # For smallville - mod_ds.lon[0]
    time      = mod_ds.time
    ixy       = mod_ds.pfts1d_ixy.isel(time=0)
    jxy       = mod_ds.pfts1d_jxy.isel(time=0)
    vegtype   = mod_ds.pfts1d_itype_veg.isel(time=0)
    var_data  = mod_ds[var]

    nlat      = len(lat.values)
    nlon      = len(lon.values)
    ntime     = len(time.values)
    npft      = np.max(vegtype).astype(int)
    num_years = len(time)//12

    # ------ print dimensions and frequency ------
    #print(ntime, npft.values+1, nlat, nlon)

    #print(len(ixy))
    #print(len(jxy))
    #print(len(vegtype))

    #unique, frequency = np.unique(ixy, return_counts = True)
    #print(unique)
    #print(frequency)

    #unique, frequency = np.unique(jxy, return_counts = True)
    #print(unique)
    #print(frequency)

    #unique, frequency = np.unique(vegtype, return_counts = True)
    #print(unique)
    #print(frequency)
    # ------------

    # Creating gridded array
    gridded = np.empty([ntime, npft.values+1, nlat, nlon])

    # Assign ELM output variable values to the correct locations in the empty grid
    gridded[:, vegtype.values.astype(int), jxy.values.astype(int) - 1, ixy.values.astype(int) - 1] = var_data.values

    # Adding dimensions and coordinates
    gridded_da      = xr.DataArray(gridded, dims=('time', 'pft', 'lat', 'lon'))
    gridded_da      = gridded_da.assign_coords(time=mod_ds.time, pft=pftname, lat=lat.values, lon=lon.values)
    gridded_da.name = var

    # Reshaping the time dimension to year, month
    reshaped       = gridded_da.values.reshape(num_years, 12, *gridded_da.values.shape[1:])
    output_reshape = xr.DataArray(reshaped, dims=('years', 'month', 'pft', 'lat', 'lon'))
    output_reshape = output_reshape.assign_coords(years=years, month=month, pft=pftname, lat=lat.values, lon=lon.values)
  
    return output_reshape

# -----------------------------------------------------------
def apply_cropwts_cft(lu_ts, yr_start, yr_end, output_reshape):
    """ Apply crop weight mask to cfts
    :param lu_ts:          land use timeseries
    :param output_reshape: reshaped model output
    :return:               reshaped model output with crop weights applied to cfts
    """
    # Reading in variables from land use timeseriees file
    pctcft  = lu_ts.PCT_CFT
    pctcrop = lu_ts.PCT_CROP

    # Defining proportion of each crop type (pctcft) within the grid crop area (pctcrop)
    cropwts     = (pctcft/100) * (pctcrop/100)

    # Masking regions with crop area <0.5%
    cropwtsmask = cropwts.where(cropwts>0.005)

    # Plotting multiple DataArrays in a Dataset
    da_plot = cropwtsmask.isel(time=150, cft=[2, 8])

    # Replace zero values with nan
    da_plot.values[da_plot.values == 0] = np.nan

    subplot_titles = ['Corn','Soybean']
    cmap_col = 'jet'

    facet_plot_US(da_plot, subplot_titles, colplot='cft', colwrap=1, cmap_col=cmap_col, cbar_label='Crop weight mask [unitless]', 
                  fig_wt=11, fig_ht=14, fig_extent=fig_extent, show_states=True, fname='cropwtsmask_US_Midwest_corn_soybean.png')

    # Renaming dimensions
    cropwtsmask = cropwtsmask.rename({'time':'years', 'cft':'pft', 'lsmlat':'lat', 'lsmlon':'lon'})

    # Subset masks between years
    cropwtsmask = cropwtsmask.sel(years = cropwtsmask.years.isin(range(yr_start, yr_end+1)))

    # Subset only 36 cfts from the re gridded output
    output_reshape_cft = output_reshape.isel(pft = slice(15,51))

    # Assign cft names to crop weights mask
    cropwtsmask['pft'] = output_reshape_cft.pft

    # Apply the crop weight mask to cfts level model output
    output_cft_cropwts = output_reshape_cft * cropwtsmask

    # Subsetting the natural PFTs to prepare for concatenation
    output_reshape_pft = output_reshape.isel(pft = slice(0,15))

    # Concatenate pft and crops weight applied cfts
    output_reshape_cropwts = xr.concat([output_reshape_pft, output_cft_cropwts], dim='pft')

    return output_reshape_cropwts

# -----------------------------------------------------------
def reshape_time_dim(output_reshape_cropwts, mod_ds, pftname):
    """ Reshape years x month to time dimension
    :param output_reshape_cropwts: reshaped model output with crop weights applied to cfts
                                   dim - years x month x pft x lat x lon
    :param mod_ds:                 ELM h1 output in xarray format
    :param pftname:                pftnames
    :return:                       reshaped model output with time dimension
                                   dim - time x pft x lat x lon
    """
    lat = output_reshape_cropwts.lat
    lon = output_reshape_cropwts.lon

    # Reshaping the time dimension to year, month
    reshaped       = output_reshape_cropwts.values.reshape(len(mod_ds.time), *output_reshape_cropwts.values.shape[2:])
    output_reshape_final = xr.DataArray(reshaped, dims=('time', 'pft', 'lat', 'lon'))
    output_reshape_final = output_reshape_final.assign_coords(time=mod_ds.time.values, pft=pftname, lat=lat.values, lon=lon.values)

    return output_reshape_final

# -----------------------------------------------------------
# Read ELM h1 output file containing output in 1D vector format
#caseid = '20220512_20x34_corn_soy_rot_US-Ne3_param_ELM_USRDAT_ICBELMCNCROP_trans'
#caseid = '20220512_20x34_corn_soy_rot_US-Ro1_param_ELM_USRDAT_ICBELMCNCROP_trans'
#caseid = '20220512_20x34_corn_soy_rot_US-UiC_param_ELM_USRDAT_ICBELMCNCROP_trans'
#caseid = '20220512_20x34_corn_soy_rot_default_param_ELM_USRDAT_ICBELMCNCROP_trans'
#caseid = '20220609_20x34_US-Ne3_param_ELM_USRDAT_ICBELMCNCROP_trans'
#caseid = '20220609_20x34_US-Ro1_param_ELM_USRDAT_ICBELMCNCROP_trans'
#caseid = '20220609_20x34_US-UiC_param_ELM_USRDAT_ICBELMCNCROP_trans'
#caseid = '20230114_20x34_corn_soy_rot_US-Ne3_param_ELM_USRDAT_ICBELMCNCROP_trans'
caseid = '20230114_20x34_corn_soy_rot_US-Ro1_param_ELM_USRDAT_ICBELMCNCROP_trans'
#caseid = '20230114_20x34_corn_soy_rot_US-UiC_param_ELM_USRDAT_ICBELMCNCROP_trans'
#caseid = '20230114_20x34_corn_soy_rot_default_param_ELM_USRDAT_ICBELMCNCROP_trans'
#caseid = '20230114_20x34_US-Ne3_param_ELM_USRDAT_ICBELMCNCROP_trans'
#caseid = '20230114_20x34_US-Ro1_param_ELM_USRDAT_ICBELMCNCROP_trans'
#caseid = '20230114_20x34_US-UiC_param_ELM_USRDAT_ICBELMCNCROP_trans'

fpath  = '/compyfs/sinh210/e3sm_scratch/' + caseid + '/run/'

# Four steps for creating the files with and without weights
# 1. check out_fname
# 2. check varnames (only GPP is saved with weights applied)
# 3. check if apply_cropwts_cft is called or not (only GPP is saved with weights applied)
# 4. check correct lu_ts is used with the set (2 lu ts with and without crop rotation)

# GPP at pft level is saved with and without PCT_CROP and PCT_CFT weight being applied
# When plotting the whole grid we use GPP with the pct_crop and pct_cft weights being applied
# When plotting outputs to observations for corn/soybean only the percent fraction 
# is not applied since we are only focussing on the fraction of the grid with corn/soybean on it.
#out_fname = caseid + '_regridded.nc'
out_fname = caseid + '_regridded_weight_applied.nc'

#varnames = ['GPP', 'EFLX_LH_TOT', 'DMYIELD', 'PLANTDAY', 'HARVESTDAY', 'TLAI', 'LEAFC']
varnames = ['GPP']

sel_lon = 263.5234
sel_lat = 41.1651

yr_start = 2001
yr_end   = 2010
mod_ds   = read_col_lev_model_output(yr_start, yr_end, fpath, caseid)

for ind, var in enumerate(varnames):
   # Convert 2D output to 5D output
   output_reshape = convert_2D_to_5D(mod_ds, yr_start, yr_end, var, pftname)

   # Read in land use timeseries data
   # land use timeseries with corn soybean rotation
   fname = '/compyfs/sinh210/mygetregionaldata/landuse.timeseries_20x34pt_f19_US_Midwest_sub_cru_hist_50pfts_corn_soy_rot_c220216.nc'

   # land use timeseries without corn soybean rotation
   #fname = '/compyfs/sinh210/mygetregionaldata/landuse.timeseries_20x34pt_f19_US_Midwest_sub_cru_hist_50pfts_c220413.nc'
   lu_ts = xr.open_mfdataset(fname)

   #output_reshape_cropwts = output_reshape
   if(var == 'GPP'):
       # Apply crop weight mask to cfts
       output_reshape_cropwts = apply_cropwts_cft(lu_ts, yr_start, yr_end, output_reshape)
   else:
       # Skip applying crop weight masks to cfts
       output_reshape_cropwts = output_reshape

   # Reshape years x month to time dimension
   # Reshape years x month to time dimension
   output_reshape_final = reshape_time_dim(output_reshape_cropwts, mod_ds, pftname)

   # Assign variable name
   output_reshape_final.name = var

   # Copy attributes
   output_reshape_final.attrs = mod_ds[var].attrs

   if (ind == 0):
      mod_ds_regridded = output_reshape_final
   else:
      mod_ds_regridded = xr.merge([mod_ds_regridded, output_reshape_final])

# Write xarray to a new NetCDF file
os.chdir('/compyfs/sinh210/e3sm_scratch/regridded_output/')
mod_ds_regridded.to_netcdf(path=out_fname, mode='w')
