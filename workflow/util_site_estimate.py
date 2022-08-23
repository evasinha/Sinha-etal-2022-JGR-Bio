import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt

__author__ = 'Eva Sinha'
__email__  = 'eva.sinha@pnnl.gov'

from util_read_data import *
from util_myDict_labels import *
from util_estimate_dataset_stats import *

# -----------------------------------------------------------
# Read and add observed flux to the site data data frame
def add_obs_site_data(site_data, site_pft, var, conv_factor, time_period, est_mon_total):

   obs_values = []
   for index, site in site_data.iterrows():
      # Read site level observations
      if(time_period == 'Annual'):
         obs_values.append(read_site_level_obs(site.SiteID, site_pft, var, conv_factor, time_period, est_mon_total))
      if(time_period == 'Monthly'):
         obs_values.append(read_site_level_obs(site.SiteID, site_pft, var, conv_factor, time_period, est_mon_total, site.month))

   # Add as columns to site location data frame
   site_data['Observed'] = obs_values

   # Convert column to numeric
   site_data['Observed'] = site_data['Observed'].astype(float)

   return(site_data)

# -----------------------------------------------------------
# Interpolate ELM outputs for site lat lon and save in data frame
def site_data_interp(site_data, site_pft, da_plot, col_name):

   site_values = []
   for index, site in site_data.iterrows():

      # Interpolate data for specified lat and lon
      site_value = da_plot.sel(pft = site_pft).interp(lat = site.lat, lon = site.lon).values

      site_values.append(site_value)

   # Add as columns to site location data frame
   site_data[col_name] = site_values

   # Convert column to numeric
   site_data[col_name] = site_data[col_name].astype(float)

   return(site_data)

# -----------------------------------------------------------
# Interpolate ELM outputs for site lat lon and save in data frame
def site_data_interp_monthly(site_data, site_pft, da_plot, col_name):

   site_values = []
   for index, site in site_data.iterrows():

      # Interpolate data for specified lat and lon
      site_value = da_plot.sel(pft = site_pft, month = site.month).interp(lat = site.lat, lon = site.lon).values

      site_values.append(site_value)

   # Add as columns to site location data frame
   site_data[col_name] = site_values

   # Convert column to numeric
   site_data[col_name] = site_data[col_name].astype(float)

   return(site_data)

# -----------------------------------------------------------
# Update site data output to add composite set result as new column
def site_data_add_composite(site_data):

   # Add column for composite
   site_values = []
   for index, site in site_data.iterrows():
      if(site.SiteID == 'US-Ne3'): site_values.append(site.Set1)
      if(site.SiteID == 'US-Ro1'): site_values.append(site.Set2)
      if(site.SiteID == 'US-UiC'): site_values.append(site.Set3)
      if(site.SiteID == 'US-Br1'): site_values.append(site.Set2)
      if(site.SiteID == 'US-Bo1'): site_values.append(site.Set3)
      if(site.SiteID == 'US-IB1'): site_values.append(site.Set3)

   # Add as a new column
   site_data['Composite'] = site_values

   return(site_data)
