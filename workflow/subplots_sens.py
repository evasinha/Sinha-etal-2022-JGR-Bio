#!/usr/bin/env python

import os
import numpy as np
import pickle as pk
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
from optparse import OptionParser

import utils as mu

parser = OptionParser();

parser.add_option("--site", dest="site", default="", \
                  help="Site ID")
parser.add_option("--crop", dest="crop", default="", \
                  help="Modeled crop name")

(options, args) = parser.parse_args()

#----------------------------------------------------------

############################################################
############################################################
############################################################
# should be run after elm_fates/run_wibcs.py
############################################################
############################################################
############################################################

def subplot_sens(ax,sensdata,pars,cases,vis="bar",reverse=False,par_labels=[],case_labels=[],colors=[],ncol=4,grid_show=True,xlbl='',legend_show=2,legend_size=10,xdatatick=[],showplot=False,topsens=[], lbl_size=18, yoffset=0.1, QoI='',xtick_labels=True):
    """Plots sensitivity for multiple observables"""
    
    ncases=sensdata.shape[0]
    npar=sensdata.shape[1]

    wd=0.6
    ylbl = QoI + ' - Sensitivity'


    assert set(pars) <= set(range(npar))
    assert set(cases) <= set(range(ncases))

    # Set up the figure
    # TODO need to scale figure size according to the expected amount of legends

    #xticklabel_size=int(400/ncases)
    xticklabel_size=18
    yticklabel_size=18


#    fig = plt.figure(figsize=(20,13))
#    fig.add_axes([0.1,0.2+yoffset,0.8,0.6-yoffset])
    #########

    # Default parameter names
    if (par_labels==[]):
        for i in range(npar):
            par_labels.append(('par_'+str(i+1)))
    # Default case names
    if (case_labels==[]):
        for i in range(ncases):
            case_labels.append(('case_'+str(i+1)))


    if(reverse):
        tmp=par_labels
        par_labels=case_labels
        case_labels=tmp
        tmp=pars
        pars=cases
        cases=tmp
        sensdata=sensdata.transpose()
    ##############################################################################

    npar_=len(pars)
    ncases_=len(cases)

    sensind = np.argsort(np.average(sensdata, axis=0))[::-1]

    if topsens==[]:
        topsens=npar_

    # Create colors list
    if colors == []:
        colors_ = fuc.set_colors(topsens)
        colors_.extend(fuc.set_colors(npar_-topsens))
        colors = [0.0 for i in range(npar_)]
        for i in range(npar_):
            colors[sensind[i]]=colors_[i]

    case_labels_=[]
    for i in range(ncases_):
        case_labels_.append(case_labels[cases[i]])

    if xdatatick==[]:
        xflag=False
        xdatatick=np.array(range(1,ncases_+1))
        sc=1.
    else:
        xflag=True
        sc=float(xdatatick[-1]-xdatatick[0])/ncases_

    if (vis=="graph"):
        for i in range(npar_):
            ax.plot(xdatatick_,sensdata[cases,i], '-o',color=colors[pars[i]], label=par_labels[pars[i]])
    elif (vis=="bar"):
        curr=np.zeros((ncases_))
        #print pars,colors
        for i in range(npar_):
            ax.bar(xdatatick,sensdata[cases,i], width=wd*sc,color=colors[pars[i]], bottom=curr, label=par_labels[pars[i]])
            curr=sensdata[cases,i]+curr
        if not xflag:
            if ncases>9:
                #xticks(np.array(range(1,ncases_+1)),case_labels_,rotation='vertical')
                ax.set_xticklabels(np.arange(1,ncases_+1,60),rotation='horizontal')
            else:
                ax.set_xticklabels(np.array(range(1,ncases_+1)),case_labels_,rotation='horizontal')
        #xlim(xdatatick[0]-wd*sc/2.-0.1,xdatatick[-1]+wd*sc/2.+0.1)

        ax.set_xlim([0,365])

    ax.set_ylabel(ylbl,fontsize=lbl_size)
    ax.tick_params(axis='y', labelsize=yticklabel_size)

    maxsens=max(max(curr),1.0)
    ax.set_ylim([0,maxsens])
    handles,labels = ax.get_legend_handles_labels()
    handles = [ handles[i] for i in sensind[:topsens]]
    labels = [ labels[i] for i in sensind[:topsens]]
    if legend_show==1:
        ax.legend(handles,labels,fontsize=legend_size)
    elif (legend_show==2):
        if(xtick_labels):
            ax.legend(handles,labels,loc='upper left',bbox_to_anchor=(0.0, -0.1),fancybox=True, shadow=True,ncol=ncol,labelspacing=-0.1,fontsize=legend_size)
        else:
            ax.legend(handles,labels,loc='upper left',bbox_to_anchor=(0.0, 0.0),fancybox=True, shadow=True,ncol=ncol,labelspacing=-0.1,fontsize=legend_size)
    elif (legend_show==3):
        ax.legend(handles,labels,loc='upper left', bbox_to_anchor=(0.0, 1.2),fancybox=True, shadow=True,ncol=ncol,labelspacing=-0.1,fontsize=legend_size)
    elif (legend_show==4):
        ax.legend_ = None
        


    if not xflag:
        zed = [tick.label.set_fontsize(xticklabel_size) for tick in ax.xaxis.get_major_ticks()]

    ax.grid(grid_show)

    if showplot:
        show()

