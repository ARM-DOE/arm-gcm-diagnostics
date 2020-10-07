import os
import glob
import cdms2
import cdutil
import numpy as np
from numpy import genfromtxt
import csv
import matplotlib.pyplot as plt
from .varid_dict import varid_longname


def annual_cycle_zt_data(parameter):
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

    # Calculate for test model
    month = seasons#['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
#    test_var_season=np.empty([len(variables),len(seasons)])*np.nan
    if not arm_name:
        test_file = glob.glob(os.path.join(test_path,'*'+test_model+'*diurnal*'+ sites[0]+'.nc')) #read in monthly test data
    else:
        test_model = ''.join(e for e in test_model if e.isalnum()).lower()
        print(test_path,test_model,sites[0][:3]+test_model+'diurnalclim' + sites[0][3:5].upper())
        test_file = glob.glob(os.path.join(test_path,sites[0][:3]+test_model+'diurnalclim' + sites[0][3:5].upper()+'*.nc' ))

    if len(test_file) == 0:
       raise RuntimeError('No monthly data for test model were found.')

    fin = cdms2.open(test_file[0])
    print(('test_model',test_model))
    for j, variable in enumerate(variables): 
        try:
            if variable == 'cl' or variable == 'cl_p':
                var = fin ('cl_p')
            else:
                var = fin(variable)
            var[var>100]=np.nan
            var_2d = np.reshape(var,(12,8,37))
    
            with open(output_path+'/metrics/'+variable+'_test_diurnal_climo_'+ sites[0]+'.csv', 'w') as outfile:
                outfile.write('# Array shape: {0}'.format(var_2d.shape)+' as (month, hours, vertical levels)\n')
                mon_id=0
                for data_slice in var_2d:
                    #outfile.write('# New slice\n')
                    outfile.write('#'+month[mon_id]+' slice\n')
                    np.savetxt(outfile, data_slice, fmt='%-7.2f')
                    mon_id=mon_id+1
        except:
            print((variable+" not processed for " + test_model))

    fin.close()
    

    # Calculate for observational data
    if sites[0] == 'sgp':
    #    obs_var_season=np.empty([len(variables),len(seasons)])*np.nan
        if not arm_name:
            obs_file = glob.glob(os.path.join(obs_path,'*ARMdiag_c1_diurnal_climo_'+ sites[0]+'*.nc')) #read in monthly test data
        else:
            obs_file = glob.glob(os.path.join(obs_path,'sgparmdiagsmondiurnalclimC1.c1.nc'))
        #obs_file = glob.glob(os.path.join(obs_path,'*ARMdiag_c1_ARSCL_ACRED_diurnal_climo*.nc')) #read in monthly test data
    else:
        
        if not arm_name:
            obs_file = glob.glob(os.path.join(obs_path,'*ARMdiag_*_diurnal_climo_'+ sites[0]+'*.nc')) 
        else:
            obs_file = glob.glob(os.path.join(obs_path,sites[0][:3]+'armdiagsmondiurnalclim' + sites[0][3:5].up()+'*.nc'))

    print(('ARM data', sites[0]))
    fin = cdms2.open(obs_file[0])
    for j, variable in enumerate(variables): 
        try:
            var = fin (variable)
            var[var>100]=np.nan
#            if sites[0] == 'sgp':
#                var_2d = np.reshape(var,(12,24,37))
#            print var_2d.shape
            var_2d = np.reshape(var,(12,24,37))
    
            with open(output_path+'/metrics/'+variable+'_obs_diurnal_climo_'+ sites[0]+'.csv', 'w') as outfile:
                outfile.write('# Array shape: {0}'.format(var_2d.shape)+' as (month, hours, vertical levels)\n')
                mon_id=0
                for data_slice in var_2d:
                    #outfile.write('# New slice\n')
                    outfile.write('#'+month[mon_id]+' slice\n')
                    np.savetxt(outfile, data_slice, fmt='%-7.2f')
                    mon_id=mon_id+1
    
    
        except:
            print((variable+" not processed for obs"))
    fin.close()
#    else:
#        obs_file = glob.glob(os.path.join(obs_path,'*ARMdiag_domain_monthly_climo_'+ sites[0]+'*.nc')) #read in monthly test data
#        #obs_file = glob.glob(os.path.join(obs_path,'*ARMdiag_c1_ARSCL_ACRED_diurnal_climo*.nc')) #read in monthly test data
#        print 'ARM data'
#        print sites[0]
#        fin = cdms2.open(obs_file[0])
#        for j, variable in enumerate(variables):
#            try:
#                var = fin (variable)
#                var[var>100]=np.nan
#                #if sites[0] == 'sgp':
#                #    var_2d = np.reshape(var,(12,24,37))
#                print var.shape
#                np.savetxt(output_path+'/metrics/'+variable+'_obs_annual_cycle_'+sites[0]+'.csv',var)
#    
#            except:
#                print (variable+" not processed for obs")
#        fin.close()
         


