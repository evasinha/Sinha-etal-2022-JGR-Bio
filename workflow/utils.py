#!/usr/bin/env python


import numpy as np
import sys
import os
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import matplotlib.animation as animation
from pylab import *

from scipy.stats.mstats import mquantiles
from scipy.interpolate import interp1d

#import fitpy.utils.common as fuc

def plot_sens(sensdata,pars,cases,vis="bar",reverse=False,par_labels=[],case_labels=[],colors=[],ncol=4,grid_show=True,xlbl='',plt_title='',text_upp_left='',text_center='',text_upp_right='',legend_show=2,legend_size=10,xdatatick=[],figname='sens.png',showplot=False,topsens=[], lbl_size=32, yoffset=0.1):
    """Plots sensitivity for multiple observables"""

    ncases=sensdata.shape[0]
    npar=sensdata.shape[1]

    wd=0.6
    ylbl='Sensitivity'


    assert set(pars) <= set(range(npar))
    assert set(cases) <= set(range(ncases))

    # Set up the figure
    # TODO need to scale figure size according to the expected amount of legends

    #xticklabel_size=int(400/ncases)
    xticklabel_size=32
    yticklabel_size=32


    fig = plt.figure(figsize=(20,13))
    #fig = plt.figure(figsize=(18,12))
    fig.add_axes([0.1,0.2+yoffset,0.8,0.6-yoffset])
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

    # if colors == []:
    #     colors = ut.set_colors(npar_)


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
            plot(xdatatick_,sensdata[cases,i], '-o',color=colors[pars[i]], label=par_labels[pars[i]])
    elif (vis=="bar"):
        curr=np.zeros((ncases_))
        #print pars,colors
        for i in range(npar_):
            bar(xdatatick,sensdata[cases,i], width=wd*sc,color=colors[pars[i]], bottom=curr, label=par_labels[pars[i]])
            curr=sensdata[cases,i]+curr
        if not xflag:
            if ncases>9:
                xticks(np.array(range(1,ncases_+1)),case_labels_,rotation='vertical')
            else:
                xticks(np.array(range(1,ncases_+1)),case_labels_,rotation='horizontal')
        #xlim(xdatatick[0]-wd*sc/2.-0.1,xdatatick[-1]+wd*sc/2.+0.1)

        xlim(0,365)
        #else:
        #    xticks(xdatatick)

    ylabel(ylbl,fontsize=lbl_size)
    xlabel(xlbl,fontsize=lbl_size)
    plt.yticks(fontsize=yticklabel_size)
    title(plt_title, fontsize=32)
    ax = gca()
    plt.text(0.01, 1.05, text_upp_left,  color='black', transform=ax.transAxes, fontsize=32, bbox=dict(facecolor='white', edgecolor='white'))
    plt.text(0.40, 1.05, text_center,    color='black', transform=ax.transAxes, fontsize=32, bbox=dict(facecolor='white', edgecolor='white'))
    plt.text(0.95, 1.05, text_upp_right, color='black', transform=ax.transAxes, fontsize=32, bbox=dict(facecolor='white', edgecolor='white'))
    # Define the month format
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    plt.gca().xaxis.set_major_formatter(DateFormatter('%d-%b'))
    xticks(rotation='horizontal')

    maxsens=max(max(curr),1.0)
    ylim([0,maxsens])
    handles,labels = gca().get_legend_handles_labels()
    handles = [ handles[i] for i in sensind[:topsens]]
    labels = [ labels[i] for i in sensind[:topsens]]
    if legend_show==1:
        legend(handles,labels,fontsize=legend_size)
    elif (legend_show==2):
        legend(handles,labels,loc='upper left',bbox_to_anchor=(0.0, -0.1),fancybox=True, shadow=True,ncol=ncol,labelspacing=-0.1,fontsize=legend_size)
    elif (legend_show==3):
        legend(handles,labels,loc='upper left', bbox_to_anchor=(0.0, 1.2),fancybox=True, shadow=True,ncol=ncol,labelspacing=-0.1,fontsize=legend_size)


    if not xflag:
        zed = [tick.label.set_fontsize(xticklabel_size) for tick in gca().xaxis.get_major_ticks()]
    
    grid(grid_show)

    plt.savefig(figname, bbox_inches='tight')
    if showplot:
        show()


