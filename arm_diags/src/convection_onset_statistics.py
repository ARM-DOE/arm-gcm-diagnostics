
# coding: utf-8

# This program is provided as-is and WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTIBILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You are allowed to redistribute it
# and/or modify it AT YOUR OWN RISK.
# 
# The radiosonde. radiometer, gauge data is provided by 
# the U.S. Department of Energy (DOE) as part of the
# Atmospheric Radiation Measurement (ARM) Climate Research Facility.
#     Stokes, G. M., and S. E. Schwartz, 1994: The Atmospheric 
#     Radiation Measurement (ARM) program: Programmatic background
#     and design of the cloud and radiation testbed. Bull.
#     Amer. Meteor. Soc., 75, 1201–1221.
# 
# Based directly on calculations in:
# 
# Schiro, K. A., J. D. Neelin, D. K. Adams, and B. R. Lintner, 2016: 
# Deep Convection and Column Water Vapor over Tropical Land versus Tropical Ocean: 
# A Comparison between the Amazon and the Tropical Western Pacific. J. Atmos. Sci., 73, 4043-4063.
# 
# See also:
# 
# Holloway, C. E. and J. D. Neelin, 2009: Moisture vertical structure, 
# column water vapor, and tropical deepconvection. J. Atmos. Sci., 66, 1665-1683. 
# DOI: 10.1175/2008JAS2806.1
# 
# Kuo, Y-H., J. D. Neelin, and C. R. Mechoso, 2017: Tropical convective 
# transition statistics and causality in the water vapor precipitation relation. 
# J. Atmos. Sci. (accepted, 12 Dec 2016)
# 
# Sahany, S., J. D. Neelin, K. Hales, and R. B. Neale, 2012: Temperature–Moisture Dependence of the Deep Convective Transition as a Constraint on Entrainment in Climate Models. J. Atmos. Sci., 69, 1340-1358.
# 
# This research supported in part by the Office of Biological and Environmental
# Research of the U.S.DOE Grant DE-SC0011074, National Science
# Foundation Grants AGS-1102838, and National Oceanic and Atmospheric Administration
# Grants NA14OAR4310274 and NA15OAR4310097.
# 
# Please follow ARM data sharing policy as per the
# Data Attribution and Publication section of their
# Data Sharing and Distribution Policy outlined at
# http://www.arm.gov/data/docs/policy
# We gratefully acknowledge the U.S. DOE for 
# providing the data.
# 
# Original code: Kathleen Schiro, python version 22 Dec 2016, University of California Dept. of Atmospheric and Oceanic Sciences
# 
# Modifications: Baird Langenbrunner, Yi-Hung Kuo
# 
# Scientific supervision: Prof. J David Neelin
# 
# For related publications and research information see 
# the Neelin group webpage  http://www.atmos.ucla.edu/~csi/


import numpy as np
import math
import scipy.io
import matplotlib.pyplot as mp
import matplotlib.cm as cm

