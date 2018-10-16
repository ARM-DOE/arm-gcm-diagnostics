import os
import glob
import cdms2
import cdutil
import numpy as np
from numpy import genfromtxt
import csv
import matplotlib.pyplot as plt
from varid_dict import varid_longname


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

    # Calculate for test model
    month = seasons#['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
#    test_var_season=np.empty([len(variables),len(seasons)])*np.nan
    test_file = glob.glob(os.path.join(test_path,'*'+test_model+'*diurnal*'+ sites[0]+'.nc')) #read in monthly test data
    fin = cdms2.open(test_file[0])
    
    
    print 'test_model',test_model

    for j, variable in enumerate(variables): 
        try:
            if variable == 'cl' or variable == 'cl_p':
                var = fin ('cl_p')
            else:
                var = fin(variable)
            var[var>100]=np.nan
            var_2d = np.reshape(var,(12,8,37))
    
            with file(output_path+'/metrics/'+variable+'_test_diurnal_climo_'+ sites[0]+'.csv', 'w') as outfile:
                outfile.write('# Array shape: {0}'.format(var_2d.shape)+' as (month, hours, vertical levels)\n')
                mon_id=0
                for data_slice in var_2d:
                    #outfile.write('# New slice\n')
                    outfile.write('#'+month[mon_id]+' slice\n')
                    np.savetxt(outfile, data_slice, fmt='%-7.2f')
                    mon_id=mon_id+1
        except:
            print (variable+" not processed for " + test_model)

    fin.close()
    

    # Calculate for observational data
    if sites[0] == 'sgp':
    #    obs_var_season=np.empty([len(variables),len(seasons)])*np.nan
        obs_file = glob.glob(os.path.join(obs_path,'*ARMdiag_c1_diurnal_climo_'+ sites[0]+'*.nc')) #read in monthly test data
        #obs_file = glob.glob(os.path.join(obs_path,'*ARMdiag_c1_ARSCL_ACRED_diurnal_climo*.nc')) #read in monthly test data
        print 'ARM data'
        print obs_file
        fin = cdms2.open(obs_file[0])
        for j, variable in enumerate(variables): 
            try:
                var = fin (variable)
                var[var>100]=np.nan
                if sites[0] == 'sgp':
                    var_2d = np.reshape(var,(12,24,37))
                print var_2d.shape
        
                with file(output_path+'/metrics/'+variable+'_obs_diurnal_climo_'+ sites[0]+'.csv', 'w') as outfile:
                    outfile.write('# Array shape: {0}'.format(var_2d.shape)+' as (month, hours, vertical levels)\n')
                    mon_id=0
                    for data_slice in var_2d:
                        #outfile.write('# New slice\n')
                        outfile.write('#'+month[mon_id]+' slice\n')
                        np.savetxt(outfile, data_slice, fmt='%-7.2f')
                        mon_id=mon_id+1
        
        
            except:
                print (variable+" not processed for obs")
        fin.close()
    else:
        obs_file = glob.glob(os.path.join(obs_path,'*ARMdiag_domain_monthly_climo_'+ sites[0]+'*.nc')) #read in monthly test data
        #obs_file = glob.glob(os.path.join(obs_path,'*ARMdiag_c1_ARSCL_ACRED_diurnal_climo*.nc')) #read in monthly test data
        print 'ARM data'
        print sites[0]
        fin = cdms2.open(obs_file[0])
        for j, variable in enumerate(variables):
            try:
                var = fin (variable)
                var[var>100]=np.nan
                #if sites[0] == 'sgp':
                #    var_2d = np.reshape(var,(12,24,37))
                print var.shape
                np.savetxt(output_path+'/metrics/'+variable+'_obs_annual_cycle_'+sites[0]+'.csv',var)
    
            except:
                print (variable+" not processed for obs")
        fin.close()
         


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
        if sites[0]=='sgp':
            obs_data = np.loadtxt(output_path+'/metrics/'+variable+'_obs_diurnal_climo_'+ sites[0]+'.csv')
            obs_data = obs_data.reshape((12,24,37))
#            cmip_data = genfromtxt(output_path+'/metrics/'+variable+'_cmip_annual_cycle.csv')

            cl_ob=np.nanmean(obs_data,axis=1)
            cl_ob_diurnal=np.nanmean(obs_data,axis=0)
            cl_ob_ann=np.nanmean(cl_ob,axis=0)
        else:
            obs_data = np.loadtxt(output_path+'/metrics/'+variable+'_obs_annual_cycle_'+ sites[0]+'.csv')
            cl_ob = obs_data
            cl_ob_ann=np.nanmean(cl_ob,axis=0)
            print cl_ob_ann.shape
        ####################Monthly Mean Diurnal Cycle

        if sites[0] == 'sgp':
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
                         #im=axs[imon].pcolormesh(y,x,obs_data_con[6:30,::-1], vmin=0, vmax=25)
                         im=axs[imon].pcolormesh(y,x,obs_data_con[:24,::-1], vmin=0, vmax=25)
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
                fig1.savefig(output_path+'/figures/'+title+'.png')
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
                fig2.savefig(output_path+'/figures/'+title+'.png')
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

