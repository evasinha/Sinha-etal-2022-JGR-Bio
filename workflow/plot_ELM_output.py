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
# List of variable names that we want to keep
varnames = ['GPP', 'ER']

for ind, var in enumerate(varnames):

   #iterate through dictionary
   for i, key in enumerate(myDict_caseid):

      # Read ELM model output for select variables
      fpath = '/compyfs/sinh210/e3sm_scratch/' + myDict_caseid[key] + '/run/'
      ds_model = read_model_output(yr_start, yr_end, fpath, myDict_caseid[key], var)

      # Estimate mean annual from monthly data
      da_plot = create_mean_annual_da(ds_model, var, conv_factor[var], est_mon_total=True)
      
      # Merge all datasets into a single dataset
      da_plot = da_plot.expand_dims(Set = [key])

      if (i == 0):
         da_plot_merge = da_plot
      else:
         da_plot_merge = xr.merge([da_plot_merge, da_plot])

   # Create a composite grid and plot composite grid and difference between composite grid and original set
   create_plot_composite(da_plot_merge, var, time_period='Annual', fname_abb='fig_regional_Annual')

# ---------- Plot monthly fluxes ----------
# List of variable names that we want to keep
varnames = ['GPP', 'ER', 'EFLX_LH_TOT', 'FSH', 'TLAI']

# Whether to estimate monthly total
est_mon_total = [True, True, False, False, False]
select_month = 'August'

for ind, var in enumerate(varnames):

   #iterate through dictionary
   for i, key in enumerate(myDict_caseid):

      # Read ELM model output for select variables
      fpath = '/compyfs/sinh210/e3sm_scratch/' + myDict_caseid[key] + '/run/'
      ds_model = read_model_output(yr_start, yr_end, fpath, myDict_caseid[key], var)
 
      # Estimate average monthly for summer months
      da_plot = create_summer_average_monthly(ds_model, sum_mon, sum_mon_str, var, conv_factor[var], est_mon_total[ind])
      
      # Create facet plot showing summer months in different columns
      cmap_col = 'jet'
      facet_plot_US(da_plot, subplot_titles='', colplot='month', colwrap=len(sum_mon), \
                    cmap_col=cmap_col, cbar_label=myDict_labels['Monthly'][var], fig_wt=5*len(sum_mon), fig_ht=8, \
                    fig_extent=fig_extent, show_states=True, fname=key+'_monthly_'+var+'.png')

      # Merge all datasets into a single dataset 
      da_plot = da_plot.expand_dims(Set = [key])

      if (i == 0):
         da_plot_merge = da_plot
      else:
         da_plot_merge = xr.merge([da_plot_merge, da_plot])

   # Create a composite grid and plot composite grid and difference between composite grid and original set
   create_plot_composite(da_plot_merge, var, time_period='Monthly', fname_abb='Summer_months')