def annual_cycle_zt_plot(parameter):
    """Prepare annual cycle and diurnal cycle plots of cloud fraction fro set 3 and set 5 diag"""
    variables = parameter.variables
    seasons = parameter.season
    output_path = parameter.output_path
    sites = parameter.sites

    month=seasons#['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    for j, variable in enumerate(variables):
        test_data = np.loadtxt(output_path+'/metrics/'+variable+'_test_diurnal_climo_'+ sites[0]+'.csv')
        test_data = test_data.reshape((12,8,37))

        cl_p=np.nanmean(test_data,axis=1)
        cl_p_diurnal=np.nanmean(test_data,axis=0)
        cl_p_ann=np.nanmean(cl_p,axis=0)
#        mmm_data = genfromtxt(output_path+'/metrics/'+variable+'_mmm_annual_cycle.csv')
#    if sites[0]=='sgp':
        obs_data = np.loadtxt(output_path+'/metrics/'+variable+'_obs_diurnal_climo_'+ sites[0]+'.csv')
        obs_data = obs_data.reshape((12,24,37))
#        cmip_data = genfromtxt(output_path+'/metrics/'+variable+'_cmip_annual_cycle.csv')

        cl_ob=np.nanmean(obs_data,axis=1)
        cl_ob_diurnal=np.nanmean(obs_data,axis=0)
        cl_ob_ann=np.nanmean(cl_ob,axis=0)
#        else:
#            obs_data = np.loadtxt(output_path+'/metrics/'+variable+'_obs_annual_cycle_'+ sites[0]+'.csv')
#            cl_ob = obs_data
#            cl_ob_ann=np.nanmean(cl_ob,axis=0)
#            print cl_ob_ann.shape
        ####################Monthly Mean Diurnal Cycle