# ---------------------------------------------------------
os.chdir('../site_calib_outputs/')

results_all = pk.load(open(options.site + '_' + options.crop + '_' + 'results_all.pk', 'rb'))

nout = len(results_all)
dim = 12

myDict = {'GPP': 365, 'ER': 730, 'LE': 1095, 'H': 1460}

fig, ax = plt.subplots(nrows=len(myDict), ncols=1, sharex=True, sharey=False, figsize=(9, 5*len(myDict)), constrained_layout=True)

for ind, key in enumerate(myDict):

    ind_plot=np.arange(myDict[key]-365,myDict[key]) # change this to (0,365) for one variable, (365, 730) for two variables, and (730, 1095) when 3 variables

    pars = range(dim)
    nout_plot = len(ind_plot)
    cases = np.arange(nout_plot)

    pnames = mu.read_textlist('pnames.txt', dim)
    outnames = [str(j+1) for j in range(nout_plot)]

    all_totsens = np.zeros((nout_plot, dim))
    all_mainsens = np.zeros((nout_plot, dim))
    for i in range(nout_plot):
        iout = ind_plot[i]
        print("================================================================")
        print("Output %d / %d" % (iout + 1, nout))
        print("================================================================")
        if results_all[iout] is not None:
            #print(results_all[iout].keys())
            mindex = results_all[iout]['mindex']
            pccf = results_all[iout]['cfs']
            a, b = mu.encode_mindex(mindex)
            # for i, j in zip(a, b):
            #     print(i, j)

            mainsens, totsens, jointsens, mean, var = mu.pce_sens('LU',
                                                                  mindex,
                                                                  pccf,
                                                                  mv=True)

            all_totsens[i, :] = totsens
            all_mainsens[i, :] = mainsens

    np.savetxt(options.site + '_' + options.crop + '_' + 'allsens_main.dat', all_mainsens)
    np.savetxt(options.site + '_' + options.crop + '_' + 'allsens_tot.dat', all_totsens)
    np.savetxt(options.site + '_' + options.crop + '_' + 'allsens_main_ave.dat', np.mean(all_mainsens, axis=0))
    np.savetxt(options.site + '_' + options.crop + '_' + 'allsens_tot_ave.dat', np.mean(all_totsens, axis=0))
    #colors = ut.set_colors(22)
    cmap = plt.get_cmap('tab20')
    colors = np.array([cmap(j) for j in np.arange(dim)/(dim-1)])

    if (ind == len(myDict)-1):
        xtick_labels = True
    else:
        xtick_labels = False

    subplot_sens(ax[ind], all_mainsens, pars, cases, vis="bar",
                 reverse=False, par_labels=pnames, case_labels=outnames,
                 colors=colors, ncol=3, grid_show=False, xlbl='',
                 legend_show=2, legend_size=16, xdatatick=[],
                 showplot=False, topsens=8,
                 lbl_size=18, yoffset=0.1, QoI=key, xtick_labels=xtick_labels)

#ax[len(myDict)-1].legend(labels)
ax[0].text(0.02, 0.93, options.crop, color='black', transform=ax[0].transAxes, fontsize=18, bbox=dict(facecolor='white', edgecolor='white'))
ax[0].text(0.85, 0.93, options.site,  color='black', transform=ax[0].transAxes, fontsize=18, bbox=dict(facecolor='white', edgecolor='white'))

# Define the month format
ax[len(myDict)-1].xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax[len(myDict)-1].xaxis.set_major_formatter(DateFormatter('%d-%b'))

plt.savefig('../figures/' + options.site + '_' + options.crop + '_' + 'sens_main_all.png', bbox_inches='tight')
