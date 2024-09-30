#===========================================================================================================================
# Program for generate annual/seasonal cycle & 2D plot from monthly data -- Original written by Dr. Chengzhu Zhang @ LLNL
#---------------------------------------------------------------------------------------------------------------------------
# V3 Development
    # ---------------------------------------------------------------------------------------
    # Xiaojian Zheng - Nov-Dec 2021
    # ### unify the data extraction and process code for all the ARM sites
    # ### change the input/output format to site-dependent
    # ### change the 2D plots from color-mesh to color-contour
    # ### change the default treatments when test model not found
    # ---------------------------------------------------------------------------------------
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

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
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

    print('============================================================')
    print('Create CF Vertical Profiles: '+sites[0])
    print('============================================================')

    # Generate new folder given site names [XZ]:
    if not os.path.exists(os.path.join(output_path,'metrics',sites[0])):
        os.makedirs(os.path.join(output_path,'metrics',sites[0]))

    # Calculate for test model
    test_findex = 0 #preset of test model indicator
    month = seasons#['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
#    test_var_season=np.empty([len(variables),len(seasons)])*np.nan
    if not arm_name:
        test_file = glob.glob(os.path.join(test_path,'*'+test_model+'*diurnal*'+ sites[0]+'.nc')) #read in monthly test data
    else:
        test_model = ''.join(e for e in test_model if e.isalnum()).lower()
        print(test_path,test_model,sites[0][:3]+test_model+'diurnalclim' + sites[0][3:5].upper())
        test_file = glob.glob(os.path.join(test_path,sites[0][:3]+test_model+'diurnalclim' + sites[0][3:5].upper()+'*.nc' ))

    if len(test_file) == 0:
       print('No climatology data for test model were found: '+sites[0])

    #test model exist
    if len(test_file) > 0: 
        test_findex = 1 

        fin = cdms2.open(test_file[0])
        print(('Processing climatology data for test_model',test_model))
        for j, variable in enumerate(variables): 
            try:
                if variable == 'cl' or variable == 'cl_p':
                    var = fin ('cl_p')
                else:
                    var = fin(variable)
                var[var>100]=np.nan
                len_var=var.shape[0]
                #auto-detect the testmodel frequency
                var_2d = np.reshape(var,(12,int(len_var/12.),37))    
    
                with open(output_path+'/metrics/'+sites[0]+'/'+variable+'_test_diurnal_climo_'+ sites[0]+'.csv', 'w') as outfile:
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
    # read in the monthly data for target site, format unified [XZ]
    if not arm_name:
        obs_file = glob.glob(os.path.join(obs_path,'*ARMdiag_*_diurnal_climo_'+ sites[0]+'*.nc')) #read in monthly test data
    else:
        obs_file = glob.glob(os.path.join(obs_path,sites[0][:3]+'armdiagsmondiurnalclim' + sites[0][3:5].upper()+'*c1.nc'))

    print(('ARM data', sites[0]))
    fin = cdms2.open(obs_file[0])
    for j, variable in enumerate(variables): 
        try:
            var = fin (variable)
            var[var>100]=np.nan #for cloud fraction set Value>100 to NaN