#def annual_cycle_zt_html(parameter):
#    """ Create set 3 diag. html hosting contour and vertical profiles of annual cycle"""
#
#    output_path = parameter.output_path
#    test_model = parameter.test_data_set
#    variables = parameter.variables
#
#    var_longname = [ varid_longname[x] for x in variables]
#
##    vas=['cl_p','T','Q']
##    vas_source=['ARSCL','Sounding','Sounding']
##    vas_long=['Cloud Fraction (%)','Temperature(C)','Specific Humidity (kg/kg)']
#    seasons=['ANN','DJF','MAM','JJA','SON']
#    #for va_ind in range(len(vas)-2):# at this stage for cl_p only
#    for j, variable in enumerate(variables):
#        htmlfile = open(output_path+'/html/AC_amip_contour.html',"w")
#        htmlfile.write('<p><th><b>'+test_model+': Annual Cycle'+ '</b></th></p>')
#        htmlfile.write('<table>')
#        htmlfile.write('<TR><TH ALIGN=LEFT><BR><TH ALIGN=LEFT><font color=blue size=+1>Southern Great Plains (SGP)</font><TH><BR><TR>')
#        #htmlfile.write('<TH><BR>')
#        htmlfile.write('<TR><TH><BR><TH ALIGN=LEFT><font color=red >Contour plots</font><BR><TH ALIGN=LEFT><font color=red > Vertical profiles</font>')
#
#        htmlfile.write('<TR><TH ALIGN=LEFT>'+var_longname[j])#+'('+vas_source[va_ind]+')')
#        fig_obs=output_path+'/figures/obs_'+variable+'_annual_cycle_clim.png'
#        fig_mod=output_path+'/figures/mod_'+variable+'_annual_cycle_clim.png'
#        fig_diff=output_path+'/figures/diff_'+variable+'_annual_cycle_clim.png'
#        htmlfile.write('<TH ALIGN=LEFT><A HREF='+fig_mod+'> Model</a>')
#        htmlfile.write('<A HREF='+fig_obs+'> Obs.</a>')
#        htmlfile.write('<A HREF='+fig_diff+'> Model-Obs.</a>')
#        #htmlfile.write('<TH><BR>')
#
#        for si in range(len(seasons)):
#           fig=output_path+'/figures/'+seasons[si]+'_'+vas[va_ind]+'_diff.png'
#           if seasons[si]=='ANN':
#               htmlfile.write('<TH ALIGN=LEFT><A HREF='+fig+'> '+seasons[si]+'</a>')
#           else:
#
#               htmlfile.write('<A HREF='+fig+'> '+seasons[si]+'</a>')
#
#
#
#def diurnal_cycle_zt_html(parameter):
#    """Create set 5 diag. html hosting contour plots of diurnal cycle"""
#    output_path = parameter.output_path
#    test_model = parameter.test_data_set
#    variables = parameter.variables
#
#    var_longname = [ varid_longname[x] for x in variables]
#
#    htmlfile = open(output_path+'/html/DC_amip_contour.html',"w")
#    htmlfile.write('<p><th><b>'+test_model+': Diurnal Cycle'+ '</b></th></p>')
#    htmlfile.write('<table>')
#    htmlfile.write('<TR><TH ALIGN=LEFT><BR><TH ALIGN=LEFT><font color=blue size=+1>Southern Great Plains (SGP)</font><TH><BR><TR>')
#    htmlfile.write('<TR><TH><BR><TH ALIGN=LEFT><font color=red >Monthly Mean</font><BR><TH ALIGN=LEFT><font color=red > Annual Mean</font>')
#
#    for j, variable in enumerate(variables):
#    #for va_ind in range(len(vas)-2):# at this stage for cl_p only
#        htmlfile.write('<TR><TH ALIGN=LEFT>'+var_longname[j])#+'('+vas_source[va_ind]+')')
#        fig_obs=output_path+'/figures/obs_'+variable+'_diurnal_clim.png'
#        fig_mod=output_path+'/figures/mod_'+variable+'_diurnal_clim.png'
#        fig_obs_mon=output_path+'/figures/obs_'+variable+'_mon_diurnal_clim.png'
#        fig_mod_mon=output_path+'/figures/mod_'+variable+'_mon_diurnal_clim.png'
#        htmlfile.write('<TH ALIGN=LEFT><A HREF='+fig_mod_mon+'> Model</a>')
#        htmlfile.write('<A HREF='+fig_obs_mon+'> Obs.</a>')
#        htmlfile.write('<TH ALIGN=LEFT><A HREF='+fig_mod+'> Model</a>')
#        htmlfile.write('<A HREF='+fig_obs+'> Obs.</a>'


