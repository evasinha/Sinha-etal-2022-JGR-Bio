__author__ = 'Eva Sinha'
__email__  = 'eva.sinha@pnnl.gov'

from util_spatial_plots import *
from util_myDict_labels import *
from util_estimate_dataset_stats import *
from util_read_data import *

#----------------------------------------------------------
# Read FluxCom data, clip to Midwest region, and estimate mean annual
def read_clip_FluxCom_data(var, time_period, select_month, obs_dataset):

   # Read FluxCom data and clip to Midwest region
   fname = FluxCom_METEO_ALL_var_fname[var]
   fpath = FluxCom_METEO_ALL_fpath
  
   # Open FluxCom netCDF data file and load the data into xarray
   ds = read_FluxCom_data(FluxCom_yr_start, FluxCom_yr_end, fpath, fname, var)
   # Clip to Midwest region
   da_plot = clip_to_midwest_region(ds, var)

   if(time_period == 'Annual'):
      # Estimate mean annual from monthly data
      da_plot = create_mean_annual_da(da_plot, var, 1, est_mon_total=True)

   if(time_period == 'Monthly'):
      # Estimate average monthly for summer months
      da_plot = create_summer_average_monthly(da_plot, sum_mon, sum_mon_str, var, 1, est_mon_total=True)
    
      # Only keep data for a single month
      #da_plot = da_plot.sel(month = select_month)

   # Replace extremely low values near the Great Lakes to nan
   #print('GPP values less than 250 gC/m2/yr that were replaced with nan')
   #tmp = da_plot.where(da_plot < 250.0).values
   #print(tmp[~np.isnan(tmp)])
   #
   #da_plot = da_plot.where(da_plot > 250.0)

   da_plot = da_plot.expand_dims(Set = [obs_dataset])

   return(da_plot)

#----------------------------------------------------------
# Read Madani et al data, clip to Midwest region, and estimate mean annual
def read_clip_Madani_et_al_data(var, time_period, select_month, obs_dataset):

   # Read Madani data and clip to Midwest region
   fname = Madani_et_al_fname
   fpath = Madani_et_al_fpath
 
   # Open netCDF data file and load the data into xarray
   ds = xr.open_dataset(fpath + fname)
   ds = ds[var]

   # Clip to Midwest region
   da_plot = clip_to_midwest_region(ds, var)

   # Subset data to keep only years between yr_start and yr_end
   da_plot = da_plot.sel(time = da_plot.time.dt.year.isin(range(yr_start, yr_end+1)))

   if(time_period == 'Annual'):
      # Estimate mean annual from monthly data
      da_plot = create_mean_annual_da(da_plot, var, 1, est_mon_total=True)

   if(time_period == 'Monthly'):
      # Estimate average monthly for summer months
      da_plot = create_summer_average_monthly(da_plot, sum_mon, sum_mon_str, var, 1, est_mon_total=True)
    
      # Only keep data for a single month
      #da_plot = da_plot.sel(month = select_month)

   # Replace 0 with nan
   da_plot = da_plot.where(da_plot != 0.0)

   da_plot = da_plot.expand_dims(Set = [obs_dataset])

   return(da_plot)

#----------------------------------------------------------
# Read MOD17A2H data and estimate mean annual
def read_MODIS_data(var, time_period, select_month, obs_dataset):

   # Read MODIS data
   fpath = MODIS_fpath

   # Read monthly MODIS GPP data
   ds_monthly = read_MODIS_monthly_data(fpath, fname='MOD17A2H_GPP_')

   ds_monthly = ds_monthly.sel(band = 1)
   ds_monthly = ds_monthly.drop_vars('band')

   # Rename coordinates
   ds_monthly = ds_monthly.rename({'x':'lon', 'y':'lat'})

   # Select variable
   ds_monthly = ds_monthly[var]

   if(time_period == 'Annual'):
      # Estimate mean annual from monthly data
      da_plot = estimate_MODIS_annual(ds_monthly, var, annual_stat='sum')

   if(time_period == 'Monthly'):
      # Estimate average monthly for summer months
      da_plot = create_summer_average_monthly(ds_monthly, sum_mon, sum_mon_str, var, 1, est_mon_total=False)
      # Only keep data for summer months
      #ds_summer = ds_monthly.sel(month = ds_monthly.month.isin(sum_mon))

      # Modify month coordinates to string
      #da_plot = ds_summer.assign_coords({'month': sum_mon_str})

      # Rename dataarray
      #ds_plot = ds_plot.rename(varname)

      # Only keep data for a single month
      #da_plot = da_plot.sel(month = select_month)

   da_plot = da_plot.expand_dims(Set = [obs_dataset])

   return(da_plot)

