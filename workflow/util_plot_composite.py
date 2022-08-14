
__author__ = 'Eva Sinha'
__email__  = 'eva.sinha@pnnl.gov'

from create_composite_grid import *
from util_spatial_plots import *
from util_myDict_labels import *
from plot_obs_yield import *
from util_estimate_dataset_stats import *
from plot_model_obs_flux import *

#----------------------------------------------------------
def create_plot_composite(da_plot_merge, var, time_period, fname_abb):
   """ Create a composite grid and plot composite grid and difference between composite grid and original set
   """
   # Create a composite grid by merging certain regions from each set
   if(time_period == 'Annual'):
      composite_grid        = create_composite_grid(da_plot_merge, var)
      no_rot_composite_grid = create_no_rot_composite_grid(da_plot_merge, var)
   elif(time_period == 'Monthly'):
      composite_grid        = create_composite_grid_monthly(da_plot_merge, var)
      no_rot_composite_grid = create_no_rot_composite_grid_monthly(da_plot_merge, var)

   # Merge composite grids
   da_plot_merge = xr.merge([da_plot_merge, composite_grid])
   da_plot_merge = xr.merge([da_plot_merge, no_rot_composite_grid])

   da_plot_merge = da_plot_merge.to_array()

   if (var == 'GPP'):

      obs_datasets = ['FluxCom', 'Madani_et_al']

      for obs_dataset in obs_datasets:
         # Make plot comparing composite and default set to observations
         plot_model_obs_flux(da_plot_merge, var, time_period, fname_abb, obs_dataset, comp_set='Default')
         plot_model_obs_flux(da_plot_merge, var, time_period, fname_abb, obs_dataset, comp_set='No_rot_Composite')

   if (var == 'NPP'):

      obs_datasets = ['Monfreda_et_al']

      for obs_dataset in obs_datasets:
         # Make plot comparing composite and default set to observations
         plot_model_obs_flux(da_plot_merge, var, time_period, fname_abb, obs_dataset, comp_set='Default')
         plot_model_obs_flux(da_plot_merge, var, time_period, fname_abb, obs_dataset, comp_set='No_rot_Composite')

   # Drop the Default set
   da_plot_merge = da_plot_merge.drop_sel(Set = 'Default')
   da_plot_merge = da_plot_merge.drop_sel(Set = 'No_rot_Composite')
   da_plot_merge = da_plot_merge.drop_sel(Set = 'Set1_no_rot')
   da_plot_merge = da_plot_merge.drop_sel(Set = 'Set2_no_rot')
   da_plot_merge = da_plot_merge.drop_sel(Set = 'Set3_no_rot')

   # Create facet plot showing results for various sets in different columns
   cmap_col = 'jet'
   if(time_period == 'Annual'):
      facet_plot_US(da_plot_merge, subplot_titles='', colplot='Set', colwrap=len(da_plot_merge.Set), \
                    cmap_col=cmap_col, cbar_label=myDict_labels[time_period][var], fig_wt=4.9*(len(da_plot_merge.Set))+0.3, fig_ht=4.9+0.2, \
                    fig_extent=fig_extent, show_states=True, fname=fname_abb+'_'+var+'.png')

      xr_plot_US(da_plot_merge.sel(Set='Composite'), plot_title='Composite', \
                 cmap_col=cmap_col, cbar_label=myDict_labels[time_period][var], fig_wt=6.0, fig_ht=6.0, \
                 fig_extent=fig_extent, show_states=True, fname=fname_abb+'_'+var+'_Composite.png')
   elif(time_period == 'Monthly'):
      facet_grid_plot_US(da_plot_merge, colplot='Set', rowplot='month', \
                         cmap_col=cmap_col, cbar_label=myDict_labels[time_period][var], \
                         fig_wt=5*(len(da_plot_merge.Set))+0.3, fig_ht=5*(len(sum_mon))+0.7, \
                         fig_extent=fig_extent, show_states=True, fname=fname_abb+'_'+var+'.png')

      facet_plot_US(da_plot_merge.sel(Set='Composite'), subplot_titles='', colplot='month', colwrap=1, \
                    cmap_col=cmap_col, cbar_label=myDict_labels[time_period][var], fig_wt=4.9+0.3, fig_ht=4.9*(len(sum_mon))+0.2, \
                    fig_extent=fig_extent, show_states=True, fname=fname_abb+'_'+var+'_Composite.png', main_title='Composite')

   # Compute difference between set and composite set
   da_plot_merge.loc[:,'Set1',:,:] = da_plot_merge.loc[:,'Set1',:,:] - da_plot_merge.loc[:,'Composite',:,:]
   da_plot_merge.loc[:,'Set2',:,:] = da_plot_merge.loc[:,'Set2',:,:] - da_plot_merge.loc[:,'Composite',:,:]
   da_plot_merge.loc[:,'Set3',:,:] = da_plot_merge.loc[:,'Set3',:,:] - da_plot_merge.loc[:,'Composite',:,:]

   # Plot after dropping Composite label from dataset
   cmap_col = 'bwr'
   if(time_period == 'Annual'):
      facet_plot_US(da_plot_merge.drop_sel(Set = 'Composite'), subplot_titles='', colplot='Set', colwrap=len(da_plot_merge.Set)-1, \
                    cmap_col=cmap_col, cbar_label=myDict_labels[time_period][var], fig_wt=4.9*(len(da_plot_merge.Set)-1)+0.3, fig_ht=4.9+0.2, \
                    fig_extent=fig_extent, show_states=True, fname=fname_abb+'_'+var+'_diff.png')
   elif(time_period == 'Monthly'):
      facet_grid_plot_US(da_plot_merge.drop_sel(Set = 'Composite'), colplot='Set', rowplot='month', \
                         cmap_col=cmap_col, cbar_label=myDict_labels[time_period][var], \
                         fig_wt=5*(len(da_plot_merge.Set)-1)+0.3, fig_ht=5*(len(sum_mon))+0.7, \
                         fig_extent=fig_extent, show_states=True, fname=fname_abb+'_'+var+'_diff.png')

   # Compute percent difference between set and composite set
   da_plot_merge.loc[:,'Set1',:,:] = 100 * (da_plot_merge.loc[:,'Set1',:,:] / da_plot_merge.loc[:,'Composite',:,:])
   da_plot_merge.loc[:,'Set2',:,:] = 100 * (da_plot_merge.loc[:,'Set2',:,:] / da_plot_merge.loc[:,'Composite',:,:])
   da_plot_merge.loc[:,'Set3',:,:] = 100 * (da_plot_merge.loc[:,'Set3',:,:] / da_plot_merge.loc[:,'Composite',:,:])

   # Plot after dropping Composite label from dataset
   cmap_col = 'bwr'
   if(time_period == 'Annual'):
      facet_plot_US(da_plot_merge.drop_sel(Set = 'Composite'), subplot_titles='', colplot='Set', colwrap=len(da_plot_merge.Set)-1, \
                    cmap_col=cmap_col, cbar_label='% difference', fig_wt=4.9*(len(da_plot_merge.Set)-1)+0.3, fig_ht=4.9+0.2, \
                    fig_extent=fig_extent, show_states=True, fname=fname_abb+'_'+var+'_per_diff.png')
   elif(time_period == 'Monthly'):
      facet_grid_plot_US(da_plot_merge.drop_sel(Set = 'Composite'), colplot='Set', rowplot='month', \
                         cmap_col=cmap_col, cbar_label='% difference', \
                         fig_wt=5*(len(da_plot_merge.Set)-1)+0.3, fig_ht=5*(len(sum_mon))+0.7, \
                         fig_extent=fig_extent, show_states=True, fname=fname_abb+'_'+var+'_per_diff.png')

