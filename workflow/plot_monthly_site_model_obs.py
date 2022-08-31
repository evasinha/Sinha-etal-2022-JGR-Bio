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

# Adding month name and repeating rows for all specified months
for ind, mon in enumerate(all_mon_str):
    if(ind == 0):
        site_data_corn_mon    = site_data_corn_orig.assign(month=mon)
        site_data_soybean_mon = site_data_soybean_orig.assign(month=mon)
    else:
        site_data_corn_mon    = pd.concat([site_data_corn_mon,    site_data_corn_orig.assign(month=mon)], ignore_index=True)
        site_data_soybean_mon = pd.concat([site_data_soybean_mon, site_data_soybean_orig.assign(month=mon)], ignore_index=True)

# List of variable names that we want to keep
varnames = ['GPP', 'ER', 'EFLX_LH_TOT']

time_period = 'Monthly'

# Whether to estimate monthly total
est_mon_total = [True, True, False]

for ind, var in enumerate(varnames):

   if(var in ['GPP','ER']):
      # Subset sites that have carbon flux data
      site_data_corn    = site_data_corn_mon[site_data_corn_mon['carbon_flux'] == True].drop(['carbon_flux'], axis=1)
      site_data_soybean = site_data_soybean_mon[site_data_soybean_mon['carbon_flux'] == True].drop(['carbon_flux'], axis=1)
   elif(var == 'EFLX_LH_TOT'):
      # Remove column that checks for carbon flux data
      site_data_corn    = site_data_corn_mon.drop(['carbon_flux'], axis=1)
      site_data_soybean = site_data_soybean_mon.drop(['carbon_flux'], axis=1)

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

      # Estimate average monthly for summer months
      da_plot = create_summer_average_monthly(ds_model[var], all_mon, all_mon_str, var, conv_factor[var], est_mon_total[ind])
    
      # Interpolate ELM outputs for site lat lon save in data frame
      site_data_corn    = site_data_interp_monthly(site_data_corn, 'corn', da_plot, key)
      site_data_soybean = site_data_interp_monthly(site_data_soybean, 'soybean', da_plot, key)

   # Update site data output to add composite set result as new column
   site_data_corn    = site_data_add_composite(site_data_corn)
   site_data_soybean = site_data_add_composite(site_data_soybean)

   # Add as columns to site location data frame
   site_data_corn['Crop']    = 'Corn'
   site_data_soybean['Crop'] = 'Soybean'

   # Row bind into a single data frame
   site_data = pd.concat([site_data_corn, site_data_soybean])

   site_data = site_data.melt(id_vars=['SiteID', 'lat', 'lon', 'month', 'Crop'])

   # Only keep data for 'Observed','Default','Composite'
   site_data = site_data.loc[site_data['variable'].isin(['Observed','Default','Composite'])]

   facet_grid_line(site_data, ylabel=myDict_labels[time_period][var], xtick_labels=all_mon_str, fname='Sitelevel_'+var+'_pft_lineplot.png')