#    if sites[0] == 'sgp':
        for index in range(2):
            fig1, axs = plt.subplots(4,3, figsize=(15, 12), facecolor='w', edgecolor='k',sharex=True,sharey=True)
            fig1.subplots_adjust(hspace = .3, wspace=.1)
            axs = axs.ravel()
            for imon in range(12):
                if index==0:
                     title='obs_'+variable+'_mon_diurnal_clim'
                     yy=np.linspace(0,23,24)
                     xx=np.linspace(100,1000,37)
                     x,y=np.meshgrid(xx,yy)
                     obs_data_con=np.concatenate((obs_data[imon,:,:],obs_data[imon,:,:]),axis=0)#6 hour GMT to Local time
                     im=axs[imon].pcolormesh(y,x,obs_data_con[6:30,::-1], vmin=0, vmax=25)
                     #im=axs[imon].pcolormesh(y,x,obs_data_con[:24,::-1], vmin=0, vmax=25)
                     plt.xlim([0,23])
                     xax =  np.arange (0,24,3)
                     my_xticks = ['0','3','6','9','12','15','18','21']

                else:
                     title='mod_'+variable+'_mon_diurnal_clim'
                     yy=np.linspace(0,7,8)
                     xx=np.linspace(100,1000,37)
                     x,y=np.meshgrid(xx,yy)
                     obs_data_con=np.concatenate((test_data[imon,:,:],test_data[imon,:,:]),axis=0)
                     #Starting time is 3:00:00 GTM, +3 hour GMT to Local time
                     #NEED TO SWTCH TO LOCAL TIME model data!!!!
                     im=axs[imon].pcolormesh(y,x,obs_data_con[1:9,::-1], vmin=0, vmax=25)
                     plt.xlim([0,7])
                     xax =  np.arange (0,8,1)
                     my_xticks = ['0','3','6','9','12','15','18','21']

                axs[imon].set_title(month[imon])
                plt.xticks(xax, my_xticks)
                plt.setp(axs[imon].get_xticklabels(), visible=True)

            for ax in axs[9:12]:
                ax.set_xlabel('Local time (hr)')
            for ax in axs[::3]:
                ax.set_ylabel('Pressure (mb)')
            axs[0].invert_yaxis()
            plt.suptitle(title)
            fig1.subplots_adjust(right=0.8)
            cbar_ax = fig1.add_axes([0.85, 0.15, 0.05, 0.7])
            fig1.colorbar(im, cax=cbar_ax)
            plt.title('cl (%)')
            fig1.savefig(output_path+'/figures/'+title+'_'+sites[0]+'.png')
            plt.close('all')

        ##########################Diurnal cycle
        for index in range(2):
            fig2 = plt.figure()# Create figure
            ax  =fig2.add_axes([0.15, 0.15, 0.65, 0.75]) # Create axes
            if index==0:
                 title='obs_'+variable+'_diurnal_clim'
                 yy=np.linspace(0,23,24)
                 xx=np.linspace(100,1000,37)
                 x,y=np.meshgrid(xx,yy)
                 obs_data_con=np.concatenate((cl_ob_diurnal,cl_ob_diurnal),axis=0)#6 hour GMT to Local time
                 im=ax.pcolormesh(y,x,obs_data_con[6:30,::-1], vmin=0, vmax=25)
                 plt.xlim([0,23])
                 xax =  np.arange (0,24,3)
                 my_xticks = ['0','3','6','9','12','15','18','21']

            else:
                 title='mod_'+variable+'_diurnal_clim'
                 yy=np.linspace(0,7,8)
                 xx=np.linspace(100,1000,37)
                 x,y=np.meshgrid(xx,yy)
                 obs_data_con=np.concatenate((cl_p_diurnal,cl_p_diurnal),axis=0)
                 #Starting time is 3:00:00 GTM, +3 hour GMT to Local time
                 im=ax.pcolormesh(y,x,obs_data_con[1:9,::-1], vmin=0, vmax=25)
                 plt.xlim([0,7])
                 xax =  np.arange (0,8,1)
                 my_xticks = ['0','3','6','9','12','15','18','21']

            plt.xticks(xax, my_xticks)
            plt.ylabel('Pressure (mb)')
            plt.xlabel('Local time (hr)')
            plt.gca().invert_yaxis()
            plt.suptitle(title)
            cbar_ax = fig2.add_axes([0.85, 0.15, 0.05, 0.75])
            fig2.colorbar(im, cax=cbar_ax)
            plt.title('cl (%)')
            fig2.savefig(output_path+'/figures/'+title+'_'+sites[0]+'.png')
        #    
            plt.close('all')
    ##########################Annual cycle

    yy=np.linspace(0,11,12)
    xx=np.linspace(100,1000,37)
    x,y=np.meshgrid(xx,yy)
    for index in range(3):
        fig = plt.figure()# Create figure
        ax  =fig.add_axes([0.15, 0.15, 0.65, 0.75]) # Create axes
        if index==0:
            title='mod_'+variable+'_annual_cycle_clim_'+sites[0]
            im=ax.pcolormesh(y,x,cl_p[:,::-1], vmin=0, vmax=25)
        elif index==1:
            im=ax.pcolormesh(y,x,cl_ob[:,::-1], vmin=0, vmax=25)
            title='obs_'+variable+'_annual_cycle_clim_'+sites[0]
        elif index==2:
            im=ax.pcolormesh(y,x,cl_p[:,::-1]-cl_ob[:,::-1], vmin=-10, vmax=10)
            title='diff_'+variable+'_annual_cycle_clim_'+sites[0]
        xax =  np.arange (0,12,1)
        my_xticks = ['J','F','M','A','M','J','J','A','S','O','N','D']
        plt.xticks(xax, my_xticks)
        plt.xlim(0,11)
        plt.ylabel('Pressure (mb)')
        plt.gca().invert_yaxis()
        plt.suptitle(title)
        cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.75])
        fig.colorbar(im, cax=cbar_ax)
        plt.title('cl (%)')
        fig.savefig(output_path+'/figures/'+title+'.png')
    #    
        plt.close('all')
    ###########################Seasonal Mean
    levels=xx
    seasons=['MAM','JJA','SON','DJF']
    cl_p2=np.concatenate((cl_p,cl_p),axis=0)
    cl_ob2=np.concatenate((cl_ob,cl_ob),axis=0)
    for index in range(len(seasons)):

        fig3 = plt.figure()# Create figure
        ax  =fig3.add_axes([0.15, 0.1, 0.8, 0.8]) # Create axes
        ax.plot(np.nanmean(cl_p2[index*3+2:(index+1)*3+2,::-1],axis=0),levels,'r',lw=3,label='MOD')
        ax.plot(np.nanmean(cl_ob2[index*3+2:(index+1)*3+2,::-1],axis=0),levels,'k',lw=3,label='OBS')
        plt.gca().invert_yaxis()
        plt.ylabel('Pressure (mb)')
        plt.xlabel('Cloud fraction (%)')
        plt.xlim([0,25])
        plt.legend(loc='best',prop={'size':15})
        plt.title(seasons[index]+' Mean Cloud Fraction')
        fig3.savefig(output_path+'/figures/'+seasons[index]+'_'+variable+'_diff_'+sites[0]+'.png')
        plt.close('all')

    ###########################ANN Mean


    fig0 = plt.figure()# Create figure
    ax  =fig0.add_axes([0.15, 0.1, 0.8, 0.8]) # Create axes
    ax.plot(cl_p_ann[::-1],levels,'r',lw=3,label='MOD')
    ax.plot(cl_ob_ann[::-1],levels,'k',lw=3,label='OBS')
    plt.gca().invert_yaxis()
    plt.ylabel('Pressure (mb)')
    plt.xlabel('Cloud fraction (%)')
    plt.xlim([0,25])
    plt.legend(loc='best',prop={'size':15})
    plt.title('Annual Mean Cloud Fraction')
    fig0.savefig(output_path+'/figures/ANN_'+variable+'_diff_'+sites[0]+'.png')
    plt.close('all')