#            if sites[0] == 'sgp':
#                var_2d = np.reshape(var,(12,24,37))
#            print var_2d.shape
            var_2d = np.reshape(var,(12,24,37))
    
            with open(output_path+'/metrics/'+sites[0]+'/'+variable+'_obs_diurnal_climo_'+ sites[0]+'.csv', 'w') as outfile:
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
         
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def annual_cycle_zt_plot(parameter):
    """Prepare annual cycle and diurnal cycle plots of cloud fraction fro set 3 and set 5 diag"""
    variables = parameter.variables
    seasons = parameter.season
    output_path = parameter.output_path
    sites = parameter.sites

    if not os.path.exists(os.path.join(output_path,'figures',sites[0])):
        os.makedirs(os.path.join(output_path,'figures',sites[0])) 

    # check test file
    test_findex = 0 #preset of test model indicator
    test_file = glob.glob(output_path+'/metrics/'+sites[0]+'/'+'cl_p_test_diurnal_climo_'+ sites[0]+'.csv')
    if len(test_file) == 0:
       print('No test model plotted for cl_p: '+sites[0])
    
    if len(test_file) > 0: 
        test_findex = 1   #test model exist

    month=seasons#['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    month_legend = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

    for j, variable in enumerate(variables):

        # process test model data
        if test_findex == 1:
            test_data = np.loadtxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_test_diurnal_climo_'+ sites[0]+'.csv')
            #auto-detect the testmodel frequency
            len_var=test_data.shape[0]
            tlen_testVar=int(len_var/12.)  #e.g., 24  or 8
            tlen_testGap=24/tlen_testVar   #e.g., 1hr or 3hr

            test_data = test_data.reshape((12,tlen_testVar,37))

            cl_p=np.nanmean(test_data,axis=1)
            cl_p_diurnal=np.nanmean(test_data,axis=0)
            cl_p_ann=np.nanmean(cl_p,axis=0)

        # process observation data
        obs_data = np.loadtxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_obs_diurnal_climo_'+ sites[0]+'.csv')
        obs_data = obs_data.reshape((12,24,37))

        cl_ob=np.nanmean(obs_data,axis=1)
        cl_ob_diurnal=np.nanmean(obs_data,axis=0)
        cl_ob_ann=np.nanmean(cl_ob,axis=0)

        #pdb.set_trace()
        #################### Monthly Mean Diurnal Cycle Contours
        #---------------------------------------------- 
        # define site-dependent contour levels [XZ]
        if sites[0] == 'sgpc1': ct_lo=0; ct_up=25.5; locoff=6
        if sites[0] == 'nsac1': ct_lo=0; ct_up=50.5; locoff=8
        if sites[0] == 'enac1': ct_lo=0; ct_up=35.5; locoff=1
        if sites[0] == 'twpc1': ct_lo=0; ct_up=70.5; locoff=14
        if sites[0] == 'twpc2': ct_lo=0; ct_up=70.5; locoff=12
        if sites[0] == 'twpc3': ct_lo=0; ct_up=60.5; locoff=15
        if sites[0] == 'maom1': ct_lo=0; ct_up=80.5; locoff=4
        # define plotting controller [XZ]
        if test_findex == 0: index_list = np.arange(1); ct_up=np.nanmax(obs_data.flatten())
        if test_findex == 1: index_list = np.arange(2); ct_up=np.nanmax(np.concatenate((obs_data.flatten(),test_data.flatten()),axis=0))
        rlevel=np.arange(ct_lo,ct_up+1,0.5)
        #---------------------------------------------- 
        #plotting contours
        for iid,index in enumerate(index_list):
            fig1, axs = plt.subplots(4,3, figsize=(15, 12), facecolor='w', edgecolor='k',sharex=True,sharey=True)
            fig1.subplots_adjust(hspace = .3, wspace=.1)
            axs = axs.ravel()
            for imon in range(12):
                if index==0:
                     title=variable+'_mon_diurnal_clim_obs'
                     yy=np.linspace(0,23,24)
                     xx=np.linspace(100,1000,37)
                     x,y=np.meshgrid(xx,yy)
                     obs_data_con=np.concatenate((obs_data[imon,:,:],obs_data[imon,:,:]),axis=0)#6 hour GMT to Local time
                     im=axs[imon].contourf(y,x,obs_data_con[locoff:locoff+24,::-1],cmap='jet',levels=rlevel)
                     #im=axs[imon].pcolormesh(y,x,obs_data_con[6:30,::-1], vmin=0, vmax=25)
                     #im=axs[imon].pcolormesh(y,x,obs_data_con[:24,::-1], vmin=0, vmax=25)
                     plt.xlim([0,23])
                     xax =  np.arange (0,24,3)
                     my_xticks = ['0','3','6','9','12','15','18','21']

                else:
                     title=variable+'_mon_diurnal_clim_mod'
                     yy=np.linspace(0,tlen_testVar-1,tlen_testVar)
                     xx=np.linspace(100,1000,37)
                     x,y=np.meshgrid(xx,yy)
                     test_data_con=np.concatenate((test_data[imon,:,:],test_data[imon,:,:]),axis=0)
                     #Starting time is 3:00:00 GTM, +3 hour GMT to Local time
                     #NEED TO SWTCH TO LOCAL TIME model data!!!!
                     if tlen_testGap == 3: #if the test model is 3-hourly
                         test_pstart = round(locoff/tlen_testGap)-1
                         if test_pstart < 0: test_pstart=int(0)
                         im=axs[imon].contourf(y,x,test_data_con[test_pstart:test_pstart+8,::-1],cmap='jet',levels=rlevel)
                     if tlen_testGap == 1: #if the test model is 1-hourly
                         im=axs[imon].contourf(y,x,test_data_con[locoff:locoff+24,::-1],cmap='jet',levels=rlevel)
                     #im=axs[imon].pcolormesh(y,x,test_data_con[1:9,::-1], vmin=0, vmax=25)
                     plt.xlim([0,tlen_testVar-1])
                     xax =  np.arange (0,tlen_testVar,int(tlen_testVar/8))
                     my_xticks = ['0','3','6','9','12','15','18','21']

                axs[imon].set_title(month_legend[imon],fontsize=17)
                plt.xticks(xax, my_xticks)
                plt.setp(axs[imon].get_xticklabels(), visible=True)

            for ax in axs[9:12]:
                ax.set_xlabel('Local time (hr)',fontsize=17)
            for ax in axs[::3]:
                ax.set_ylabel('Pressure (mb)',fontsize=17)
            axs[0].invert_yaxis()
            plt.suptitle(title,fontsize=30)
            fig1.subplots_adjust(right=0.8)
            cbar_ax = fig1.add_axes([0.85, 0.15, 0.05, 0.7])
            cb = fig1.colorbar(im, cax=cbar_ax)
            #cb.set_ticks(np.arange(ct_lo,ct_up+4.5,5),update_ticks=True)
            cb.ax.tick_params(labelsize=15)
            plt.title('cl (%)',fontsize=15)
            fig1.savefig(output_path+'/figures/'+sites[0]+'/'+title+'_'+sites[0]+'.png')
            plt.close('all')

        ########################## Diurnal Cycle Contours
        #---------------------------------------------- 
        # define site-dependent contour levels and local time offest[XZ]
        if sites[0] == 'sgpc1': ct_lo=0; ct_up=25.5; locoff=6
        if sites[0] == 'nsac1': ct_lo=0; ct_up=30.5; locoff=8
        if sites[0] == 'enac1': ct_lo=0; ct_up=25.5; locoff=1
        if sites[0] == 'twpc1': ct_lo=0; ct_up=70.5; locoff=14
        if sites[0] == 'twpc2': ct_lo=0; ct_up=40.5; locoff=12
        if sites[0] == 'twpc3': ct_lo=0; ct_up=40.5; locoff=15
        if sites[0] == 'maom1': ct_lo=0; ct_up=60.5; locoff=4
        if test_findex == 0: ct_up=np.nanmax(cl_ob_diurnal.flatten())
        if test_findex == 1: ct_up=np.nanmax(np.concatenate((cl_ob_diurnal.flatten(),cl_p_diurnal.flatten()),axis=0))

        rlevel=np.arange(ct_lo,ct_up+1,0.5)
        #---------------------------------------------- 
        #plotting contours
        for iid,index in enumerate(index_list):
            fig2 = plt.figure()# Create figure
            ax  =fig2.add_axes([0.15, 0.15, 0.65, 0.75]) # Create axes
            if index==0:
                 title=variable+'_diurnal_clim_obs'
                 yy=np.linspace(0,23,24)
                 xx=np.linspace(100,1000,37)
                 x,y=np.meshgrid(xx,yy)
                 obs_data_con=np.concatenate((cl_ob_diurnal,cl_ob_diurnal),axis=0)#6 hour GMT to Local time
                 im=ax.contourf(y,x,obs_data_con[locoff:locoff+24,::-1],cmap='jet',levels=rlevel)
                 #im=ax.pcolormesh(y,x,obs_data_con[6:30,::-1], vmin=0, vmax=25)
                 plt.xlim([0,23])
                 xax =  np.arange (0,24,3)
                 my_xticks = ['0','3','6','9','12','15','18','21']

            else:
                 title=variable+'_diurnal_clim_mod'
                 yy=np.linspace(0,tlen_testVar-1,tlen_testVar)
                 xx=np.linspace(100,1000,37)
                 x,y=np.meshgrid(xx,yy)
                 test_data_con=np.concatenate((cl_p_diurnal,cl_p_diurnal),axis=0)
                 #Starting hour GMT to Local time
                 if tlen_testGap == 3: #if the test model is 3-hourly
                     test_pstart = round(locoff/tlen_testGap)-1
                     if test_pstart < 0: test_pstart=int(0)
                     im=ax.contourf(y,x,test_data_con[test_pstart:test_pstart+8,::-1],cmap='jet',levels=rlevel)
                 if tlen_testGap == 1: #if the test model is 1-hourly
                     im=ax.contourf(y,x,test_data_con[locoff:locoff+24,::-1],cmap='jet',levels=rlevel)
                 #im=ax.pcolormesh(y,x,test_data_con[1:9,::-1], vmin=0, vmax=25)
                 plt.xlim([0,tlen_testVar-1])
                 xax =  np.arange (0,tlen_testVar,int(tlen_testVar/8))
                 my_xticks = ['0','3','6','9','12','15','18','21']

            plt.xticks(xax, my_xticks)
            plt.ylabel('Pressure (mb)')
            plt.xlabel('Local time (hr)')
            plt.gca().invert_yaxis()
            plt.suptitle(title)
            cbar_ax = fig2.add_axes([0.85, 0.15, 0.05, 0.75])
            cb = fig2.colorbar(im, cax=cbar_ax)
            #cb.set_ticks(np.arange(ct_lo,ct_up+4.5,5),update_ticks=True)
            plt.title('cl (%)')
            fig2.savefig(output_path+'/figures/'+sites[0]+'/'+title+'_'+sites[0]+'.png')
        #    
            plt.close('all')
    ########################## Annual Cycle Contours

    # define plotting controller [XZ]
    if test_findex == 0: aindex_list = np.arange(1)
    if test_findex == 1: aindex_list = np.arange(3)

    yy=np.linspace(0,11,12)
    xx=np.linspace(100,1000,37)
    x,y=np.meshgrid(xx,yy)
    #---------------------------------------------- 
    # define site-dependent contour levels [XZ]
    if sites[0] == 'sgpc1': ct_lo=0; ct_up=25.5; ct_lo_diff=-10; ct_up_diff=10.5
    if sites[0] == 'nsac1': ct_lo=0; ct_up=60.5; ct_lo_diff=-35; ct_up_diff=40.5
    if sites[0] == 'enac1': ct_lo=0; ct_up=35.5; ct_lo_diff=-15; ct_up_diff=20.5
    if sites[0] == 'twpc1': ct_lo=0; ct_up=70.5; ct_lo_diff=-10; ct_up_diff=40.5
    if sites[0] == 'twpc2': ct_lo=0; ct_up=60.5; ct_lo_diff=-10; ct_up_diff=50.5
    if sites[0] == 'twpc3': ct_lo=0; ct_up=40.5; ct_lo_diff=-20; ct_up_diff=15.5
    if sites[0] == 'maom1': ct_lo=0; ct_up=70.5; ct_lo_diff=-15; ct_up_diff=60.5

    if test_findex == 0:
        ct_up=np.nanmax(cl_ob)
    if test_findex == 1: 
        ct_up=np.nanmax([cl_ob,cl_p])
        tmpct=cl_p[:,::-1]-cl_ob[:,::-1]

        ct_lo_diff=int(np.nanmin(tmpct)-1)
        ct_up_diff=int(np.nanmax(tmpct)+1)

    rlevel=np.arange(ct_lo,ct_up+1,0.5) #original
    drlevel=np.arange(ct_lo_diff,ct_up_diff,0.5)   #difference
    #---------------------------------------------- 


    # start plotting
    for iid,index in enumerate(aindex_list):
        fig = plt.figure()# Create figure
        ax  =fig.add_axes([0.15, 0.15, 0.65, 0.75]) # Create axes
        if index==0: #observation
            im=ax.contourf(y,x,cl_ob[:,::-1],cmap='jet',levels=rlevel)
            title=variable+'_annual_cycle_clim_obs_'+sites[0]
        elif index==1: #test model
            title=variable+'_annual_cycle_clim_mod_'+sites[0]
            im=ax.contourf(y,x,cl_p[:,::-1],cmap='jet',levels=rlevel)
            #im=ax.pcolormesh(y,x,cl_p[:,::-1], vmin=0, vmax=25)
        elif index==2: #difference
            im=ax.contourf(y,x,cl_p[:,::-1]-cl_ob[:,::-1],cmap='coolwarm',levels=drlevel)
            title=variable+'_annual_cycle_clim_the_diff_'+sites[0]
        xax =  np.arange (0,12,1)
        my_xticks = ['J','F','M','A','M','J','J','A','S','O','N','D']
        plt.xticks(xax, my_xticks)
        plt.xlim(0,11)
        plt.ylabel('Pressure (mb)')
        plt.xlabel('Month')
        plt.gca().invert_yaxis()
        plt.suptitle(title)
        cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.75])
        cb = fig.colorbar(im, cax=cbar_ax)
        #if index < 2:  cb.set_ticks(np.arange(ct_lo,ct_up+4.5,5),update_ticks=True)           #original plot colorbar
        #if index == 2: cb.set_ticks(np.arange(ct_lo_diff,ct_up_diff+4.5,5),update_ticks=True) #difference plot colorbar
        plt.title('cl (%)')
        fig.savefig(output_path+'/figures/'+sites[0]+'/'+title+'.png')
    #    
        plt.close('all')
    ########################### Seasonal Mean Vertical Lind Plot
    levels=xx
    seasons=['MAM','JJA','SON','DJF']
    if test_findex == 1: cl_p2=np.concatenate((cl_p,cl_p),axis=0)
    cl_ob2=np.concatenate((cl_ob,cl_ob),axis=0)

    #---------------------------------------------- 
    # define site-dependent contour levels [XZ]
    if test_findex == 0: xtup=np.nanmax(cl_ob2.flatten())
    if test_findex == 1: xtup=np.nanmax(np.concatenate((cl_ob2.flatten(),cl_p2.flatten()),axis=0))

    #---------------------------------------------- 
    # start plotting
    for index in range(len(seasons)):
        fig3 = plt.figure(figsize=(10,15))# Create figure
        ax  =fig3.add_axes([0.15, 0.07, 0.80, 0.88]) # Create axes
        if test_findex == 1: ax.plot(np.nanmean(cl_p2[index*3+2:(index+1)*3+2,::-1],axis=0),levels,'r',lw=3,label='MOD')
        ax.plot(np.nanmean(cl_ob2[index*3+2:(index+1)*3+2,::-1],axis=0),levels,'k',lw=3,label='OBS')
        plt.gca().invert_yaxis()
        plt.ylabel('Pressure (mb)',fontsize=20)
        plt.xlabel('Cloud Fraction (%)',fontsize=20)
        plt.xlim([0,xtup])
        plt.legend(loc='best',prop={'size':25})
        ax.tick_params(labelsize=20,length=5,width=1,direction='out',which='major')
        plt.title(seasons[index]+' Mean Cloud Fraction Vertical Profile',fontsize=20)
        fig3.savefig(output_path+'/figures/'+sites[0]+'/'+variable+'_zdiff_'+seasons[index]+'_'+sites[0]+'.png')
        plt.close('all')

    ########################### ANN Mean Vertical Lind Plot

    fig0 = plt.figure(figsize=(10,15))# Create figure
    ax  =fig0.add_axes([0.15, 0.07, 0.80, 0.88]) # Create axes
    if test_findex == 1: ax.plot(cl_p_ann[::-1],levels,'r',lw=3,label='MOD')
    ax.plot(cl_ob_ann[::-1],levels,'k',lw=3,label='OBS')
    plt.gca().invert_yaxis()
    plt.ylabel('Pressure (mb)',fontsize=20)
    plt.xlabel('Cloud Fraction (%)',fontsize=20)
    plt.xlim([0,xtup])
    plt.legend(loc='best',prop={'size':25})
    ax.tick_params(labelsize=20,length=5,width=1,direction='out',which='major')
    plt.title('Annual Mean Cloud Fraction Vertical Profile',fontsize=20)
    fig0.savefig(output_path+'/figures/'+sites[0]+'/'+variable+'_zdiff_'+'ANN_'+sites[0]+'.png')
    plt.close('all')
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

