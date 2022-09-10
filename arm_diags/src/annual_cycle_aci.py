#===========================================================================================================================
# Program for generate annual/seasonal cycle & line plot from monthly data -- Original written by Dr. Chengzhu Zhang @ LLNL
#---------------------------------------------------------------------------------------------------------------------------
# V3 Development
    # ----------------------------------------------------------------------------------------------------
    # Xiaojian Zheng - Aug2022
    # ### modification based on annual_cycle.pro to accommodate the aci annual cycle metrics
    # ----------------------------------------------------------------------------------------------------

#===========================================================================================================================
import os
import pdb
import glob
import cdms2
import cdutil
import numpy as np
from numpy import genfromtxt
import csv
import matplotlib.pyplot as plt
from .varid_dict import varid_longname
from .taylor_diagram import TaylorDiagram
from .utils import climo

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def var_annual_cycle(var, seasons):
    "Calculate annual cycle climatology of each variable"
    var_season_data = np.empty([len(seasons)])*np.nan
    cdutil.setTimeBoundsMonthly(var)
    var_season_data = cdutil.ANNUALCYCLE.climatology(var)(squeeze=1)
    # convert units
    if var.id == 'tas':
        var_season_data = var_season_data-273.15

    if var.id == 'pr':
        var_season_data = var_season_data*3600.*24.
        
    return var_season_data

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def annual_cycle_aci_data(parameter):
    """Calculate annual cycle climatology"""
    variables = parameter.variables
    seasons = parameter.season
    test_path = parameter.test_data_path
    obs_path = parameter.obs_path
    cmip_path = parameter.cmip_path
    output_path = parameter.output_path
    sites = parameter.sites
   
    test_model = parameter.test_data_set 
    ref_models = parameter.ref_models

    arm_name = parameter.arm_filename

    cmip_ver = cmip_path.split('/')[-1]

    #------------------------------------------
    # define controlling index
    test_index = 0
    cmip_index = 0
    #------------------------------------------
    print('============================================================')
    print('Create Annual Cycles: '+sites[0])
    print('============================================================')

    # Calculate for test model
    test_var_season=np.empty([len(variables),len(seasons)])*np.nan
    if not arm_name:
        test_file = glob.glob(os.path.join(test_path,'*'+test_model+'*acimo*' + sites[0]+'.nc' )) #read in monthly test data
    else:
        test_model = ''.join(e for e in test_model if e.isalnum()).lower()
#         print(test_path,test_model,sites[0][:3]+test_model+'mon' + sites[0][3:5].upper())
        test_file = glob.glob(os.path.join(test_path,sites[0][:3]+test_model+'acimon' + sites[0][3:5].upper()+'*.nc' )) #read in monthly test data
    print('test_file',test_file)
        

