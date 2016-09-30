#!/usr/bin/env python
# Copyright: This document has been placed in the public domain.

"""
Taylor diagram (Taylor, 2001) test implementation.

http://www-pcmdi.llnl.gov/about/staff/Taylor/CV/Taylor_diagram_primer.htm
"""

__version__ = "Time-stamp: <2012-02-17 20:59:35 ycopin>"
__author__ = "Yannick Copin <yannick.copin@laposte.net>"

import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt

class TaylorDiagram(object):
    """Taylor diagram: plot model standard deviation and correlation
    to reference (data) sample in a single-quadrant polar plot, with
    r=stddev and theta=arccos(correlation).
    """

    def __init__(self, refstd, fig=None, rect=111, label='_'):
        """Set up Taylor diagram axes, i.e. single quadrant polar
        plot, using mpl_toolkits.axisartist.floating_axes. refstd is
        the reference standard deviation to be compared to.
        """

        from matplotlib.projections import PolarAxes
        import mpl_toolkits.axisartist.floating_axes as FA
        import mpl_toolkits.axisartist.grid_finder as GF

        self.refstd = refstd            # Reference standard deviation

        tr = PolarAxes.PolarTransform()

        # Correlation labels
        rlocs = np.concatenate((np.arange(10)/10.,[0.95,0.99]))
        tlocs = np.arccos(rlocs)        # Conversion to polar angles
        gl1 = GF.FixedLocator(tlocs)    # Positions
        tf1 = GF.DictFormatter(dict(zip(tlocs, map(str,rlocs))))

        # Standard deviation axis extent
        self.smin = 0.0
        self.smax = 1.5*self.refstd

        ghelper = FA.GridHelperCurveLinear(tr,
                                           extremes=(0,np.pi/2, # 1st quadrant
                                                     self.smin,self.smax),
                                           grid_locator1=gl1,
                                           tick_formatter1=tf1,
                                           )

#        if fig is None:
#            fig = plt.figure()

        ax = FA.FloatingSubplot(fig, rect, grid_helper=ghelper)
        fig.add_subplot(ax)

        # Adjust axes
        ax.axis["top"].set_axis_direction("bottom")  # "Angle axis"
        ax.axis["top"].toggle(ticklabels=True, label=True)
        ax.axis["top"].major_ticklabels.set_axis_direction("top")
        ax.axis["top"].label.set_axis_direction("top")
        ax.axis["top"].label.set_text("Correlation")

        ax.axis["left"].set_axis_direction("bottom") # "X axis"
        ax.axis["left"].label.set_text("Standard deviation")

        ax.axis["right"].set_axis_direction("top")   # "Y axis"
        ax.axis["right"].toggle(ticklabels=True)
        ax.axis["right"].major_ticklabels.set_axis_direction("left")

        ax.axis["bottom"].set_visible(False)         # Useless
        
        # Contours along standard deviations
        ax.grid(False)

        self._ax = ax                   # Graphical axes
        self.ax = ax.get_aux_axes(tr)   # Polar coordinates

        # Add reference point and stddev contour
        #print "Reference std:", self.refstd
        l, = self.ax.plot([0], self.refstd, 'k*',
                          ls='', ms=10, label=label)
        t = np.linspace(0, np.pi/2)
        r = np.zeros_like(t) + self.refstd
        self.ax.plot(t,r, 'k--', label='_')

        # Collect sample points for latter use (e.g. legend)
        self.samplePoints = [l]

    def add_sample(self, stddev, corrcoef, *args, **kwargs):
        """Add sample (stddev,corrcoeff) to the Taylor diagram. args
        and kwargs are directly propagated to the Figure.plot
        command."""

        l, = self.ax.plot(np.arccos(corrcoef), stddev,
                          *args, **kwargs) # (theta,radius)
        self.samplePoints.append(l)

        return l

    def add_contours(self, levels=5, **kwargs):
        """Add constant centered RMS difference contours."""

        rs,ts = np.meshgrid(np.linspace(self.smin,self.smax),
                            np.linspace(0,np.pi/2))
        # Compute centered RMS difference
        rms = np.sqrt(self.refstd**2 + rs**2 - 2*self.refstd*rs*np.cos(ts))
        
        contours = self.ax.contour(ts, rs, rms, levels, **kwargs)

        return contours


#if __name__=='__main__':
#
#    basedir='/g/g92/zhang40/calc_stats'
#    pr_obs=genfromtxt(basedir+'/data/all_pr_obs_regrid_3x3.csv')
#    # Reference dapret
#    data=pr_obs[0,:]
#    refstd = data.std(ddof=1)           # Reference standard deviation
#    x=np.arange(12)
#    
#    # Models
#    pr_cmip=genfromtxt(basedir+'/data/all_pr_model_regrid_3x3.csv')
#    pr_mod=genfromtxt(basedir+'/data/'+'CESM-CAM5_AC.csv')
#
#    # Compute stddev and correlation coefficient of models
#    mod_num=pr_cmip.shape[0]-1
#    m_all=[pr_cmip[x,:] for x in range(mod_num)]
##    print m_all[20]
#    samples = np.array([ [m.std(ddof=1), np.corrcoef(data, m)[0,1]]
#                         for m in m_all])
##    print data, pr_mod[0,:]
#    print samples
#    mod_sample=np.array([ pr_mod[1,:].std(ddof=1), np.corrcoef(data, pr_mod[1,:])[0,1]])
#    mmm_sample=np.array([ pr_cmip[mod_num,:].std(ddof=1), np.corrcoef(data, pr_cmip[mod_num,:])[0,1]])
#
#    fig = plt.figure(figsize=(8,8))
#    dia = TaylorDiagram(refstd, fig=fig,rect=111, label="Reference")
##    colors = plt.matplotlib.cm.rainbow(np.linspace(0,1,len(samples)))
##    markers = iter(['o','s','v','^','D','>','p','o','s','v','^','D','>','p','o','s','v','^','D','>','p','o','s','v','^','D','H','p','o','s','v','^','D','>','p'])
#
#    # Add samples to Taylor diagram
#    for i,(stddev,corrcoef) in enumerate(samples):
#        dia.add_sample(stddev, corrcoef, marker='.',ms=10, c='grey')
#
#    dia.add_sample(mod_sample[0], mod_sample[1],marker='.',ms=15, c='red',label='MOD') 
#    dia.add_sample(mmm_sample[0], mmm_sample[1],marker='.',ms=15, c='b',label='MMM') 
#    # Add RMS contours, and label them
#    contours = dia.add_contours(colors='0.5')
#    plt.clabel(contours, inline=1, fontsize=10)
#    plt.title('Surface Precipitation (mm/day)')
#
#    print dia.samplePoints[21]
#    # Add a figure legend
#    fig.legend([dia.samplePoints[0],dia.samplePoints[22],dia.samplePoints[23]] ,
#               [ p.get_label() for p in [dia.samplePoints[0],dia.samplePoints[22],dia.samplePoints[23]] ],
#               numpoints=1,  loc='upper right',prop={'size':10})
#    fig.savefig('figures/AC_amip_taylorD_pr.png')
#
##    plt.show()
#