#    
#
#def annual_cycle_line_pl t(parameter):
#    """Calculate annual cycle climatology"""
#    variables = parameter.variables
#    seasons = parameter.season
#    output_path = parameter.output_path
#
#    var_longname = [ varid_longname[x] for x in variables]
#    for j, variable in enumerate(variables):
#        mod_num = cmip_data.shape[0]
#
#        fig = plt.figure()# Create figure
#        ax  =fig.add_axes([0.15, 0.14, 0.8, 0.8]) # Create axes
#        xax =  np.arange (1,13,1)
#
#        for mod_ind in range(mod_num):
#            ax.plot(xax,cmip_data[mod_ind,:],'grey',lw=1)
#        ann_mean=np.mean(test_data[:])
#        ax.plot(xax,test_data[:],'r',label='MOD: %.2f'%ann_mean,lw=3)
#        ann_mean=np.mean(obs_data[:])
#        ax.plot(xax,obs_data[:],'k',label='OBS: %.2f'%ann_mean,lw=3)
#        ann_mean=np.mean(mmm_data[:])
#        ax.plot(xax,mmm_data[:],'b',label='MMM: %.2f'%ann_mean,lw=3)
#        #my_xticks = ['J','F','M','A','M','J','J','A','S','O','N','D']
#        my_xticks = seasons
#        plt.xticks(xax, my_xticks)
#        plt.xlim(1,12)
##        plt.ylim(ylim[va_ind])
#        plt.title('Annual Cycle: Model vs OBS vs CMIP' )
#        plt.xlabel('Month')
#        plt.legend(loc='best',prop={'size':15})
#        plt.ylabel(var_longname[j])
#        fig.savefig(output_path+'/figures/'+variable+'_annual_cycle.png')
#        plt.close('all')
#       
#
#    
#def annual_cycle_taylor_diagram(parameter):
#    """Calculate annual cycle climatology"""
#    variables = parameter.variables
#    seasons = parameter.season
#    output_path = parameter.output_path
#
#    var_longname = [ varid_longname[x] for x in variables]
#    for j, variable in enumerate(variables):
#        obs_data = genfromtxt(output_path+'/metrics/'+variable+'_obs_annual_cycle_std_corr.csv')
#        test_data = genfromtxt(output_path+'/metrics/'+variable+'_test_annual_cycle_std_corr.csv')
#        mmm_data = genfromtxt(output_path+'/metrics/'+variable+'_mmm_annual_cycle_std_corr.csv')
#        cmip_data = genfromtxt(output_path+'/metrics/'+variable+'_cmip_annual_cycle_std_corr.csv')
#        mod_num = cmip_data.shape[0]
#        
#
#        fig = plt.figure(figsize=(8,8))
#        refstd = obs_data[0]
#        dia = TaylorDiagram(refstd, fig=fig,rect=111, label="Reference")
#
#        # Add samples to Taylor diagram
#        for i,(stddev,corrcoef) in enumerate(cmip_data):
#            dia.add_sample(stddev, corrcoef, marker='.',ms=10, c='grey')
#
#        dia.add_sample(test_data[0], test_data[1],marker='.',ms=15, c='red',label='MOD')
#        dia.add_sample(mmm_data[0], mmm_data[1],marker='.',ms=15, c='b',label='MMM')
#
#        # Add RMS contours, and label them
#        contours = dia.add_contours(colors='0.5')
#        plt.clabel(contours, inline=1, fontsize=10)
#        plt.title(var_longname[j])
#
#        # Add a figure legend
#        fig.legend([dia.samplePoints[0],dia.samplePoints[-2],dia.samplePoints[-1]] ,
#                   [ p.get_label() for p in [dia.samplePoints[0],dia.samplePoints[-2],dia.samplePoints[-1]] ],
#                   numpoints=1,  loc='upper right',prop={'size':10})
##        np.savetxt(output_path+'metrics/'+vas[va_ind]+'_'+mod+'std_corr.csv',mod_sample,fmt='%.3f')
#        fig.savefig(output_path+'/figures/'+variable+'_annual_cycle_taylor_diagram.png')
#        plt.close('all')


    
    
    
    