#----------------------------------------------------------
def create_plot_regridded_composite(da_plot_merge, var, plot_row, time_period, fname_abb):
   """ Create a composite grid and plot composite grid and difference between composite grid and original set
   """
   # Create a composite grid by merging certain regions from each set
   composite_grid        = create_regridded_composite_grid(da_plot_merge, var, plot_row)
   no_rot_composite_grid = create_no_rot_regridded_composite_grid(da_plot_merge, var, plot_row)
   da_plot_merge = xr.merge([da_plot_merge, composite_grid])

   da_plot_merge = da_plot_merge.to_array()

   # Drop the Default set
   da_plot_merge = da_plot_merge.drop_sel(Set = 'Default')
   da_plot_merge = da_plot_merge.drop_sel(Set = 'Set1_no_rot')
   da_plot_merge = da_plot_merge.drop_sel(Set = 'Set2_no_rot')
   da_plot_merge = da_plot_merge.drop_sel(Set = 'Set3_no_rot')

   # Create facet grid plot showing results for various sets in different columns and pft in different rows
   cmap_col = 'jet'
   facet_grid_plot_US(da_plot_merge, colplot='Set', rowplot=plot_row, \
                      cmap_col=cmap_col, cbar_label=myDict_labels[time_period][var], \
                      fig_wt=5*(len(da_plot_merge.Set))+0.3, fig_ht=5*2+1.0, \
                      fig_extent=fig_extent, show_states=True, fname=fname_abb+'_'+var+'_cft.png')

   facet_plot_US(da_plot_merge.sel(Set='Composite'), subplot_titles='', colplot=plot_row, colwrap=1, \
                 cmap_col=cmap_col, cbar_label=myDict_labels[time_period][var], fig_wt=4.9+0.3, fig_ht=4.9*2+0.2, \
                 fig_extent=fig_extent, show_states=True, fname=fname_abb+'_'+var+'_cft_Composite.png', main_title='Composite')

   # Compute difference between set and composite set
   da_plot_merge.loc[:,'Set1',:,:,:] = da_plot_merge.loc[:,'Set1',:,:,:] - da_plot_merge.loc[:,'Composite',:,:,:]
   da_plot_merge.loc[:,'Set2',:,:,:] = da_plot_merge.loc[:,'Set2',:,:,:] - da_plot_merge.loc[:,'Composite',:,:,:]
   da_plot_merge.loc[:,'Set3',:,:,:] = da_plot_merge.loc[:,'Set3',:,:,:] - da_plot_merge.loc[:,'Composite',:,:,:]

   # Plot after dropping Composite label from dataset
   cmap_col = 'bwr'
   facet_grid_plot_US(da_plot_merge.drop_sel(Set = 'Composite'), colplot='Set', rowplot=plot_row, \
                      cmap_col=cmap_col, cbar_label=myDict_labels[time_period][var], \
                      fig_wt=5*(len(da_plot_merge.Set)-1)+0.3, fig_ht=5*2+1.0, \
                      fig_extent=fig_extent, show_states=True, fname=fname_abb+'_'+var+'_cft_diff.png')

   # Compute percent difference between set and composite set
   da_plot_merge.loc[:,'Set1',:,:,:] = 100 * (da_plot_merge.loc[:,'Set1',:,:,:] / da_plot_merge.loc[:,'Composite',:,:,:])
   da_plot_merge.loc[:,'Set2',:,:,:] = 100 * (da_plot_merge.loc[:,'Set2',:,:,:] / da_plot_merge.loc[:,'Composite',:,:,:])
   da_plot_merge.loc[:,'Set3',:,:,:] = 100 * (da_plot_merge.loc[:,'Set3',:,:,:] / da_plot_merge.loc[:,'Composite',:,:,:])

   # Plot after dropping Composite label from dataset
   cmap_col = 'bwr'
   facet_grid_plot_US(da_plot_merge.drop_sel(Set = 'Composite'), colplot='Set', rowplot=plot_row, \
                      cmap_col=cmap_col, cbar_label='% difference', \
                      fig_wt=5*(len(da_plot_merge.Set)-1)+0.3, fig_ht=5*2+1.0, \
                      fig_extent=fig_extent, show_states=True, fname=fname_abb+'_'+var+'_cft_per_diff.png')

   if(var == 'DMYIELD'):

      obs_fpath      = '/qfs/people/sinh210/wrk/E3SM_SFA/ELM-Bioenergy/obsdata/USDA_NASS/'
      geo_county =  merge_county_shp_USDA_yield(obs_fpath)

      # Write xarray to a new NetCDF file
      os.chdir('composite_grids')
      composite_grid.to_netcdf(path='yield_Composite.nc', mode='w')
      no_rot_composite_grid.to_netcdf(path='yield_No_rot_Composite.nc', mode='w')
      os.chdir('../')

      #plot_obs_model_yield(composite_grid, geo_county)

      cmap_col = 'jet'
      plot_xa_gpd(composite_grid, geo_county, \
                  cmap_col=cmap_col, cbar_label=myDict_labels[time_period][var], \
                  fig_wt=8*2, fig_ht=11, fname='Model_obs_yield_Composite.png')
      plot_xa_gpd(no_rot_composite_grid, geo_county, \
                  cmap_col=cmap_col, cbar_label=myDict_labels[time_period][var], \
                  fig_wt=8*2, fig_ht=11, fname='Model_obs_yield_No_rot_Composite.png')

   if(var in ['GPP','DMYIELD']):
      # Merge with and without rotation composite grid
      da_plot_merge = xr.merge([composite_grid, no_rot_composite_grid])
      da_plot_merge = da_plot_merge.to_array()

      # Create facet grid plot showing results for various sets in different columns and pft in different rows
      cmap_col = 'jet'
      facet_grid_plot_US(da_plot_merge, colplot='Set', rowplot=plot_row, \
                         cmap_col=cmap_col, cbar_label=myDict_labels[time_period][var], \
                         fig_wt=5*(len(da_plot_merge.Set))+0.3, fig_ht=5*2+1.0, \
                         fig_extent=fig_extent, show_states=True, fname=fname_abb+'_'+var+'_cft_rot_compare.png')

      # Compute difference between with and without rotation composite set
      da_plot_diff = da_plot_merge.loc[:,'Composite',:,:,:] - da_plot_merge.loc[:,'No_rot_Composite',:,:,:]

      cmap_col = 'bwr'
      facet_plot_US(da_plot_diff, subplot_titles='', colplot=plot_row, colwrap=1, \
                    cmap_col=cmap_col, cbar_label=myDict_labels[time_period][var], fig_wt=4.9+0.3, fig_ht=4.9*2+0.2, \
                    fig_extent=fig_extent, show_states=True, fname=fname_abb+'_'+var+'_cft_rot_diff.png', main_title='Difference')
