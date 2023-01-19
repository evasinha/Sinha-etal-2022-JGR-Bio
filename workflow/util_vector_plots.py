import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
from itertools import cycle
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.ticker import FormatStrFormatter
 
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
def bar_plot(site_data, ylabel, fname):

    # Change directory    
    os.chdir('../figures/')

    color = ['silver','mediumseagreen','palegreen','lightsalmon','lightskyblue','bisque']

    fig, axis = plt.subplots(1, 1, figsize=(14, 7))

    x_axis = np.arange(len(site_data))

    site_data[['Observed','Default','Composite','Set1','Set2','Set3']].plot.bar(rot = 0, color=color)

    plt.xticks(x_axis, site_data.SiteID)
    plt.ylabel(ylabel)
    plt.legend(loc='upper left', bbox_to_anchor=(0.0, -0.05), ncol=6)

    plt.savefig(fname, bbox_inches='tight')

    plt.close(fig=None)
    
    # Change directory    
    os.chdir('../workflow/')

# -----------------------------------------------------------
# Make spatial plot of xarray dataset showing boundaries of lakes and states
def bar_subplots(site_data_1, site_data_2, title_1, title_2, ylabel, fname):

    # Change directory    
    os.chdir('../figures/')

    #color = ['silver','mediumseagreen','palegreen','lightsalmon','lightskyblue','bisque']
    color = ['silver','mediumseagreen','palegreen']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7), sharey=True)

    x_axis = np.arange(len(site_data_1))

    #site_data_1[['Observed','Default','Composite','Set1','Set2','Set3']].plot.bar(ax=ax1, rot = 0, color=color)
    #site_data_2[['Observed','Default','Composite','Set1','Set2','Set3']].plot.bar(ax=ax2, rot = 0, color=color)
    site_data_1[['Observed','Default','Composite']].plot.bar(ax=ax1, rot = 0, color=color)
    site_data_2[['Observed','Default','Composite']].plot.bar(ax=ax2, rot = 0, color=color)

    ax1.set_xticklabels(site_data_1.SiteID)
    ax2.set_xticklabels(site_data_2.SiteID)
    ax1.set_ylabel(ylabel)

    handles, labels = ax1.get_legend_handles_labels()
    fig.legend(handles, labels, loc='center', bbox_to_anchor=(0.5, 0), ncol=6)

    ax1.get_legend().remove()
    ax2.get_legend().remove()

    ax1.set_title(title_1)
    ax2.set_title(title_2)

    plt.savefig(fname, bbox_inches='tight')

    plt.close(fig=None)
    
    # Change directory    
    os.chdir('../workflow/')

# -----------------------------------------------------------
# Make spatial plot of xarray dataset showing boundaries of lakes and states
def facet_grid_bar(site_data, ylabel, fname):

    # Change directory    
    os.chdir('../figures/')

    # Facet grid bar plot
    g = sns.catplot(data=site_data, x='SiteID', y='value', hue='variable', \
                    col='month', row='Crop', kind='bar', height=4, aspect=1.2, margin_titles=True)

    # Modify axis labels
    g.set_axis_labels('', ylabel)

    # Move legend to bottom
    sns.move_legend(g, 'lower center', bbox_to_anchor=(.5, 0.45), ncol=3, title=None, frameon=False)

    # Modify facet titles
    g.set_titles(col_template='{col_name}', row_template='{row_name}')

    # Rotate xtick labels
    for ax in g.axes.flat:
       for label in ax.get_xticklabels():
          label.set_rotation(90)

    plt.savefig(fname, bbox_inches='tight')

    plt.close(fig=None)
    
    # Change directory    
    os.chdir('../workflow/')

# ---------- function for estimating realtive root mean square error ----------
def rrmse(predictions, targets):
    rmse = np.sqrt(((predictions - targets) ** 2).mean())
    return rmse/np.sqrt((targets ** 2).mean())

