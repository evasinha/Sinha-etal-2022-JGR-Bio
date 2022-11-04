#!/usr/bin/env python

import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt


def myrc():
    mpl.rc('legend', loc='best', fontsize=22)
    mpl.rc('lines', linewidth=4, color='r')
    mpl.rc('axes', linewidth=1, grid=True, labelsize=22)
    mpl.rc('xtick', labelsize=20)
    mpl.rc('ytick', labelsize=20)
    mpl.rc('font', size=20)
    mpl.rc('figure', figsize=(12, 9), max_open_warning=200)
    # mpl.rc('font', family='serif')

    return mpl.rcParams

def plot_yx(x, y, rowcols=None, ylabel='', xlabels=None,
            log=False, filename='eda.png',
            ypad=0.3, gridshow=True, ms=2):

    nsam, ndim = x.shape
    assert(nsam == y.shape[0])

    if rowcols is None:
        rows = 3
        cols = (ndim // 3) + 1
    else:
        rows, cols = rowcols

    fig, axes = plt.subplots(rows, cols, figsize=(8 * cols, (3 + ypad) * rows),
                             gridspec_kw={'hspace': ypad, 'wspace': 0.3})
    #fig.suptitle('Horizontally stacked subplots')

    axes = axes.reshape(rows, cols)

    axes = axes.T
    # print(axes.shape)
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

    for i in range(ndim, cols * rows):
        ih = i % cols
        iv = i // cols
        axes[ih, iv].remove()

    plt.savefig(filename, bbox_inches='tight')

    # plt.gcf().clear()
    return


def set_colors(npar):
    """ Sets a list of different colors of requested length, as rgb triples"""
    colors = []
    pp = 1 + int(npar / 6)
    for i in range(npar):
        c = 1 - float(int((i / 6)) / pp)
        b = np.empty((3))
        for jj in range(3):
            b[jj] = c * int(i % 3 == jj)
        a = int(int(i % 6) / 3)
        colors.append(((1 - a) * b[2] + a * (c - b[2]),
                       (1 - a) * b[1] + a * (c - b[1]),
                       (1 - a) * b[0] + a * (c - b[0])))

    return colors


def plot_dm(datas, models, errorbars=[], labels=[],
            axes_labels=['Model', 'Apprx'], figname='dm.eps',
            showplot=False, legendpos='in', msize=4):
    """Plots data-vs-model and overlays y=x"""
    if errorbars == []:
        erb = False
    else:
        erb = True

    custom_xlabel = axes_labels[0]
    custom_ylabel = axes_labels[1]

    if legendpos == 'in':
        fig = plt.figure(figsize=(10, 10))
    elif legendpos == 'out':
        fig = plt.figure(figsize=(14, 10))
        fig.add_axes([0.1, 0.1, 0.6, 0.8])

    ncase = len(datas)
    if labels == []:
        labels = [''] * ncase

    # Create colors list
    colors = set_colors(ncase)
    yy = np.empty((0, 1))
    for i in range(ncase):
        data = datas[i]
        model = models[i]
        if erb:
            erbl, erbh = errorbars[i]
        npts = data.shape[0]
        neach = 1
        if (data.ndim > 1):
            neach = data.shape[1]

        # neb=model.shape[1]-1# errbars not implemented yet

        ddata = data.reshape(npts, neach)

        for j in range(neach):
            yy = np.append(yy, ddata[:, j])
            if (erb):
                plt.errorbar(ddata[:, j], model, yerr=[erbl, erbh],
                             fmt='o', markersize=2, ecolor='grey')
            plt.plot(ddata[:, j], model, 'o', color=colors[i], label=labels[i], markersize=msize)

    delt = 0.1 * (yy.max() - yy.min())
    minmax = [yy.min() - delt, yy.max() + delt]
    plt.plot(minmax, minmax, 'k--', linewidth=1.5, label='y=x')

    plt.xlabel(custom_xlabel)
    plt.ylabel(custom_ylabel)
    # plt.title('Data vs Model')
    if legendpos == 'in':
        plt.legend()
    elif legendpos == 'out':
        plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5),
                   ncol=1, fancybox=True, shadow=True)

    # plt.xscale('log')
    # plt.yscale('log')

    # plt.gca().set_aspect('equal', adjustable='box')
    # plt.axis('scaled')
    # plt.axis('equal')
    #plt.gca().set_aspect('equal', adjustable='box')
    # Trying to make sure both axis have the same number of ticks
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(7))
    plt.gca().yaxis.set_major_locator(plt.MaxNLocator(7))
    plt.savefig(figname, bbox_inches='tight')
    if showplot:
        plt.show()
    plt.clf()