def convection_onset_statistics(cwv, precip,test, output_path,sites):
# Create CWV bins
    number_of_bins = 28 # default = 28
    cwv_max = 70 # default = 70 (in mm)
    cwv_min = 28 # default = 28 (in mm)
    bin_width = 1.5 # default = 1.5
    bin_center = np.arange((cwv_min+(bin_width/2)), (cwv_max-(bin_width/2))+bin_width, bin_width)

    # Define precip threshold
    precip_threshold = 0.5; # default 0.5 (in mm/hr)

    # Define variables for binning
    bin_index = np.zeros([number_of_bins,cwv.size])
    precip_binned = np.empty([number_of_bins,cwv.size]) * np.nan
    precip_counts = np.zeros([number_of_bins,cwv.size])


    # In[264]:

    # Bin the data by CWV value as specified above
    for i in range (0,number_of_bins):
        for j in range(0,cwv.size):
            if cwv[j] > (cwv_min+(i*bin_width)):
                bin_index[i,j] = 1
            if cwv[j] > (cwv_min+(i*bin_width)+bin_width):
                bin_index[i,j] = 0
            if bin_index[i,j] == 1:  
                precip_binned[i,j] = precip[j]
            else:
                precip_binned[i,j] = np.nan
            if precip_binned[i,j] >= precip_threshold:
                precip_counts[i,j] = 1
            if np.isnan(precip_binned[i,j]):
                precip_counts[i,j] = np.nan


    # In[265]:

    # Create binned arrays
    hist_cwv = np.empty([number_of_bins,1]) * np.nan
    hist_precip_points = np.empty([number_of_bins,1]) * np.nan
    pr_binned_mean = np.empty([number_of_bins,1]) * np.nan
    pr_binned_var = np.empty([number_of_bins,1]) * np.nan
    pr_binned_std = np.empty([number_of_bins,1]) * np.nan
    pr_probability = np.empty([number_of_bins,1]) * np.nan
    errorbar_hist_precip_points = np.empty([number_of_bins,1]) * np.nan
    std_error_precip = np.empty([number_of_bins,1]) * np.nan
    pdf_cwv = np.empty([number_of_bins,1]) * np.nan
    pdf_precipitating_points = np.empty([number_of_bins,1]) * np.nan

    # Fill binned arrays
    hist_cwv = bin_index.sum(axis=1)
    hist_precip_points = np.nansum(precip_counts,axis=1)
    pr_binned_mean = np.nanmean(precip_binned,axis=1)
    pr_binned_var = np.nanvar(precip_binned,axis=1)
    pr_binned_std = np.nanstd(precip_binned,axis=1)
    r = np.empty([1,number_of_bins]) * np.nan
    r = np.sum(~np.isnan(precip_counts),axis=1)
    pr_probability = np.nansum(precip_counts,axis=1)/r
    pdf_cwv = hist_cwv/bin_width
    pdf_precipitating_points = hist_precip_points/bin_width
    for i in range(0,number_of_bins):
        std_error_precip[i] = pr_binned_std[i]/math.sqrt(hist_cwv[i])
        errorbar_hist_precip_points[i] = math.sqrt(hist_precip_points[i])/bin_width


    # In[266]:

    # create color map
    # choose from maps here:
    # http://matplotlib.org/examples/color/colormaps_reference.html
    scatter_colors = cm.jet(np.linspace(0,1,number_of_bins+1,endpoint=True))
    # scatter_colors = cm.plasma(numpy.linspace(0,1,number_of_bins+1,endpoint=True))


    # In[267]:

    axes_fontsize = 12 # size of font in all plots
    legend_fontsize = 9
    marker_size = 40 # size of markers in scatter plots
    xtick_pad = 10 # padding between x tick labels and actual plot

    # create figure canvas
    fig = mp.figure(figsize=(8,2.5))


    # create figure 1
    ax1 = fig.add_subplot(131)
    ax1.set_xlim(25,72)
    ax1.set_ylim(0,6)
    ax1.set_xticks([30,40,50,60,70])
    ax1.set_yticks([0,1,2,3,4,5,6])
    ax1.tick_params(labelsize=axes_fontsize)
    ax1.tick_params(axis='x', pad=10)
    error = [std_error_precip,std_error_precip]
    ax1.errorbar(bin_center, pr_binned_mean, xerr=0, yerr=error, ls='none', color='black')
    ax1.scatter(bin_center, pr_binned_mean, edgecolor='none', facecolor=scatter_colors, s=marker_size, clip_on=False, zorder=3)
    ax1.set_ylabel('Precip (mm hr $^-$ $^1$)', fontsize=axes_fontsize)
    ax1.set_xlabel('CWV (mm)', fontsize=axes_fontsize)
    ax1.text(0.05, 0.95, sites[0], transform=ax1.transAxes, fontsize=12, verticalalignment='top')
    ax1.text(0.05, 0.85, test, transform=ax1.transAxes, fontsize=12, verticalalignment='top')
    #ax1.grid()
    ax1.set_axisbelow(True)

    # create figure 2 (probability pickup)
    ax2 = fig.add_subplot(132)
    ax2.set_xlim(25,72)
    ax2.set_ylim(0,1)
    ax2.set_xticks([30,40,50,60,70])
    ax2.set_yticks([0.0,0.2,0.4,0.6,0.8,1.0])
    ax2.tick_params(labelsize=axes_fontsize)
    ax2.tick_params(axis='x', pad=xtick_pad)
    ax2.scatter(bin_center, pr_probability, marker='d', s=marker_size, edgecolor='none', facecolor='steelblue', clip_on=False, zorder=3)
    ax2.set_ylabel('Probability of Precip', fontsize=axes_fontsize)
    ax2.set_xlabel('CWV (mm)', fontsize=axes_fontsize)
    #ax2.grid()
    ax2.set_axisbelow(True)

    # create figure 3 (non-normalized PDF)
    ax3 = fig.add_subplot(133)
    ax3.set_yscale('log')
    ax3.set_ylim(5e-1, 5e5)
    ax3.set_xlim(25,72)
    ax3.set_xticks([30,40,50,60,70])
    ax3.set_yticks(10**np.array((0,1,2,3,4,5)))
    ax3.tick_params(labelsize=axes_fontsize)
    ax3.tick_params(axis='x', pad=xtick_pad)
    # yscale is log scale, so throw out any zero values
    pdf_precipitating_points[pdf_precipitating_points==0] = np.nan
    error = [errorbar_hist_precip_points,errorbar_hist_precip_points]
    ax3.errorbar(bin_center, pdf_precipitating_points, xerr=0, yerr=error, ls='none', color='black')
    ax3.scatter(bin_center, pdf_precipitating_points, edgecolor='none', facecolor='b', s=marker_size, clip_on=False, zorder=3, label='precip $>$ 0.5 mm hr $^{\minus 1}$')
    ax3.scatter(bin_center, pdf_cwv, marker='x', color='0', label='all')
    ax3.set_ylabel('Freq Density', fontsize=axes_fontsize)
    ax3.set_xlabel('CWV (mm)', fontsize=axes_fontsize)
    #ax3.grid()
    ax3.set_axisbelow(True)

    # create legend
    legend_handles, legend_labels = ax3.get_legend_handles_labels()
    ax3.legend(legend_handles, legend_labels, loc='upper left', bbox_to_anchor=(0.1,0.95), fontsize=legend_fontsize, scatterpoints=1, handlelength=0, labelspacing=0, borderpad=0, borderaxespad=0, frameon=False)



    # set layout to tight (so that space between figures is minimized)
    mp.tight_layout()
    # save figure
    #mp.savefig('conv_diagnostics_example_kas_new.pdf', transparent=True, bbox_inches='tight')
    mp.savefig(output_path +'/figures/conv_diagnostics_'+test+'_'+sites[0]+'.png', transparent=True, bbox_inches='tight')



