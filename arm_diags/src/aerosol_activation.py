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
    test_model = parameter.test_data_set
    obs_path = parameter.obs_path
    cmip_path = parameter.cmip_path
    output_path = parameter.output_path
    sites = parameter.sites

    if not os.path.exists(os.path.join(output_path,'figures',sites[0])):
        os.makedirs(os.path.join(output_path,'figures',sites[0])) 
    #==========================================================================
    # Control plotting index
    index_hist = 0
    #==========================================================================
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
    #==========================================================================
    # Plotting=================================================================
    #==========================================================================
    # define parameter
    if sites[0] == 'sgpc1':
        ccn02_pedge=np.arange(0,6200,100)
        cpc_pedge=np.arange(0,6200,100)
        pvmax=6000
    if sites[0] == 'enac1':
        ccn02_pedge=np.arange(0,1020,20)
        cpc_pedge=np.arange(0,1020,20)
        pvmax=1000
    #-------------------------------------------------------------------------    
    #cpc & ccn histograms
    if index_hist == 1:
        if sites[0] == 'sgpc1':
            hist_pedge=np.arange(0,20200,200)
            histccn_pedge=np.arange(0,6200,200)
            pvgap=200; pvmax_hist=10000; pvmax_hist_ccn=6000
        if sites[0] == 'enac1':
            hist_pedge=np.arange(0,10200,200)
            histccn_pedge=np.arange(0,2200,200)
            pvgap=200; pvmax_hist=6000; pvmax_hist_ccn=2000
        hist_cpc_obs,bins_obs=np.histogram(cpc_bulk,bins=hist_pedge)
        freq_cpc_obs = hist_cpc_obs/np.sum(hist_cpc_obs)
        hist_ccn02_obs,ccnbins_obs=np.histogram(ccn02_bulk,bins=histccn_pedge)
        freq_ccn02_obs = hist_ccn02_obs/np.sum(hist_ccn02_obs)
        hist_ccn05_obs,ccnbins_obs=np.histogram(ccn05_bulk,bins=histccn_pedge)
        freq_ccn05_obs = hist_ccn05_obs/np.sum(hist_ccn05_obs)

        fig=plt.figure(figsize=(26,10))
        fsize=30;xysize=30;lsize=30
        gspec = GridSpec(ncols=2, nrows=1, figure=fig)
        ax1=fig.add_subplot(gspec[0])
        ax1.set_title(sites[0].upper()+' Aerosol Distribution (OBS)',fontsize=fsize)
        ax1.bar(bins_obs[:-1]+pvgap/3., freq_cpc_obs, width = pvgap/3*2, color='k',align='edge',\
                                label='Aerosol = '+'%3i' % np.nanmean(cpc_bulk)\
                                 +'$\pm$'+'%3i' % np.nanstd(cpc_bulk))
        ax1.set_xlim(0, pvmax_hist)
        #yup=(int(np.nanmax(freq_cpc_obs)*10.)+1)/10.
        ax1.set_ylim(0,0.3)
        ax1.set_xlabel('Aerosol Num. Conc.($cm^{-3}$)',fontsize=fsize)
        ax1.set_ylabel('PDF',fontsize=fsize)
        ax1.tick_params(axis='x',labelsize=lsize,length=0,width=3,direction='in',which='major')
        ax1.tick_params(axis='y',labelsize=lsize,length=5,width=3,direction='out',which='major')
        #ax1.set_xticks(xbin)
        ax1.legend(loc='best',fontsize=lsize)
        for axis in ['top','bottom','left','right']:
            ax1.spines[axis].set_linewidth(3)
        #-----------------------------------------------
        ax1=fig.add_subplot(gspec[1])
        ax1.set_title(sites[0].upper()+' CCN Distribution (OBS)',fontsize=fsize)
        ax1.bar(ccnbins_obs[:-1]+pvgap/4., freq_ccn02_obs, width = pvgap/4, color='b',align='edge',\
                                label='$CCN_{0.2SS}$ = '+'%3i' % np.nanmean(ccn02_bulk)\
                                 +'$\pm$'+'%3i' % np.nanstd(ccn02_bulk))
        ax1.bar(ccnbins_obs[:-1]+pvgap/2., freq_ccn05_obs, width = pvgap/4, color='r',align='edge',\
                                label='$CCN_{0.5SS}$ = '+'%3i' % np.nanmean(ccn05_bulk)\
                                 +'$\pm$'+'%3i' % np.nanstd(ccn05_bulk))
        ax1.set_xlim(0, pvmax_hist_ccn)
        #yup=(int(np.nanmax([freq_ccn02_obs,freq_ccn05_obs])*10.)+1)/10.
        ax1.set_ylim(0,0.3)
        ax1.set_xlabel('Aerosol Num. Conc.($cm^{-3}$)',fontsize=fsize)
        ax1.set_ylabel('PDF',fontsize=fsize)
        ax1.tick_params(axis='x',labelsize=lsize,length=0,width=3,direction='in',which='major')
        ax1.tick_params(axis='y',labelsize=lsize,length=5,width=3,direction='out',which='major')
        #ax1.set_xticks(xbin)
        ax1.legend(loc='best',fontsize=lsize)
        for axis in ['top','bottom','left','right']:
            ax1.spines[axis].set_linewidth(3)
        plt.subplots_adjust(left = 0.07, right = 0.97, bottom = 0.10, top = 0.95,hspace=0.10) 
        plt.savefig(output_path+'/figures/'+sites[0]+'/'+'aerosol_all_distribution_hist_obs_'+sites[0]+'.png')
    #-------------------------------------------------------------------------    
    #Bulk aerosol vs. ccn02
    ratio_all = ccn02_bulk / cpc_bulk
    ratio_mean = np.nanmean(ratio_all) ; ratio_std = np.nanstd(ratio_all)
    
    fig=plt.figure(figsize=(12,10))

    fsize=30;xysize=30;lsize=20
    gspec = GridSpec(ncols=1, nrows=1, figure=fig)
    ax1=fig.add_subplot(gspec[0])
    ax1.set_title(sites[0].upper()+' Bulk Aerosol Activation (OBS)',fontsize=fsize)
    h2d02,xeg02,yeg02,im02 =plt.hist2d(cpc_bulk,ccn02_bulk,bins=[cpc_pedge,ccn02_pedge],cmap='turbo',density=True)
    ax1.plot([0,pvmax],[0,pvmax],'r',lw=3)
    ax1.text(0.02,0.9,'Ratio = '+'%.2f' % ratio_mean+'$\pm$'+'%.2f' % ratio_std,color='r',
             ha='left', va='center', transform=ax1.transAxes,fontsize=xysize)
    ax1.set_xlabel('Aerosol Num. Conc. (# $cm^{-3}$)',fontsize=xysize)
    ax1.set_ylabel('CCN Num. Conc. @0.2%SS (# $cm^{-3}$)',fontsize=xysize)
    ax1.tick_params(labelsize=xysize,length=10,width=2,direction='out',which='major')
    ax1.tick_params(length=7,width=3,direction='out',which='minor')
    cb1=plt.colorbar()
    cb1.ax.tick_params(labelsize=13)
    cb1.set_label('Probability Density',fontsize=15)
    for axis in ['top','bottom','left','right']:
            ax1.spines[axis].set_linewidth(2)
    plt.subplots_adjust(left = 0.16, right = 1.01, bottom = 0.11, top = 0.94,hspace=0.15)  
    plt.savefig(output_path+'/figures/'+sites[0]+'/'+'aerosol_activation_bulk_cpc_ccn02_obs_'+sites[0]+'.png')
    
    #-------------------------------------------------------------------------    
    #Bulk aerosol vs. ccn05
    ratio_all = ccn05_bulk / cpc_bulk
    ratio_mean = np.nanmean(ratio_all) ; ratio_std = np.nanstd(ratio_all)
    
    fig=plt.figure(figsize=(12,10))

    fsize=30;xysize=30;lsize=20
    gspec = GridSpec(ncols=1, nrows=1, figure=fig)
    ax1=fig.add_subplot(gspec[0])
    ax1.set_title(sites[0].upper()+' Bulk Aerosol Activation (OBS)',fontsize=fsize)
    h2d02,xeg02,yeg02,im02 =plt.hist2d(cpc_bulk,ccn05_bulk,bins=[cpc_pedge,ccn02_pedge],cmap='turbo',density=True)
    ax1.plot([0,pvmax],[0,pvmax],'r',lw=3)
    ax1.text(0.02,0.9,'Ratio = '+'%.2f' % ratio_mean+'$\pm$'+'%.2f' % ratio_std,color='r',
             ha='left', va='center', transform=ax1.transAxes,fontsize=xysize)
    ax1.set_xlabel('Aerosol Num. Conc. (# $cm^{-3}$)',fontsize=xysize)
    ax1.set_ylabel('CCN Num. Conc. @0.5%SS (# $cm^{-3}$)',fontsize=xysize)
    ax1.tick_params(labelsize=xysize,length=10,width=2,direction='out',which='major')
    ax1.tick_params(length=7,width=3,direction='out',which='minor')
    cb1=plt.colorbar()
    cb1.ax.tick_params(labelsize=13)
    cb1.set_label('Probability Density',fontsize=15)
    for axis in ['top','bottom','left','right']:
            ax1.spines[axis].set_linewidth(2)
    plt.subplots_adjust(left = 0.16, right = 1.01, bottom = 0.11, top = 0.94,hspace=0.15)  
    plt.savefig(output_path+'/figures/'+sites[0]+'/'+'aerosol_activation_bulk_cpc_ccn05_obs_'+sites[0]+'.png')
    #-------------------------------------------------------------------------
    #==========================================================================
    #==========================================================================
    #==========================================================================
    #==========================================================================
    #==========================================================================
    # Calculate for test model
    test_findex = 0 #preset of test model indicator
    
    test_model = ''.join(e for e in test_model if e.isalnum()).lower()
    print(test_path,test_model,sites[0][:3]+test_model+'*hr' + sites[0][3:5].upper())
    test_file = glob.glob(os.path.join(test_path,sites[0][:3]+test_model+'*hr' + sites[0][3:5].upper()+'*.nc' ))

    if len(test_file) == 0:
       print('No hour data for test model were found: '+sites[0])

    #test model exist
    if len(test_file) > 0: 
        test_findex = 1 

        #initialize the indicator for temporal res of testmodel
        test_tres = test_file[0].split(test_model)[-1][:3] #e.g., '3hr', '1hr'
        print('test_file',test_file[0])
        
        fin = cdms2.open(test_file[0])
        # test Activation
        #check if test model contain the required variables
        #cpc
        try:
            cpc_test0 = fin('cpc'); cpc_test0.filled(fill_value=np.nan)
            cpc_test0=np.array(cpc_test0)
            test_cpc_exist = 1
        except:
            test_cpc_exist = 0
        #aitken mode aerosol
        try:
            ait_test0 = fin('aitken'); ait_test0.filled(fill_value=np.nan)
            ait_test0=np.array(ait_test0)
            test_ait_exist = 1
        except:
            test_ait_exist = 0
        #accumulation mode aerosol
        try:
            acc_test0 = fin('accumulation'); acc_test0.filled(fill_value=np.nan)
            acc_test0=np.array(acc_test0)
            test_acc_exist = 1
        except:
            test_acc_exist = 0
        #ccn at 0.2%SS
        try:
            ccn02_test0 = fin('ccn02'); ccn02_test0.filled(fill_value=np.nan)
            ccn02_test0=np.array(ccn02_test0)
            test_ccn02_exist = 1
        except:
            test_ccn02_exist = 0
        #ccn at 0.5%SS
        try:
            ccn05_test0 = fin('ccn05'); ccn05_test0.filled(fill_value=np.nan)
            ccn05_test0=np.array(ccn05_test0)
            test_ccn05_exist = 1
        except:
            test_ccn05_exist = 0

        fin.close()  
        #initial QC
        if (test_cpc_exist == 1) and (test_ccn02_exist == 1) and (test_ccn05_exist == 1):
            lvloc=np.where((cpc_test0>0)&(ccn02_test0>0)&(ccn05_test0>0))[0]
            cpc_test=cpc_test0[lvloc].copy(); ccn02_test=ccn02_test0[lvloc].copy(); ccn05_test=ccn05_test0[lvloc].copy();
            if (test_ait_exist == 1) and (test_acc_exist == 1):
                ait_test=ait_test0[lvloc].copy(); acc_test=acc_test0[lvloc].copy()
        #pdb.set_trace()
        #==========================================================================
        # Plotting=================================================================
        #==========================================================================  
        #cpc & ccn histograms
        if index_hist == 1:
            if test_cpc_exist == 1:
                hist_cpc_test,bins_test=np.histogram(cpc_test,bins=hist_pedge)
                freq_cpc_test = hist_cpc_test/np.sum(hist_cpc_test)
            if test_ait_exist == 1:
                hist_ait_test,bins_test=np.histogram(ait_test,bins=hist_pedge)
                freq_ait_test = hist_ait_test/np.sum(hist_ait_test)
            if test_acc_exist == 1:
                hist_acc_test,bins_test=np.histogram(acc_test,bins=hist_pedge)
                freq_acc_test = hist_acc_test/np.sum(hist_acc_test)
            if test_ccn02_exist == 1:
                hist_ccn02_test,ccnbins_test=np.histogram(ccn02_test,bins=histccn_pedge)
                freq_ccn02_test = hist_ccn02_test/np.sum(hist_ccn02_test)
            if test_ccn05_exist == 1:
                hist_ccn05_test,ccnbins_test=np.histogram(ccn05_test,bins=histccn_pedge)
                freq_ccn05_test = hist_ccn05_test/np.sum(hist_ccn05_test)

            fig=plt.figure(figsize=(26,10))
            fsize=30;xysize=30;lsize=30
            gspec = GridSpec(ncols=2, nrows=1, figure=fig)
            ax1=fig.add_subplot(gspec[0])
            ax1.set_title(sites[0].upper()+' Aerosol Distribution (model)',fontsize=fsize)
            if test_cpc_exist == 1:
                ax1.bar(bins_test[:-1]+pvgap/5., freq_cpc_test, width = pvgap/5, color='k',align='edge',\
                                        label='Aerosol = '+'%3i' % np.nanmean(cpc_test)\
                                         +'$\pm$'+'%3i' % np.nanstd(cpc_test))
            if test_ait_exist == 1:
                ax1.bar(bins_test[:-1]+pvgap/5.*2, freq_ait_test, width = pvgap/5, color='blue',align='edge',\
                                        label='Aitken = '+'%3i' % np.nanmean(ait_test)\
                                         +'$\pm$'+'%3i' % np.nanstd(ait_test))
            if test_acc_exist == 1:
                ax1.bar(bins_test[:-1]+pvgap/5.*3, freq_acc_test, width = pvgap/5, color='darkviolet',align='edge',\
                                        label='Accumulation = '+'%3i' % np.nanmean(acc_test)\
                                         +'$\pm$'+'%3i' % np.nanstd(acc_test))
            ax1.set_xlim(0, pvmax_hist)
            #yup=(int(np.nanmax(freq_cpc_test)*10.)+1)/10.
            ax1.set_ylim(0,0.3)
            ax1.set_xlabel('Aerosol Num. Conc.($cm^{-3}$)',fontsize=fsize)
            ax1.set_ylabel('PDF',fontsize=fsize)
            ax1.tick_params(axis='x',labelsize=lsize,length=0,width=3,direction='in',which='major')
            ax1.tick_params(axis='y',labelsize=lsize,length=5,width=3,direction='out',which='major')
            #ax1.set_xticks(xbin)
            ax1.legend(loc='best',fontsize=lsize)
            for axis in ['top','bottom','left','right']:
                ax1.spines[axis].set_linewidth(3)
            #-----------------------------------------------
            ax1=fig.add_subplot(gspec[1])
            ax1.set_title(sites[0].upper()+' CCN Distribution (model)',fontsize=fsize)
            if test_ccn02_exist == 1:
                ax1.bar(ccnbins_test[:-1]+pvgap/4., freq_ccn02_test, width = pvgap/4, color='b',align='edge',\
                                        label='$CCN_{0.2SS}$ = '+'%3i' % np.nanmean(ccn02_test)\
                                         +'$\pm$'+'%3i' % np.nanstd(ccn02_test))
            if test_ccn05_exist == 1:
                ax1.bar(ccnbins_test[:-1]+pvgap/2., freq_ccn05_test, width = pvgap/4, color='r',align='edge',\
                                        label='$CCN_{0.5SS}$ = '+'%3i' % np.nanmean(ccn05_test)\
                                         +'$\pm$'+'%3i' % np.nanstd(ccn05_test))
            ax1.set_xlim(0, pvmax_hist_ccn)
            #yup=(int(np.nanmax([freq_ccn02_test,freq_ccn05_test])*10.)+1)/10.
            ax1.set_ylim(0,0.3)
            ax1.set_xlabel('Aerosol Num. Conc.($cm^{-3}$)',fontsize=fsize)
            ax1.set_ylabel('PDF',fontsize=fsize)
            ax1.tick_params(axis='x',labelsize=lsize,length=0,width=3,direction='in',which='major')
            ax1.tick_params(axis='y',labelsize=lsize,length=5,width=3,direction='out',which='major')
            #ax1.set_xticks(xbin)
            ax1.legend(loc='best',fontsize=lsize)
            for axis in ['top','bottom','left','right']:
                ax1.spines[axis].set_linewidth(3)
            plt.subplots_adjust(left = 0.07, right = 0.97, bottom = 0.10, top = 0.95,hspace=0.10) 
            plt.savefig(output_path+'/figures/'+sites[0]+'/'+'aerosol_all_distribution_hist_testmodel_'+sites[0]+'.png')
        #------------------------------------------------------------------------- 
        #-------------------------------------------------------------------------    
        #Bulk aerosol vs. ccn02
        if (test_cpc_exist == 1) and (test_ccn02_exist == 1):
            ratio_all = ccn02_test / cpc_test
            ratio_mean = np.nanmean(ratio_all) ; ratio_std = np.nanstd(ratio_all)

            fig=plt.figure(figsize=(12,10))

            fsize=30;xysize=30;lsize=20
            gspec = GridSpec(ncols=1, nrows=1, figure=fig)
            ax1=fig.add_subplot(gspec[0])
            ax1.set_title(sites[0].upper()+' Bulk Aerosol Activation (model)',fontsize=fsize)
            h2d02,xeg02,yeg02,im02 =plt.hist2d(cpc_test,ccn02_test,bins=[cpc_pedge,ccn02_pedge],cmap='turbo',density=True)
            ax1.plot([0,pvmax],[0,pvmax],'r',lw=3)
            ax1.text(0.02,0.9,'Ratio = '+'%.2f' % ratio_mean+'$\pm$'+'%.2f' % ratio_std,color='r',
                     ha='left', va='center', transform=ax1.transAxes,fontsize=xysize)
            ax1.set_xlabel('Aerosol Num. Conc. (# $cm^{-3}$)',fontsize=xysize)
            ax1.set_ylabel('CCN Num. Conc. @0.2%SS (# $cm^{-3}$)',fontsize=xysize)
            ax1.tick_params(labelsize=xysize,length=10,width=2,direction='out',which='major')
            ax1.tick_params(length=7,width=3,direction='out',which='minor')
            cb1=plt.colorbar()
            cb1.ax.tick_params(labelsize=13)
            cb1.set_label('Probability Density',fontsize=15)
            for axis in ['top','bottom','left','right']:
                    ax1.spines[axis].set_linewidth(2)
            plt.subplots_adjust(left = 0.16, right = 1.01, bottom = 0.11, top = 0.94,hspace=0.15)  
            plt.savefig(output_path+'/figures/'+sites[0]+'/'+'aerosol_activation_bulk_cpc_ccn02_testmodel_'+sites[0]+'.png')
        #------------------------------------------------------------------------- 
        #-------------------------------------------------------------------------    
        #Bulk aerosol vs. ccn05
        if (test_cpc_exist == 1) and (test_ccn02_exist == 1):
            ratio_all = ccn05_test / cpc_test
            ratio_mean = np.nanmean(ratio_all) ; ratio_std = np.nanstd(ratio_all)

            fig=plt.figure(figsize=(12,10))

            fsize=30;xysize=30;lsize=20
            gspec = GridSpec(ncols=1, nrows=1, figure=fig)
            ax1=fig.add_subplot(gspec[0])
            ax1.set_title(sites[0].upper()+' Bulk Aerosol Activation (model)',fontsize=fsize)
            h2d02,xeg02,yeg02,im02 =plt.hist2d(cpc_test,ccn05_test,bins=[cpc_pedge,ccn02_pedge],cmap='turbo',density=True)
            ax1.plot([0,pvmax],[0,pvmax],'r',lw=3)
            ax1.text(0.02,0.9,'Ratio = '+'%.2f' % ratio_mean+'$\pm$'+'%.2f' % ratio_std,color='r',
                     ha='left', va='center', transform=ax1.transAxes,fontsize=xysize)
            ax1.set_xlabel('Aerosol Num. Conc. (# $cm^{-3}$)',fontsize=xysize)
            ax1.set_ylabel('CCN Num. Conc. @0.5%SS (# $cm^{-3}$)',fontsize=xysize)
            ax1.tick_params(labelsize=xysize,length=10,width=2,direction='out',which='major')
            ax1.tick_params(length=7,width=3,direction='out',which='minor')
            cb1=plt.colorbar()
            cb1.ax.tick_params(labelsize=13)
            cb1.set_label('Probability Density',fontsize=15)
            for axis in ['top','bottom','left','right']:
                    ax1.spines[axis].set_linewidth(2)
            plt.subplots_adjust(left = 0.16, right = 1.01, bottom = 0.11, top = 0.94,hspace=0.15)  
            plt.savefig(output_path+'/figures/'+sites[0]+'/'+'aerosol_activation_bulk_cpc_ccn05_testmodel_'+sites[0]+'.png')
        #-------------------------------------------------------------------------
        #==========================================================================
    #==========================================================================
    #==========================================================================
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=    
