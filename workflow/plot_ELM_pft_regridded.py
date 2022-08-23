"""
Python modules for making spatial plots of ELM outputs
"""
import os
import sys
import matplotlib as mpl
mpl.use('Agg')
import numpy as np
import xarray as xr
import geopandas
import pandas as pd

__author__ = 'Eva Sinha'
__email__  = 'eva.sinha@pnnl.gov'

from util_spatial_plots import *
from util_read_data import *
from util_myDict_labels import *
from util_estimate_dataset_stats import *
from util_plot_composite import *

# ---------- Plot annual fluxes ----------
# filepath for ELM regridded pft level outputs
fpath  = '/qfs/people/sinh210/wrk/E3SM_SFA/ELM-Bioenergy/spatial_plots/regridded_output/'

# List of variable names that we want to keep
varnames = ['GPP', 'DMYIELD', 'PLANTDAY', 'HARVESTDAY']

subplot_titles = ['Corn','Soybean']

for ind, var in enumerate(varnames):

   #iterate through dictionary
   for i, key in enumerate(myDict_caseid):

      # Read ELM model output for select variables
      if(var == 'GPP'):
         fname = myDict_caseid[key] + '_regridded_weight_applied.nc'
      else:
         fname = myDict_caseid[key] + '_regridded.nc'
      ds_model = xr.open_mfdataset(fpath + fname)

      # Subset data for corn and soybean
      ds_model = ds_model.sel(pft = ds_model.pft.isin(['corn', 'soybean']))

      if(var == 'GPP'):
         # Estimate mean annual from monthly data
         da_plot = create_mean_annual_da(ds_model[var], var, conv_factor[var], est_mon_total=True)
      elif(var == 'DMYIELD'):
         # Estimate mean annual yield
         da_plot = estimate_mean_annual_yield(ds_model[var], var)
      else:
         # Estimate mean annual planting and harvest
         da_plot = estimate_mean_annual_dates(ds_model[var], var)
      
      # Merge all datasets into a single dataset 
      da_plot = da_plot.expand_dims(Set = [key])
      if (i == 0):
         da_plot_merge = da_plot
      else:
         da_plot_merge = xr.merge([da_plot_merge, da_plot])

   # Create a composite grid and plot composite grid and difference between composite grid and original set
   create_plot_regridded_composite(da_plot_merge, var, plot_row='pft', time_period='Annual', fname_abb='fig_regional_Annual')

# ---------- Plot monthly fluxes ----------
# List of variable names that we want to keep
varnames = ['GPP']

for ind, var in enumerate(varnames):

   #iterate through dictionary
   for i, key in enumerate(myDict_caseid):

      # Read ELM model output for select variables
      fname = myDict_caseid[key] + '_regridded_weight_applied.nc'
      ds_model = xr.open_mfdataset(fpath + fname)

      # Subset data for corn and soybean
      ds_model = ds_model.sel(pft = ds_model.pft.isin(['corn', 'soybean']))

      # Estimate average monthly for summer months
      da_plot = create_summer_average_monthly(ds_model[var], sum_mon, sum_mon_str, var, conv_factor[var], est_mon_total=True)

      # Create facet plot showing summer months in different columns
      cmap_col = 'jet'
      facet_grid_plot_US(da_plot, colplot='month', rowplot='pft', \
                         cmap_col=cmap_col, cbar_label=myDict_labels['Monthly'][var], \
                         fig_wt=5*len(sum_mon), fig_ht=12, \
                         fig_extent=fig_extent, show_states=True, fname=key+'_monthly_'+var+'_cft.png')

      # Only keep data for a single month
      da_plot = da_plot.sel(month = select_month)

      # Merge all datasets into a single dataset
      da_plot = da_plot.expand_dims(Set = [key])
      if (i == 0):
         da_plot_merge = da_plot
      else:
         da_plot_merge = xr.merge([da_plot_merge, da_plot])

   # Create a composite grid and plot composite grid and difference between composite grid and original set
   create_plot_regridded_composite(da_plot_merge, var, plot_row='pft', time_period='Monthly', fname_abb=select_month)