def plot_yx(x, y, rowcols=None, ylabel='', xlabels=None,
            log=False, filename='eda.png',
            ypad=0.3, gridshow=True, ms=2):

    nsam, ndim = x.shape
    assert(nsam==y.shape[0])

    if rowcols is None:
        rows = 3
        cols = (ndim // 3) + 1
    else:
        rows, cols = rowcols



    fig, axes = plt.subplots(rows, cols, figsize=(8*cols,(3+ypad)*rows),
                             gridspec_kw={'hspace': ypad, 'wspace': 0.3})
    #fig.suptitle('Horizontally stacked subplots')

    axes=axes.reshape(rows, cols)

    axes = axes.T
    #print(axes.shape)
    for i in range(ndim):
        ih = i % cols
        iv = i // cols
        axes[ih, iv].plot(x[:, i], y, 'o', ms=ms)
        axes[ih, iv].set_xlabel(xlabels[i])
        axes[ih, iv].set_ylabel(ylabel)
        #axes[ih, iv].set_ylim(ymin=-0.05, ymax=0.5)
        axes[ih, iv].grid(gridshow)
        if log:
            axes[ih, iv].set_yscale('log')

    for i in range(ndim, cols*rows):
        ih = i % cols
        iv = i // cols
        axes[ih, iv].remove()

    plt.savefig(filename)

    #plt.gcf().clear()
    return

def data_split(data_all, trfrac=0.8):
    nsam = len(data_all[0])
    indperm = np.random.permutation(nsam)
    result = []
    for data in data_all:
        assert(len(data)==nsam)

        ntr = int(nsam*trfrac)
        ind_trn = indperm[:ntr]
        ind_tst = indperm[ntr:]

        data_trn = data[ind_trn]
        data_tst = data[ind_tst]

        result.append((data_trn, data_tst))

    return result


def ind_split(ns, split_method, split_params):

    if (split_method == 'Kfold_small'):
        KK = split_params[0]
        # ind=np.ones((ns))
        indp = np.random.permutation(ns)
        list_ind = np.array_split(indp, KK)
        # ind[i*sam_spl:(i+1)*sam_spl]=np.zeros((sam_spl))
        # intind=ind.astype(int)

    elif (split_method == 'Kfold'):
        KK = split_params[0]

        indp = np.random.permutation(ns)
        full_ind = range(ns)
        fold_ind = np.array_split(indp, KK)
        list_ind = []
        for cur_ind in fold_ind:
            list_ind.append(np.array(list(set(full_ind) - set(cur_ind))))

    elif (split_method == 'rand_fold'):
        KK = split_params[0]

        npt = split_params[1]

        list_ind = []
        for i in range(KK):
            list_ind.append(np.random.permutation(ns)[0:npt])

    elif (split_method == 'trval'):
        assert(ns == np.sum(split_params))
        KK = len(split_params)
        perms = np.random.permutation(ns)
        list_ind = []
        begin = 0
        for i in range(KK):
            list_ind.append(perms[begin:begin + split_params[i]])
            begin += split_params[i]

    return list_ind

class disable_print:

    def __init__(self):
        self.oldstdout = None
        self.oldstderr = None
        self.devnull = open(os.devnull, 'w')

    def __enter__(self):
        self.oldstdout, sys.stdout = sys.stdout, self.devnull
        self.oldstderr, sys.stderr = sys.stderr, self.devnull

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self.oldstdout
        sys.stderr = self.oldstderr


def read_textlist(filename, nsize):

    if os.path.exists(filename):
        with open(filename) as f:
            names = f.read().splitlines()
            assert(len(names) == nsize)
    else:
        names = ['# ' + str(i) for i in range(1, nsize + 1)]

    return names


def pick_ind(data, row):
    ind_data = np.empty((0,), dtype=int)
    assert(data.shape[1] == len(row))
    nr = len(row)
    ndata = data.shape[0]
    inds = []
    islice = []
    for j in range(nr):
        if (row[j] != None):
            inds.append(np.where(data[:, j] == row[j])[0])
        else:
            islice.append(j)
    ind_out = np.arange(ndata)
    for ind in inds:
        ind_out = np.intersect1d(ind_out, ind)
    ind_data = np.append(ind_data, ind_out, axis=0)

    return ind_data, islice




##################################################
##################################################
##################################################


def multidim_intersect(arr1, arr2):
    arr1_view = arr1.view([('', arr1.dtype)] * arr1.shape[1])
    arr2_view = arr2.view([('', arr2.dtype)] * arr2.shape[1])
    intersected = np.intersect1d(arr1_view, arr2_view)
    return intersected.view(arr1.dtype).reshape(-1, arr1.shape[1])

##################################################
##################################################
##################################################


def encode_mindex(mindex):

    npc = mindex.shape[0]
    ndim = mindex.shape[1]
    print("Multiindex has %d terms" % npc)
    dims = []
    ords = []
    for ipc in range(npc):
        nzs = np.nonzero(mindex[ipc, :])[0].tolist()
        if len(nzs) == 0:
            dims.append([0])
            ords.append([0])
        else:
            dims.append([i + 1 for i in nzs])
            ords.append(mindex[ipc, nzs].tolist())
#            this_sp_mindex=np.vstack((nzs+1,mindex[ipc,nzs])).T
 #           this_sp_mindex=this_sp_mindex.reshape(1,-1)

        # effdim=len(np.nonzero(mindex[ipc,:])[0])
        # print effdim
  #      sp_mindex.append(this_sp_mindex)
    return dims, ords  # sp_mindex

##################################################
##################################################
##################################################


def pce_eval(xdata, pctype, mi, pccf):
    uqtkbin = os.environ['UQTK_INS'] + os.sep + 'bin'
    np.savetxt('mi', mi, fmt="%d")
    np.savetxt('pccf', pccf)
    np.savetxt('xdata.dat', xdata)

    cmd = uqtkbin + os.sep + 'pce_eval -x PC_mi -r mi -f pccf -s ' + pctype + ' > pceval.log'
    os.system(cmd)


    ydata = np.loadtxt('ydata.dat')

    return ydata


####################################################################


def pce_sens(pctype, mi, pccf, mv=False):
    uqtkbin = os.environ['UQTK_INS'] + os.sep + 'bin'
    np.savetxt('mi', mi, fmt="%d")
    np.savetxt('pccf', pccf)

    cmd = uqtkbin + os.sep + 'pce_sens -m mi -f pccf -x ' + pctype + ' > pcsens.log'
    os.system(cmd)

    mainsens = np.loadtxt('mainsens.dat')
    totsens = np.loadtxt('totsens.dat')
    jointsens = np.loadtxt('jointsens.dat')
    varfrac = np.atleast_1d(np.loadtxt('varfrac.dat'))

    if (mv):
        mean = pccf[0]
        var = mean**2 / varfrac[0]

        return mainsens, totsens, jointsens, mean, var

    else:
        return mainsens, totsens, jointsens