#----------------------------------------------------------
# Make plot comparing composite and default set to observations
def plot_model_obs_flux(da_plot_merge, var, time_period, fname_abb, obs_dataset, comp_set):

   if(obs_dataset == 'FluxCom'):
      # Read FluxCom data, clip to Midwest region, and estimate mean annual
      obs_da_plot = read_clip_FluxCom_data(var, time_period, fname_abb, obs_dataset)
   if(obs_dataset == 'Madani_et_al'):
      # Read Madani et al data, clip to Midwest region, and estimate mean annual
      obs_da_plot = read_clip_Madani_et_al_data(var, time_period, fname_abb, obs_dataset)
   if(obs_dataset == 'MODIS'):
      # Read MOD17A2H data and estimate mean annual
      obs_da_plot = read_MODIS_data(var, time_period, fname_abb, obs_dataset)

   # Rename dataarray
   da_plot_merge = da_plot_merge.rename(var)

   da_plot_merge = xr.merge([obs_da_plot, da_plot_merge.sel(Set=[comp_set,'Composite'], variable=var)])

   da_plot_merge = da_plot_merge.to_array()

   # Create facet plot showing results for various sets in different columns
   cmap_col = 'jet'
   if(time_period == 'Annual'):
      facet_plot_US(da_plot_merge.sel(Set=[obs_dataset ,comp_set, 'Composite']), \
                    subplot_titles='', colplot='Set', colwrap=3, \
                    cmap_col=cmap_col, cbar_label=myDict_labels[time_period][var], fig_wt=5*3, fig_ht=8, \
                    fig_extent=fig_extent, show_states=True, fname=fname_abb+'_'+var+'_Model_vs_'+obs_dataset+'_'+comp_set+'.png')
   elif(time_period == 'Monthly'):
      facet_grid_plot_US(da_plot_merge.sel(Set=[obs_dataset ,comp_set, 'Composite']), 
                         colplot='Set', rowplot='month', \
                         cmap_col=cmap_col, cbar_label=myDict_labels[time_period][var], fig_wt=5*3+0.3, fig_ht=5*(len(sum_mon))+0.7, \
                         fig_extent=fig_extent, show_states=True, fname=fname_abb+'_'+var+'_Model_vs_'+obs_dataset+'_'+comp_set+'.png')

   # Compute difference between set and composite set
   da_plot_merge.loc[:,'Composite',:,:] = da_plot_merge.loc[:,'Composite',:,:] - da_plot_merge.loc[:,obs_dataset,:,:]
   da_plot_merge.loc[:,comp_set,:,:]   = da_plot_merge.loc[:,comp_set,:,:] - da_plot_merge.loc[:,obs_dataset,:,:]

   # Plot after dropping Composite label from dataset
   cmap_col = 'bwr'
   if(time_period == 'Annual'):
      output = open('../figures/' + obs_dataset + ' ' + comp_set + '_stats.txt','w')
      output.write('Average difference between ' + obs_dataset + ' ' + comp_set + ' set for ' + \
                   var  + ' ' + str(round(np.nanmean(da_plot_merge.sel(Set=[comp_set]).values),2)) + '\n')
      output.write('Average difference between ' + obs_dataset + ' Composite set for ' + \
                   var  + ' ' + str(round(np.nanmean(da_plot_merge.sel(Set=['Composite']).values),2)) + '\n')
      facet_plot_US(da_plot_merge.sel(Set=[comp_set, 'Composite']), \
                    subplot_titles='', colplot='Set', colwrap=2, \
                    cmap_col=cmap_col, cbar_label=myDict_labels[time_period][var], fig_wt=5*2, fig_ht=8, \
                    fig_extent=fig_extent, show_states=True, fname=fname_abb+'_'+var+'_Model_vs_'+obs_dataset+'_'+comp_set+'_diff.png')
   elif(time_period == 'Monthly'):
      facet_grid_plot_US(da_plot_merge.sel(Set=[comp_set, 'Composite']), 
                         colplot='Set', rowplot='month', \
                         cmap_col=cmap_col, cbar_label=myDict_labels[time_period][var], fig_wt=5*2+0.3, fig_ht=5*(len(sum_mon))+0.7, \
                         fig_extent=fig_extent, show_states=True, fname=fname_abb+'_'+var+'_Model_vs_'+obs_dataset+'_'+comp_set+'_diff.png')

   # Compute percent difference between set and composite set
   da_plot_merge.loc[:,'Composite',:,:] = 100 * (da_plot_merge.loc[:,'Composite',:,:] / da_plot_merge.loc[:,obs_dataset,:,:])
   da_plot_merge.loc[:,comp_set,:,:]   = 100 * (da_plot_merge.loc[:,comp_set,:,:] / da_plot_merge.loc[:,obs_dataset,:,:])

   # Plot after dropping Composite label from dataset
   cmap_col = 'bwr'
   if(time_period == 'Annual'):
      output.write('Average % difference between ' + obs_dataset +  ' ' + comp_set + ' set for ' + \
                   var  + ' ' + str(round(np.nanmean(da_plot_merge.sel(Set=[comp_set]).values),2)) + '\n')
      output.write('Average % difference between ' + obs_dataset + ' Composite set for ' + \
                   var + ' '  + str(round(np.nanmean(da_plot_merge.sel(Set=['Composite']).values),2)) + '\n')
      output.write('Absolute average % difference between ' + obs_dataset +  ' ' + comp_set + ' set for ' + \
                   var  + ' ' + str(round(np.nanmean(np.absolute(da_plot_merge.sel(Set=[comp_set]).values)),2)) + '\n')
      output.write('Absolute average % difference between ' + obs_dataset + ' Composite set for ' + \
                   var + ' '  + str(round(np.nanmean(np.absolute(da_plot_merge.sel(Set=['Composite']).values)),2)) + '\n')
      output.close()
      facet_plot_US(da_plot_merge.sel(Set=[comp_set, 'Composite']), subplot_titles='', colplot='Set', colwrap=2, \
                    cmap_col=cmap_col, cbar_label='% difference', fig_wt=5*2, fig_ht=8, \
                    fig_extent=fig_extent, show_states=True, fname=fname_abb+'_'+var+'_Model_vs_'+obs_dataset+'_'+comp_set+'_per_diff.png')
   elif(time_period == 'Monthly'):
      facet_grid_plot_US(da_plot_merge.sel(Set=[comp_set, 'Composite']), 
                         colplot='Set', rowplot='month', \
                         cmap_col=cmap_col, cbar_label='% difference', fig_wt=5*2+0.3, fig_ht=5*(len(sum_mon))+0.7, \
                         fig_extent=fig_extent, show_states=True, fname=fname_abb+'_'+var+'_Model_vs_'+obs_dataset+'_'+comp_set+'_per_diff.png')