#     if len(test_file) == 0:
#        raise RuntimeError('No monthly data for test model were found.')
    try:
        fin = cdms2.open(test_file[0])

        print(('test_model',test_model))

        for j, variable in enumerate(variables): 
            try:
                var = fin(variable)
                #test_var_season[j, :] = var_annual_cycle(var, seasons)
                test_var_season[j, :] = climo(var, 'ANNUALCYCLE')
                print(('after', test_var_season[j, :]))

            except:
                print((variable+" not processed for " + test_model))
        fin.close()
        test_index = 1
    except:
        print('No monthly ACI data for test model were found.')

    # Calculate for observational data (specified by the ACI data structure)
    obs_var_season=np.empty([len(variables),len(seasons),2])*np.nan
    print('ARM data',sites[0])
    # read in the monthly data for target site, format unified [XZ]
    obs_file = glob.glob(os.path.join(obs_path,sites[0][:3]+'armdiagsaciclim' + sites[0][3:5].upper()+'*c1.nc')) #read in monthly data
    print('obs_file',obs_file)
    fin = cdms2.open(obs_file[0])
    for j, variable in enumerate(variables): 
        try:
            var = fin(variable)
            #obs_var_season[j, :] = climo(var, 'ANNUALCYCLE')
            obs_var_season[j, :, 0] = var[:,0] #mean
            obs_var_season[j, :, 1] = var[:,1] #std
        except:  
            print((variable+" not processed for obs"))
    fin.close()
  
    # Calculate cmip model seasonal mean climatology
    cmip_var_season=np.empty([len(ref_models),len(variables),len(seasons)])*np.nan
    for i, ref_model in enumerate(ref_models):
        
        if not arm_name:
            ref_file = glob.glob(os.path.join(cmip_path,'*'+ref_model+'*acimo*'+ sites[0]+'.nc')) #read in monthly cmip data
        else:
            ref_model = cmip_ver +''.join(e for e in ref_model if e.isalnum()).lower()
            ref_file = glob.glob(os.path.join(cmip_path,sites[0]+'/'+sites[0][:3]+ref_model+'acimon' + sites[0][3:5].upper()+'*.nc' )) #read in monthly test data
            
            print('ref_file',ref_file, ref_model,sites[0][:3]+ref_model+'acimon' + sites[0][3:5].upper())
        print(('ref_model', ref_model))

        if len(ref_file) == 0:
            print((ref_model+" not found!"))
        else:
            fin = cdms2.open(ref_file[0])

            for j, variable in enumerate(variables): 
                try:
                    var = fin(variable)
                    #cmip_var_season[i, j, :] = var_annual_cycle(var, seasons)
                    tmpvarannual = climo(var, 'ANNUALCYCLE')
                    lnn=np.where(tmpvarannual == 0)[0]
                    if len(lnn) == 12: tmpvarannual[:]=np.nan #set to missing if model output is invalid
                    cmip_var_season[i, j, :] = tmpvarannual.copy()
                    print((ref_model,cmip_var_season[i, j, :]))
                except:
                    print((variable+" not processed for " + ref_model))
            fin.close()
    # Calculate multi-model mean
    mmm_var_season =  np.nanmean(cmip_var_season,axis=0)
    cmip_index = 1
    # If none of the CMIP is valid, cease the table output
    if len(np.where(np.isfinite(mmm_var_season))[0]) == 0:
        cmip_index = 0
        print('No monthly ACI data for CMIP models were found.')
        
    # Save data in csv format in metrics folder
    # Generate new folder given site names [XZ]:
    if not os.path.exists(os.path.join(output_path,'metrics',sites[0])):
        os.makedirs(os.path.join(output_path,'metrics',sites[0])) 
    for j, variable in enumerate(variables):
        if test_index == 1: np.savetxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_test_annual_cycle_'+sites[0]+'.csv',test_var_season[j,:])
        if cmip_index == 1: 
            np.savetxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_mmm_annual_cycle_'+sites[0]+'.csv',mmm_var_season[j,:])
            np.savetxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_cmip_annual_cycle_'+sites[0]+'.csv',cmip_var_season[:,j,:])
        np.savetxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_obs_annual_cycle_'+sites[0]+'.csv',obs_var_season[j,:,0])

        # Reference standard deviation
        data = obs_var_season[j,:,0]
        refstd = data.std(ddof=1)           # Reference standard deviation
        x=np.arange(len(seasons))

        # Compute and save stddev and correlation coefficient of models,for taylor diagram
        if test_index == 1:
            test_sample=np.array([test_var_season[j,:].std(ddof=1), np.corrcoef(data, test_var_season[j,:])[0,1]])
            np.savetxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_test_annual_cycle_std_corr_'+sites[0]+'.csv',test_sample)
        if cmip_index == 1:
            mod_num=len(ref_models)
            m_all=[cmip_var_season[x,j,:] for x in range(mod_num)]
            cmip_samples = np.array([[m.std(ddof=1), np.corrcoef(data, m)[0,1]] for m in m_all])
            mmm_sample=np.array([mmm_var_season[j,:].std(ddof=1), np.corrcoef(data,mmm_var_season[j,:])[0,1]])
            np.savetxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_mmm_annual_cycle_std_corr_'+sites[0]+'.csv',mmm_sample)
            np.savetxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_cmip_annual_cycle_std_corr_'+sites[0]+'.csv',cmip_samples)
            
        obs_sample=np.array([refstd,1.0])
        np.savetxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_obs_annual_cycle_std_corr_'+sites[0]+'.csv',obs_sample)
        
        
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def annual_cycle_aci_line_plot(parameter):
    """Calculate annual cycle climatology"""
    variables = parameter.variables
    seasons = parameter.season
    output_path = parameter.output_path
    sites = parameter.sites
    #------------------------------------------
    # define controlling index
    test_index = 0
    cmip_index = 0
    #------------------------------------------
    if not os.path.exists(os.path.join(output_path,'figures',sites[0])):
        os.makedirs(os.path.join(output_path,'figures',sites[0])) 

    var_longname = [ varid_longname[x] for x in variables]
    for j, variable in enumerate(variables):
        try:
            test_data = genfromtxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_test_annual_cycle_'+sites[0]+'.csv')
            test_index = 1
        except:
            print('No test model monthly ACI data metrics found')
        try:
            mmm_data = genfromtxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_mmm_annual_cycle_'+sites[0]+'.csv')
            cmip_data = genfromtxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_cmip_annual_cycle_'+sites[0]+'.csv')
            mod_num = cmip_data.shape[0]
            cmip_index = 1
        except:
            mod_num = 0
            print('No CMIP model monthly ACI data metrics found')
        obs_data = genfromtxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_obs_annual_cycle_'+sites[0]+'.csv')
        
        # Start Plotting
        fig = plt.figure()# Create figure
        ax  =fig.add_axes([0.12, 0.12, 0.82, 0.81]) # Create axes
        xax =  np.arange (1,13,1)
        if cmip_index == 1:
            for mod_ind in range(mod_num):
                ax.plot(xax,cmip_data[mod_ind,:],'grey',lw=1)
            ann_mean=np.mean(mmm_data[:])
            ax.plot(xax,mmm_data[:],'b',label='MMM: %.2f'%ann_mean,lw=3)
        if test_index == 1:
            ann_mean=np.mean(test_data[:])
            ax.plot(xax,test_data[:],'r',label='MOD: %.2f'%ann_mean,lw=3)
        ann_mean=np.mean(obs_data[:])
        ax.plot(xax,obs_data[:],marker='o', color='black', ms=5,label='OBS: %.2f'%ann_mean,lw=3)

        #my_xticks = ['J','F','M','A','M','J','J','A','S','O','N','D']
        my_xticks = seasons
        plt.xticks(xax, my_xticks)
        plt.xlim(1,12)
        if sites[0] == 'sgpc1':
            if variable == 'cpc': plt.ylim(2000,5000)
            if variable[0:3] == 'ccn': plt.ylim(0,2000)
            if variable == 'cod': plt.ylim(0,50)
        if sites[0] == 'enac1':
            if variable == 'cpc': plt.ylim(0,1000)
            if variable[0:3] == 'ccn': plt.ylim(0,400)
            if variable == 'cod': plt.ylim(0,50)
        plt.title('Annual Cycle: Model vs OBS vs CMIP',fontsize=15)
        plt.xlabel('Month',fontsize=15)
        plt.legend(loc='best',prop={'size':12})
        plt.ylabel(var_longname[j])
        #special notes for models mistreating surface type [XZ]:
