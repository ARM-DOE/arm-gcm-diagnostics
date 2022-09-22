#===========================================================================================================================
# Program for generate aerosol-to-ccn activate metric
#---------------------------------------------------------------------------------------------------------------------------
# V3 Development
    # ----------------------------------------------------------------------------------------------------
    # Xiaojian Zheng - Aug2022 @ LLNL
    # ### use all the available collocated data for bulk part activation density plot
    # ----------------------------------------------------------------------------------------------------

#===========================================================================================================================
import os
import pdb
import glob
import cdms2
import cdutil
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from .varid_dict import varid_longname
from .taylor_diagram import TaylorDiagram
from .utils import climo

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

def aerosol_activation_density_plot(parameter):
    variables = parameter.variables
    test_path = parameter.test_data_path
    obs_path = parameter.obs_path
    cmip_path = parameter.cmip_path
    output_path = parameter.output_path
    sites = parameter.sites

    if not os.path.exists(os.path.join(output_path,'figures',sites[0])):
        os.makedirs(os.path.join(output_path,'figures',sites[0])) 
    # Calculate for observational data
    print('ARM data',sites[0])
    obs_file = glob.glob(os.path.join(obs_path,sites[0][:3]+'armdiagsaciactivate' + sites[0][3:5].upper()+'*c1.nc')) #read in data
    print('obs_file',obs_file)
    fin = cdms2.open(obs_file[0])
    # Bulk Activation
    cpc_bulk = fin('cpc_bulk'); cpc_bulk.filled(fill_value=np.nan)
    cpc_bulk=np.array(cpc_bulk)
    #
    ccn02_bulk = fin('ccn02_bulk'); ccn02_bulk.filled(fill_value=np.nan)
    ccn02_bulk=np.array(ccn02_bulk)
    #
    ccn05_bulk = fin('ccn05_bulk'); ccn05_bulk.filled(fill_value=np.nan)
    ccn05_bulk=np.array(ccn05_bulk)
    fin.close()  
    # Plotting================================================================
    # define parameter
    if sites[0] == 'sgpc1':
        ccn02_pedge=np.arange(0,3100,100)
        cpc_pedge=np.arange(0,6200,200)
        pvmax=6000
    if sites[0] == 'enac1':
        ccn02_pedge=np.arange(0,1050,50)
        cpc_pedge=np.arange(0,1050,50)
        pvmax=1000
    #-------------------------------------------------------------------------    
    #Bulk aerosol vs. ccn02
    ratio_all = ccn02_bulk / cpc_bulk
    ratio_mean = np.nanmean(ratio_all) ; ratio_std = np.nanstd(ratio_all)
    
    fig=plt.figure(figsize=(12,10))

    fsize=30;xysize=30;lsize=20
    gspec = GridSpec(ncols=1, nrows=1, figure=fig)
    ax1=fig.add_subplot(gspec[0])
    ax1.set_title(sites[0].upper()+' Bulk Aerosol Activation',fontsize=fsize)
    h2d02,xeg02,yeg02,im02 =plt.hist2d(cpc_bulk,ccn02_bulk,bins=[cpc_pedge,ccn02_pedge],cmap='turbo')
    ax1.plot([0,pvmax],[0,pvmax],'r',lw=3)
    ax1.text(0.02,0.9,'Ratio = '+'%.2f' % ratio_mean+'$\pm$'+'%.2f' % ratio_std,color='r',
             ha='left', va='center', transform=ax1.transAxes,fontsize=xysize)
    ax1.set_xlabel('Aerosol Num. Conc. (# $cm^{-3}$)',fontsize=xysize)
    ax1.set_ylabel('CCN Num. Conc. @0.2%SS (# $cm^{-3}$)',fontsize=xysize)
    ax1.tick_params(labelsize=xysize,length=10,width=2,direction='out',which='major')
    ax1.tick_params(length=7,width=3,direction='out',which='minor')
    for axis in ['top','bottom','left','right']:
            ax1.spines[axis].set_linewidth(2)
    plt.subplots_adjust(left = 0.15, right = 0.95, bottom = 0.11, top = 0.94,hspace=0.15)  
    plt.savefig(output_path+'/figures/'+sites[0]+'/'+'aerosol_activation_bulk_cpc_ccn02_'+sites[0]+'.png')
    
    #-------------------------------------------------------------------------    
    #Bulk aerosol vs. ccn05
    ratio_all = ccn05_bulk / cpc_bulk
    ratio_mean = np.nanmean(ratio_all) ; ratio_std = np.nanstd(ratio_all)
    
    fig=plt.figure(figsize=(12,10))

    fsize=30;xysize=30;lsize=20
    gspec = GridSpec(ncols=1, nrows=1, figure=fig)
    ax1=fig.add_subplot(gspec[0])
    ax1.set_title(sites[0].upper()+' Bulk Aerosol Activation',fontsize=fsize)
    h2d02,xeg02,yeg02,im02 =plt.hist2d(cpc_bulk,ccn05_bulk,bins=[cpc_pedge,ccn02_pedge],cmap='turbo')
    ax1.plot([0,pvmax],[0,pvmax],'r',lw=3)
    ax1.text(0.02,0.9,'Ratio = '+'%.2f' % ratio_mean+'$\pm$'+'%.2f' % ratio_std,color='r',
             ha='left', va='center', transform=ax1.transAxes,fontsize=xysize)
    ax1.set_xlabel('Aerosol Num. Conc. (# $cm^{-3}$)',fontsize=xysize)
    ax1.set_ylabel('CCN Num. Conc. @0.5%SS (# $cm^{-3}$)',fontsize=xysize)
    ax1.tick_params(labelsize=xysize,length=10,width=2,direction='out',which='major')
    ax1.tick_params(length=7,width=3,direction='out',which='minor')
    for axis in ['top','bottom','left','right']:
            ax1.spines[axis].set_linewidth(2)
    plt.subplots_adjust(left = 0.15, right = 0.95, bottom = 0.11, top = 0.94,hspace=0.15)  
    plt.savefig(output_path+'/figures/'+sites[0]+'/'+'aerosol_activation_bulk_cpc_ccn05_'+sites[0]+'.png')
    
    #-------------------------------------------------------------------------
    
    
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=    