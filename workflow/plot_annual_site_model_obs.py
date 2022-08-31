import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt

__author__ = 'Eva Sinha'
__email__  = 'eva.sinha@pnnl.gov'

from util_read_data import *
from util_myDict_labels import *
from util_estimate_dataset_stats import *
from util_vector_plots import *
from util_site_estimate import *

# -----------------------------------------------------------

# Read observational site lat and lon
site_data_corn_orig    = pd.read_csv('site_loc.csv')
site_data_soybean_orig = pd.read_csv('site_loc.csv')

# List of variable names that we want to keep
varnames = ['GPP', 'ER', 'EFLX_LH_TOT']

time_period = 'Annual'

# Whether to estimate monthly total
est_mon_total = [True, True, False]

for ind, var in enumerate(varnames):

   if(var in ['GPP','ER']):
      # Subset sites that have carbon flux data
      site_data_corn    = site_data_corn_orig[site_data_corn_orig['carbon_flux'] == True].drop(['carbon_flux'], axis=1)
      site_data_soybean = site_data_soybean_orig[site_data_soybean_orig['carbon_flux'] == True].drop(['carbon_flux'], axis=1)
   elif(var == 'EFLX_LH_TOT'):
      # Remove column that checks for carbon flux data
      site_data_corn    = site_data_corn_orig.drop(['carbon_flux'], axis=1)
      site_data_soybean = site_data_soybean_orig.drop(['carbon_flux'], axis=1)

   # Read and add observed flux to the site data data frame
   site_data_corn    = add_obs_site_data(site_data_corn, 'corn', var, obs_conv_factor[var], time_period, est_mon_total[ind])
   site_data_soybean = add_obs_site_data(site_data_soybean, 'soybean', var, obs_conv_factor[var], time_period, est_mon_total[ind])

   #iterate through dictionary
   for i, key in enumerate(myDict_caseid):

      # Read ELM model output for select variables
      fpath = '/compyfs/sinh210/e3sm_scratch/regridded_output/'
      if(var in ['GPP','EFLX_LH_TOT']):
         fname = myDict_caseid[key] + '_regridded.nc'
      
         ds_model = xr.open_mfdataset(fpath + fname)

         # Subset data for corn and soybean
         ds_model = ds_model.sel(pft = ds_model.pft.isin(['corn', 'soybean']))

      elif(var == 'ER'):
         fname = myDict_caseid[key] + '_column_regridded.nc'
      
         ds_model = xr.open_mfdataset(fpath + fname)

         # Subset data for corn and soybean
         ds_model = ds_model.sel(col = ds_model.col.isin([217, 223]))
         ds_model = ds_model.assign_coords(time=ds_model.time.values, col=['corn','soybean'], lat=ds_model.lat.values, lon=ds_model.lon.values)

         # Rename coordinates
         ds_model = ds_model.rename({'col': 'pft'})

      # Estimate mean annual from monthly data
      da_plot = create_mean_annual_da(ds_model[var], var, conv_factor[var], est_mon_total[ind])

      # Interpolate ELM outputs for site lat lon save in data frame
      site_data_corn    = site_data_interp(site_data_corn, 'corn', da_plot, key)
      site_data_soybean = site_data_interp(site_data_soybean, 'soybean', da_plot, key)

   # Update site data output to add composite set result as new column
   site_data_corn    = site_data_add_composite(site_data_corn)
   site_data_soybean = site_data_add_composite(site_data_soybean)

   bar_plot(site_data_corn,    ylabel=myDict_labels['Annual'][var], fname='Sitelevel_'+time_period+'_'+var+'_corn.png')
   bar_plot(site_data_soybean, ylabel=myDict_labels['Annual'][var], fname='Sitelevel_'+time_period+'_'+var+'_soybean.png')

   # Make bar plots with facetting for corn and soybean
   bar_subplots(site_data_corn, site_data_soybean, title_1='Corn', title_2='Soybean', \
                ylabel=myDict_labels['Annual'][var], fname='Sitelevel_'+time_period+'_'+var+'_pft.png')

   site_data_corn.loc[:,'Default_per_diff'] = 100 * (site_data_corn['Default'] - site_data_corn['Observed'])/site_data_corn['Observed']
   site_data_corn.loc[:,'Composite_per_diff'] = 100 * (site_data_corn['Composite'] - site_data_corn['Observed'])/site_data_corn['Observed']

   site_data_soybean.loc[:,'Default_per_diff'] = 100 * (site_data_soybean['Default'] - site_data_soybean['Observed'])/site_data_soybean['Observed']
   site_data_soybean.loc[:,'Composite_per_diff'] = 100 * (site_data_soybean['Composite'] - site_data_soybean['Observed'])/site_data_soybean['Observed']

   site_data_corn[['SiteID','Observed','Default','Composite','Default_per_diff','Composite_per_diff']].to_csv(\
                  '../figures/Sitelevel_'+time_period+'_'+var+'_corn.txt', sep=',', float_format='%.2f',mode='w', index=False)
   site_data_soybean[['SiteID','Observed','Default','Composite','Default_per_diff','Composite_per_diff']].to_csv(\
                  '../figures/Sitelevel_'+time_period+'_'+var+'_soybean.txt', sep=',', float_format='%.2f', mode='w', index=False)