#         if (variable == 'hfls') or (variable == 'hfss') or (variable == 'rsus'):
#             if (sites[0] == 'enac1') or (sites[0] == 'twpc1') or (sites[0] == 'twpc2') or (sites[0] == 'twpc3'):
#                 ax.text(0.5, 0.05,'Note: the selected grid points were ocean grids in most GCMs', ha='center', va='center', transform=ax.transAxes,fontsize=8)
        # save figures
        figname = variable+'_annual_cycle_'+sites[0]+'.png'
        if (variable[0] != 'c'):
            figname = 'chemical_'+variable+'_annual_cycle_'+sites[0]+'.png'
        fig.savefig(output_path+'/figures/'+sites[0]+'/'+figname)
        plt.close('all')


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def annual_cycle_aci_taylor_diagram(parameter):
    """Calculate annual cycle climatology"""
    variables = parameter.variables
    seasons = parameter.season
    output_path = parameter.output_path
    sites = parameter.sites
    #------------------------------------------
    # define controlling index
    test_index = 0
    cmip_index = 0
    #------------------------------------------
    if not os.path.exists(os.path.join(output_path,'figures',sites[0])):
        os.makedirs(os.path.join(output_path,'figures',sites[0])) 

    var_longname = [ varid_longname[x] for x in variables]
    for j, variable in enumerate(variables):
        try:
            test_data = genfromtxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_test_annual_cycle_std_corr_'+sites[0]+'.csv')
            test_index = 1
        except:
            print('No test model monthly ACI data metrics found')
        try:
            mmm_data = genfromtxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_mmm_annual_cycle_std_corr_'+sites[0]+'.csv')
            cmip_data = genfromtxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_cmip_annual_cycle_std_corr_'+sites[0]+'.csv')
            mod_num = cmip_data.shape[0]   
            cmip_index = 1
        except:
            mod_num = 0
            print('No CMIP model monthly ACI data metrics found')
        obs_data = genfromtxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_obs_annual_cycle_std_corr_'+sites[0]+'.csv')
        
        # observational annual mean must be valid for taylor diagram [XZ]
        if np.isfinite(obs_data[0]):
            try:
                fig = plt.figure(figsize=(8,8))
                refstd = obs_data[0]
                dia = TaylorDiagram(refstd, fig=fig,rect=111, label="Reference")

                # Add samples to Taylor diagram
                if cmip_index == 1:
                    for i,(stddev,corrcoef) in enumerate(cmip_data):
                        dia.add_sample(stddev, corrcoef, marker='.',ms=10, c='grey')
                    dia.add_sample(mmm_data[0], mmm_data[1],marker='.',ms=15, c='b',label='MMM')
                if test_index == 1:
                    dia.add_sample(test_data[0], test_data[1],marker='.',ms=15, c='red',label='MOD')

                # Add RMS contours, and label them
                contours = dia.add_contours(colors='0.5')
                plt.clabel(contours, inline=1, fontsize=10)
                plt.title(var_longname[j])

                # Add a figure legend
                if (cmip_index + test_index) == 0:
                    lg_item = [dia.samplePoints[0]]
                if (cmip_index + test_index) == 1:
                    lg_item = [dia.samplePoints[0],dia.samplePoints[-1]]
                if (cmip_index + test_index) == 2:
                    lg_item = [dia.samplePoints[0],dia.samplePoints[-2],dia.samplePoints[-1]]
                fig.legend( lg_item,
                           [ p.get_label() for p in lg_item ],
                           numpoints=1,  loc='upper right',prop={'size':10})
#                np.savetxt(basedir+'metrics/'+vas[va_ind]+'_'+mod+'std_corr.csv',mod_sample,fmt='%.3f')
                figname = variable+'_annual_cycle_taylor_diagram_'+sites[0]+'.png'
                if (variable[0] != 'c'):
                    figname = 'chemical_'+variable+'_annual_cycle_taylor_diagram_'+sites[0]+'.png'
                fig.savefig(output_path+'/figures/'+sites[0]+'/'+figname)
                plt.close('all')
            except:    
                print(('Taylor diagram not generated for ' +variable+': plotting error'))
        else:
            print(('Taylor diagram not generated for ' +variable+': observation annual mean not valid'))
    
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=    
    
    