#----------------------------------------------------------
# Make plot comparing Composite, Set1, Set2, and Set3 to observations
def plot_model_obs_flux_3sets(da_plot_merge, var, time_period, fname_abb, obs_dataset):

   if(obs_dataset == 'FluxCom'):
      # Read FluxCom data, clip to Midwest region, and estimate mean annual
      obs_da_plot = read_clip_FluxCom_data(var, time_period, fname_abb, obs_dataset)
   if(obs_dataset == 'Madani_et_al'):
      # Read Madani et al data, clip to Midwest region, and estimate mean annual
      obs_da_plot = read_clip_Madani_et_al_data(var, time_period, fname_abb, obs_dataset)
   if(obs_dataset == 'MODIS'):
      # Read MOD17A2H data and estimate mean annual
      obs_da_plot = read_MODIS_data(var, time_period, fname_abb, obs_dataset)

   # Rename dataarray
   da_plot_merge = da_plot_merge.rename(var)

   da_plot_merge = xr.merge([obs_da_plot, da_plot_merge.sel(Set=['Composite','Set1','Set2','Set3'], variable=var)])

   da_plot_merge = da_plot_merge.to_array()

   # Create facet plot showing results for various sets in different columns
   cmap_col = 'jet'
   if(time_period == 'Annual'):
      facet_plot_US(da_plot_merge.sel(Set=[obs_dataset,'Composite','Set1','Set2','Set3']), \
                    subplot_titles='', colplot='Set', colwrap=5, \
                    cmap_col=cmap_col, cbar_label=myDict_labels[time_period][var], fig_wt=5*5, fig_ht=8, \
                    fig_extent=fig_extent, show_states=True, fname=fname_abb+'_'+var+'_Model_vs_'+obs_dataset+'_3sets.png')
   elif(time_period == 'Monthly'):
      facet_grid_plot_US(da_plot_merge.sel(Set=[obs_dataset,'Composite','Set1','Set2','Set3']),
                         colplot='Set', rowplot='month', \
                         cmap_col=cmap_col, cbar_label=myDict_labels[time_period][var], fig_wt=5*5+0.3, fig_ht=5*(len(sum_mon))+0.7, \
                         fig_extent=fig_extent, show_states=True, fname=fname_abb+'_'+var+'_Model_vs_'+obs_dataset+'_3sets.png')

   # Compute difference between set and composite set
   da_plot_merge.loc[:,'Composite',:,:] = da_plot_merge.loc[:,'Composite',:,:] - da_plot_merge.loc[:,obs_dataset,:,:]
   da_plot_merge.loc[:,'Set1',:,:] = da_plot_merge.loc[:,'Set1',:,:] - da_plot_merge.loc[:,obs_dataset,:,:]
   da_plot_merge.loc[:,'Set2',:,:] = da_plot_merge.loc[:,'Set2',:,:] - da_plot_merge.loc[:,obs_dataset,:,:]
   da_plot_merge.loc[:,'Set3',:,:] = da_plot_merge.loc[:,'Set3',:,:] - da_plot_merge.loc[:,obs_dataset,:,:]

   # Plot after dropping observations label from dataset
   cmap_col = 'bwr'
   if(time_period == 'Annual'):
      output = open('../figures/' + obs_dataset + '_stats_3sets.txt','w')
      output.write('Average difference between ' + obs_dataset + ' Composite set for ' + \
                   var  + ' ' + str(round(np.nanmean(da_plot_merge.sel(Set=['Composite']).values),2)) + '\n')
      output.write('Average difference between ' + obs_dataset + ' Set1 set for ' + \
                   var  + ' ' + str(round(np.nanmean(da_plot_merge.sel(Set=['Set1']).values),2)) + '\n')
      output.write('Average difference between ' + obs_dataset + ' Set2 set for ' + \
                   var  + ' ' + str(round(np.nanmean(da_plot_merge.sel(Set=['Set2']).values),2)) + '\n')
      output.write('Average difference between ' + obs_dataset + ' Set3 set for ' + \
                   var  + ' ' + str(round(np.nanmean(da_plot_merge.sel(Set=['Set3']).values),2)) + '\n')
      facet_plot_US(da_plot_merge.sel(Set=['Composite','Set1','Set2','Set3']), \
                    subplot_titles='', colplot='Set', colwrap=4, \
                    cmap_col=cmap_col, cbar_label=myDict_labels[time_period][var], fig_wt=5*4, fig_ht=8, \
                    fig_extent=fig_extent, show_states=True, fname=fname_abb+'_'+var+'_Model_vs_'+obs_dataset+'_3sets_diff.png')
   elif(time_period == 'Monthly'):
      facet_grid_plot_US(da_plot_merge.sel(Set=['Composite','Set1','Set2','Set3']), 
                         colplot='Set', rowplot='month', \
                         cmap_col=cmap_col, cbar_label=myDict_labels[time_period][var], fig_wt=5*4+0.3, fig_ht=5*(len(sum_mon))+0.7, \
                         fig_extent=fig_extent, show_states=True, fname=fname_abb+'_'+var+'_Model_vs_'+obs_dataset+'_3sets_diff.png')

   # Compute percent difference between set and composite set
   da_plot_merge.loc[:,'Composite',:,:] = 100 * (da_plot_merge.loc[:,'Composite',:,:] / da_plot_merge.loc[:,obs_dataset,:,:])
   da_plot_merge.loc[:,'Set1',:,:] = 100 * (da_plot_merge.loc[:,'Set1',:,:] / da_plot_merge.loc[:,obs_dataset,:,:])
   da_plot_merge.loc[:,'Set2',:,:] = 100 * (da_plot_merge.loc[:,'Set2',:,:] / da_plot_merge.loc[:,obs_dataset,:,:])
   da_plot_merge.loc[:,'Set3',:,:] = 100 * (da_plot_merge.loc[:,'Set3',:,:] / da_plot_merge.loc[:,obs_dataset,:,:])

   # Plot after dropping observations from dataset
   cmap_col = 'bwr'
   if(time_period == 'Annual'):
      output.write('Average % difference between ' + obs_dataset + ' Composite set for ' + \
                   var + ' '  + str(round(np.nanmean(da_plot_merge.sel(Set=['Composite']).values),2)) + '\n')
      output.write('Average % difference between ' + obs_dataset + ' Set1 set for ' + \
                   var + ' '  + str(round(np.nanmean(da_plot_merge.sel(Set=['Set1']).values),2)) + '\n')
      output.write('Average % difference between ' + obs_dataset + ' Set2 set for ' + \
                   var + ' '  + str(round(np.nanmean(da_plot_merge.sel(Set=['Set2']).values),2)) + '\n')
      output.write('Average % difference between ' + obs_dataset + ' Set3 set for ' + \
                   var + ' '  + str(round(np.nanmean(da_plot_merge.sel(Set=['Set3']).values),2)) + '\n')
      output.write('Absolute average % difference between ' + obs_dataset + ' Composite set for ' + \
                   var + ' '  + str(round(np.nanmean(np.absolute(da_plot_merge.sel(Set=['Composite']).values)),2)) + '\n')
      output.write('Absolute average % difference between ' + obs_dataset + ' Set1 set for ' + \
                   var + ' '  + str(round(np.nanmean(np.absolute(da_plot_merge.sel(Set=['Set1']).values)),2)) + '\n')
      output.write('Absolute average % difference between ' + obs_dataset + ' Set2 set for ' + \
                   var + ' '  + str(round(np.nanmean(np.absolute(da_plot_merge.sel(Set=['Set2']).values)),2)) + '\n')
      output.write('Absolute average % difference between ' + obs_dataset + ' Set3 set for ' + \
                   var + ' '  + str(round(np.nanmean(np.absolute(da_plot_merge.sel(Set=['Set3']).values)),2)) + '\n')
      output.close()
      facet_plot_US(da_plot_merge.sel(Set=['Composite','Set1','Set2','Set3']), subplot_titles='', colplot='Set', colwrap=4, \
                    cmap_col=cmap_col, cbar_label='% difference', fig_wt=5*4, fig_ht=8, \
                    fig_extent=fig_extent, show_states=True, fname=fname_abb+'_'+var+'_Model_vs_'+obs_dataset+'_3sets_per_diff.png')
   elif(time_period == 'Monthly'):
      facet_grid_plot_US(da_plot_merge.sel(Set=['Composite','Set1','Set2','Set3']), 
                         colplot='Set', rowplot='month', \
                         cmap_col=cmap_col, cbar_label='% difference', fig_wt=5*4+0.3, fig_ht=5*(len(sum_mon))+0.7, \
                         fig_extent=fig_extent, show_states=True, fname=fname_abb+'_'+var+'_Model_vs_'+obs_dataset+'_3sets_per_diff.png')