# -----------------------------------------------------------
def annotate(data, **kws):
    pred1  = data.loc[data['variable'] == 'Default', 'value'].to_numpy()
    pred2  = data.loc[data['variable'] == 'Composite', 'value'].to_numpy()
    target = data.loc[data['variable'] == 'Observed', 'value'].to_numpy()
 
    rrmse1 = rrmse(pred1, target)
    rrmse2 = rrmse(pred2, target)
    ax = plt.gca()
    #ax.text(.05, .9, 'RRMSE={:.2f}'.format(rrmse1), transform=ax.transAxes, color='#ff7f0e', size='x-large')
    #ax.text(.05, .8, 'RRMSE={:.2f}'.format(rrmse2), transform=ax.transAxes, color='#2ca02c', size='x-large')

    # Plot RRMSE as inset bar plot
    ax = plt.gca()
    axins = inset_axes(ax,  width='15%', height='20%' ,loc='upper left', borderpad=2.1)
    axins.bar(['Default', 'Composite'], [rrmse1, rrmse2], color=['forestgreen','palegreen'])

    # Remove xaxis tick lables and tick marks
    axins.set_xticks([])

    # Format y axis numbers
    axins.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

    # Invisible spines
    axins.spines['right'].set_visible(False)
    axins.spines['top'].set_visible(False)

# -----------------------------------------------------------
# Make spatial plot of xarray dataset showing boundaries of lakes and states
def facet_grid_line(site_data, ylabel, xtick_labels, fname):

    # Change directory    
    os.chdir('../figures/')

    col_palette = {'Observed':'silver', 'Default':'mediumseagreen', 'Composite':'palegreen'}

    # Facet grid bar plot
    g = sns.catplot(data=site_data, x='month', y='value', hue='variable', \
                    col='SiteID', row='Crop', kind='point', palette=col_palette, height=4, aspect=1.0, margin_titles=True)

    # Add RRMSE as annotation
    g.map_dataframe(annotate)

    # Modify axis labels
    g.set_axis_labels('', ylabel)

    # Only keep one yaxis label
    g.axes[0,0].set_ylabel('')
    g.axes[1,0].set_ylabel(ylabel, loc='bottom')

    # Move legend to bottom
    sns.move_legend(g, 'lower center', bbox_to_anchor=(.5, -0.05), ncol=3, title=None, frameon=False)

    # Modify facet titles
    g.set_titles(col_template='{col_name}', row_template='{row_name}')

    # Modify xaxis labels
    g.set_xticklabels(xtick_labels)

    # Rotate xtick labels
    #for ax in g.axes.flat:
    #   for label in ax.get_xticklabels():
    #      label.set_rotation(90)

    # Return first element of the string
    def update_xticks(x):
       return(x[0])

    for ax in g.axes.flat:
       labels = ax.get_xticklabels() # get x labels
       for i, label in enumerate(labels):
          labels[i] = update_xticks(label.get_text())
       ax.set_xticklabels(labels)


    plt.savefig(fname, bbox_inches='tight')

    plt.close(fig=None)
    
    # Change directory    
    os.chdir('../workflow/')

# -----------------------------------------------------------
# Plot time series
def plot_ts_annual(da, ylabel, key, fname, sel_pft):

   # Change directory    
   os.chdir('../figures/')

   cycol = cycle('bgrcmk')

   fig, ax = plt.subplots(figsize=(11, 8.5))

   for yr in np.unique(da['time.year']):
      da_plot = da.sel(time = da.time.dt.year.isin([yr]))
      plt.plot(da_plot.time.dt.dayofyear, da_plot, color=next(cycol), label=str(yr))

   plt.ylabel(ylabel)    
   plt.legend(loc='upper left')
 
   # Define the month format
   #plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2))
   #plt.gca().xaxis.set_major_formatter(DateFormatter('%d-%b'))

   ax.text(0.02, 1.02, sel_pft.capitalize(), color='black', transform=ax.transAxes, fontsize=18, bbox=dict(facecolor='white', edgecolor='white'))
   ax.text(0.85, 1.02, key,  color='black', transform=ax.transAxes, fontsize=18, bbox=dict(facecolor='white', edgecolor='white'))

   plt.savefig(key + '_' + fname + '_' +  sel_pft + '.pdf', bbox_inches='tight')

   plt.close(fig=None)

   # Change directory
   os.chdir('../workflow/')

# -----------------------------------------------------------
# Plot time series with table at bottom
def plot_ts_table_annual(da, ds_plantday, ds_harvestday, ylabel, key, fname, sel_pft):

   # Change directory    
   os.chdir('../figures/')

   cycol = cycle('bgrcmk')

   fig, ax = plt.subplots(figsize=(11, 8.5))

   for yr in np.unique(da['time.year']):
      da_plot = da.sel(time = str(yr))
      plt.plot(da_plot.time.dt.dayofyear, da_plot, color=next(cycol), label=str(yr))

   plt.ylabel(ylabel)    
   plt.legend(loc='upper left')
 
   # Define the month format
   plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2))
   plt.gca().xaxis.set_major_formatter(DateFormatter('%d-%b'))

   # Add a table at the bottom of the axes
   plantday_data   = ds_plantday.sel(pft=sel_pft).values
   harvestday_data = ds_harvestday.sel(pft=sel_pft).values
   the_table = plt.table(cellText  = [np.transpose(plantday_data), np.transpose(harvestday_data)],
                         rowLabels = ['Planting day', 'Harvest day'],
                         colLabels = ds_plantday.time.dt.year.values,
                         loc       = 'bottom',
                         bbox = [0, -0.3, 1.0, 0.2])

   ax.text(0.02, 1.02, sel_pft.capitalize(), color='black', transform=ax.transAxes, fontsize=18, bbox=dict(facecolor='white', edgecolor='white'))
   ax.text(0.85, 1.02, key,  color='black', transform=ax.transAxes, fontsize=18, bbox=dict(facecolor='white', edgecolor='white'))

   plt.savefig(key + '_' + fname + '_' +  sel_pft + '.pdf', bbox_inches='tight')

   plt.close(fig=None)

   # Change directory
   os.chdir('../workflow/')

# -----------------------------------------------------------
# Make facet line plot of the xarray dataset
def xarray_facet_line_plot(ds_plot, facet_col, xlabel, ylabel, fname, xmin, xmax, hue_var=None, col_wrap=None, xvline=None, sharey=True):

   # Change directory    
   os.chdir('../figures/')

   fg = ds_plot.plot(col        = facet_col, 
                     hue        = hue_var,
                     col_wrap   = col_wrap, 
                     xlim       = (xmin,xmax), 
                     sharey     = sharey,
                     aspect     = 1.5,
                     add_legend = False)

   # https://cduvallet.github.io/posts/2018/11/facetgrid-ylabel-access
   # Iterate thorugh each axis
   for ax in fg.axes.flat:
      # Modify column title
      if ax.get_title():
         subplot_title = ax.get_title().split('=')[1]
         subplot_title = subplot_title.strip()
         if (facet_col in ['pft','cft']):
            ax.set_title(pft_names[subplot_title], fontsize=15)
            #ax.set_title(subplot_title, fontsize=15)
         else:
            ax.set_title(subplot_title, fontsize=15)

      if(xvline is not None):
         # Add a vertical line at specified x
         ax.axvline(x=xvline, color='red', linestyle=':')

   # Add axis labels
   fg.set_axis_labels(x_var=xlabel, y_var=ylabel)

   # Move legend to bottom
   #fg.add_legend(ncol=2, bbox_to_anchor=(0.5, -0.01))

   plt.savefig(fname, bbox_inches='tight')

   plt.close(fig=None)
    
   # Change directory    
   os.chdir('../workflow/')
    
# -----------------------------------------------------------
# Make facet grid line plot for the xarray dataset
def xarray_facet_grid_line_plot(ds_plot, facet_row, facet_col, xvline, xlabel, ylabel, fname):

   # Change directory    
   os.chdir('../figures/')

   fg = ds_plot.plot(row=facet_row, col=facet_col, sharey='row')

   # https://cduvallet.github.io/posts/2018/11/facetgrid-ylabel-access
   # Iterate thorugh each axis
   for ax in fg.axes.flat:

      # Modify column title
      if ax.get_title():
         tmp = ax.get_title().split('=')[1]
         ax.set_title(tmp, fontsize=15)

      # Modify right ylabel (row title) more human-readable and larger
      # Only the 2nd and 4th axes have something in ax.texts
      if ax.texts:
         # This contains the right ylabel text
         txt = ax.texts[0]
         ax.text(txt.get_unitless_position()[0], txt.get_unitless_position()[1],
                 txt.get_text().split('=')[1],
                 transform = ax.transAxes,
                 va        = 'center',
                 fontsize  = 15,
                 rotation  = -90)
         # Remove the original text
         ax.texts[0].remove()

      # Add a vertical line at specified x
      ax.axvline(x=xvline, color='red', linestyle=':')

   # Add axis labels
   fg.set_axis_labels(x_var=xlabel, y_var=ylabel)

   # Define x ticks
   plt.xticks(np.arange(min(ds_plot.time), max(ds_plot.time)+1, 200))

   plt.savefig(fname, bbox_inches='tight')

   plt.close(fig=None)
    
   # Change directory    
   os.chdir('../workflow/')
    
# -----------------------------------------------------------
