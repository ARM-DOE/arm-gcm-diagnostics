import os
import glob
import cdms2
import cdutil
import numpy as np
from numpy import genfromtxt
import csv
import matplotlib.pyplot as plt
from matplotlib.pyplot import grid
from varid_dict import varid_longname
import cdtime

def var_pdf_daily(var, season, years):
    "Calculate diurnal cycle climatology of each variable"
    if season == 'JJA':
        mo0 = 6
    if season == 'SON': 
        mo0 = 9
    if season == 'DJF': 
        mo0 = 12
    if season == 'MAM': 
        mo0 = 3
    var_da_year = np.empty([len(years),90])*np.nan
    for iy,year in enumerate(years):
        t1 = cdtime.comptime(year,mo0,01)
        t2 = t1.add(90,cdtime.Days)
#        try:
        var_yr =  var(time=(t1,t2,'co'))
        var_da_year[iy,:]= var_yr
        if var.id == 'tas':
            var_da_year[iy,:] = var_da_year[iy,:]-273.15

        if var.id == 'pr':
            var_da_year[iy,:] = var_da_year[iy,:]*3600.*24.
#        except:
#            print str(year) +' not Available!'
#            var_da_year[iy,:] =  np.nan
    var_da = np.reshape(var_da_year, (90*len(years)))
    return var_da


def pdf_daily_data(parameter):
    """Calculate diurnal cycle climatology"""
    variables = parameter.variables
    test_path = parameter.test_data_path
    obs_path = parameter.obs_path
    cmip_path = parameter.cmip_path
    output_path = parameter.output_path
    seasons = parameter.season
   
    test_model = parameter.test_data_set 
    ref_models = parameter.ref_models

    # Calculate for test model
    years = range(1979,2006)        #a total of 27 years 
    
    test_var_season=np.empty([len(variables),len(years)*90])*np.nan
    test_file = glob.glob(os.path.join(test_path,'*'+test_model+'*_da_*.nc')) #read in test data
    if len(test_file) == 0:
       raise RuntimeError('No daily data for test model were found.')
    fin = cdms2.open(test_file[0])
    
    print('test_model',test_model)

    for j, variable in enumerate(variables): 
        for season in seasons:
            try:
                var = fin (variable,squeeze = 1)
                test_var_da = var_pdf_daily(var,season,years)

            except:
                print(variable+" not processed for " + test_model)
            test_var_season[j,:] = test_var_da

    # Calculate for observational data
    years_obs = range(1999,2012)
    obs_var_season=np.empty([len(variables),len(years_obs)*90])*np.nan
    obs_file = glob.glob(os.path.join(obs_path,'*ARMdiag*daily*.nc')) #read in diurnal test data
    print('ARM data')
    fin = cdms2.open(obs_file[0])
    for j, variable in enumerate(variables): 
              
        try:
            var = fin (variable)
            for season in seasons:
                try:
                    var = fin (variable,squeeze = 1)
                    obs_var_da = var_pdf_daily(var,season,years_obs)
    
                except:
                    print(variable+" not processed for obs")
        except:
            print(variable+" not processed for obs")
        obs_var_season[j,:] = obs_var_da

    # Calculate cmip model seasonal mean climatology
    cmip_var_season=np.empty([len(ref_models),len(variables),len(years)*90])*np.nan
 
    for i, ref_model in enumerate(ref_models):
         ref_file = glob.glob(os.path.join(cmip_path,'*'+ref_model+'*_da_*.nc')) #read in monthly cmip data
         print('ref_model', ref_model)
         if not ref_file :
             print(ref_model+" not found!") 
         else:
             fin = cdms2.open(ref_file[0])
         
             for j, variable in enumerate(variables): 
                 for season in seasons:
                     try:
                         var = fin (variable,squeeze = 1)
                         cmip_var_season[i, j, :] = var_pdf_daily(var, season,years)

                     except:
                         print(variable+" not processed for " + ref_model)
             fin.close()  
    # Calculate multi-model mean
    mmm_var_season =  np.nanmean(cmip_var_season,axis=0)

    # Save data in csv format in metrics folder
    for j, variable in enumerate(variables):
        for i, season in enumerate(seasons):
            np.savetxt(output_path+'/metrics/'+variable+'_'+season+'_test_pdf_daily.csv',test_var_season[j,:])
            np.savetxt(output_path+'/metrics/'+variable+'_'+season+'_mmm_pdf_daily.csv',mmm_var_season[j,:])
            np.savetxt(output_path+'/metrics/'+variable+'_'+season+'_cmip_pdf_daily.csv',cmip_var_season[:,j,:])
            np.savetxt(output_path+'/metrics/'+variable+'_'+season+'_obs_pdf_daily.csv',obs_var_season[j,:])

def accum(list):
    """Sequential accumulation of the original list"""
    result = []
    for i in range(len(list)):
        result.append(sum(list[:i+1]))
    return result
    
def calculate_pdf(var):
    bins_width=[0.0025*1.2**(x) for x in range(55)]
    bins=accum(bins_width)
    bins=[x for x in bins]
    precip_cutoff=0.03-0.0025/2 
    ind = np.where(var>precip_cutoff)
    var_da=var[ind]
    y,binEdges=np.histogram(var_da,bins=bins,density=True)
    cumulative = np.cumsum(y*(binEdges[1:]-binEdges[:-1]))
    wday_ob=100.0*np.size(var_da)/np.size(var)
    return y, binEdges  

def pdf_daily_plot(parameter):
    """plotting pdf using daily mean"""
    variables = parameter.variables
    seasons = parameter.season
    output_path = parameter.output_path
    ref_models = parameter.ref_models

    var_longname = [ varid_longname[x] for x in variables]
    mod_num = len(ref_models)
    
    for j, variable in enumerate(variables):
        for i, season in enumerate(seasons):
            test_data = genfromtxt(output_path+'/metrics/'+variable+'_'+season+'_test_pdf_daily.csv')
            mmm_data =  genfromtxt(output_path+'/metrics/'+variable+'_'+season+'_mmm_pdf_daily.csv')
            obs_data =  genfromtxt(output_path+'/metrics/'+variable+'_'+season+'_obs_pdf_daily.csv')
            cmip_data = genfromtxt(output_path+'/metrics/'+variable+'_'+season+'_cmip_pdf_daily.csv')
            mod_num = cmip_data.shape[0]

            
    
            ######################Use same method to calculate PDFs for obs, model and cmip multi-models.
            fig = plt.figure()# Create figure
            ax  =fig.add_axes([0.15, 0.15, 0.8, 0.8]) # Create axes
            xax =  np.arange (1,13,1)
    
            fig1 = plt.figure()# Create figure
            ax1  =fig1.add_axes([0.15, 0.15, 0.8, 0.8]) # Create axes
            y,binEdges = calculate_pdf(test_data)
    
            ax.plot(0.5*(binEdges[1:]+binEdges[:-1]),y,'r',lw=3)
            y1=y*0.5*(binEdges[1:]+binEdges[:-1])
            ax1.plot(0.5*(binEdges[1:]+binEdges[:-1]),y1,'r',lw=3)

            y,binEdges = calculate_pdf(obs_data)

            ax.plot(0.5*(binEdges[1:]+binEdges[:-1]),y,'b',lw=3)
            y1=y*0.5*(binEdges[1:]+binEdges[:-1])
            ax1.plot(0.5*(binEdges[1:]+binEdges[:-1]),y1,'b',lw=3)
            for imod in range(mod_num):
                y,binEdges = calculate_pdf(cmip_data[imod,:])
    
                ax.plot(0.5*(binEdges[1:]+binEdges[:-1]),y,'grey',lw=1)
                y1=y*0.5*(binEdges[1:]+binEdges[:-1])
                ax1.plot(0.5*(binEdges[1:]+binEdges[:-1]),y1,'grey',lw=1)
                cumulative1 = np.cumsum(y1*(binEdges[1:]-binEdges[:-1]))

            ax.text(0.85, 0.9,'OBS',color='r',verticalalignment='top', horizontalalignment='right',transform=ax.transAxes)
            ax.text(0.85, 0.8,'MOD',color='b',verticalalignment='top', horizontalalignment='right',transform=ax.transAxes)
            ax1.text(1.2, 1,'OBS',color='r',verticalalignment='top', horizontalalignment='right',transform=ax.transAxes)
            ax1.text(1.2, 0.9,'MOD',color='b',verticalalignment='top', horizontalalignment='right',transform=ax.transAxes)

            ax.set_xscale('log')
            ax.set_yscale('log')
            ax.set_xlim([0.05,200])
            ax.set_ylim([0.0001,20])
            ax.set_ylabel('Frequency')
            ax.set_xlabel('Precipitation rate (mm/day)')
            ax1.set_xlim([0.05,200])
            ax1.set_ylim([0.01,1])
            ax1.set_xscale('log')
            ax1.set_yscale('log')
            ax1.set_ylabel('Precipitation Amount (mm/day)')
            ax1.set_xlabel('Precipitation rate (mm/day)')
            fig.savefig(output_path+'/figures/'+variable+'_'+season+'_pdf1_daily.png')
            fig1.savefig(output_path+'/figures/'+variable+'_'+season+'_pdf2_daily.png')





#    
#            fig = plt.figure()# Create figure
#            ax  =fig.add_axes([0.15, 0.14, 0.8, 0.8]) # Create axes
#            xax_3hr=np.array([3.0*x-6.5 for x in range(8)])
#            xax_1hr=np.array([1.0*x-6.5 for x in range(24)]) 
#            #xax =  np.arange (1,13,1)
#    
#            # plotting ref models 
#            mod_phase=np.empty([mod_num])
#            mod_amp=np.empty([mod_num])
#            for mod_ind in range(mod_num):
#                popt, pcov = curve_fit(func24, xax_3hr, cmip_data[mod_ind,:] ,p0=(1.0,0.2))
#                p1_mod = popt[0]
#                p2_mod = popt[1]
#                ymod_fit=func24(xax_1hr,p1_mod,p2_mod)+np.mean(cmip_data[mod_ind,:])
#                
#                mod_fit,=ax.plot(np.concatenate((xax_1hr,[x+24 for x in xax_1hr])),np.concatenate((ymod_fit,ymod_fit)), 'grey',lw=1)
#                mod_amp[mod_ind]=p1_mod
#                if p1_mod<=0 :
#                   p2_mod=1.5*np.pi-p2_mod
#                if p1_mod>0 :
#                   p2_mod=0.5*np.pi-p2_mod
#                mod_phase[mod_ind]=p2_mod
#                #ax.plot(xax_3hr,cmip_data[mod_ind,:],'grey',lw=1)
#    
#            # plotting test model
#            ann_mean=np.mean(test_data[:])
#            popt, pcov = curve_fit(func24, xax_3hr, test_data ,p0=(1.0,0.2))
#            p1_mod = popt[0]
#            p2_mod = popt[1]
#            ymod_fit=func24(xax_1hr,p1_mod,p2_mod)+np.mean(test_data)
#            mod_fit,=ax.plot(np.concatenate((xax_1hr,[x+24 for x in xax_1hr])),np.concatenate((ymod_fit,ymod_fit)), 'r',label = 'MOD: %.2f'%ann_mean,lw=2)
#            ax.plot(np.concatenate((xax_3hr,[x+24 for x in xax_3hr])),np.concatenate((test_data,test_data)),'.r',label='MOD',lw=2,markersize=15)
#            test_amp=p1_mod
#            if p1_mod<=0 :
#               p2_mod=1.5*np.pi-p2_mod
#            if p1_mod>0 :
#               p2_mod=0.5*np.pi-p2_mod
#            test_phase=p2_mod
#            #ax.plot(xax_3hr,test_data[:],'r',label='MOD: %.2f'%ann_mean,lw=3)
#    
#            # plotting test model
#            ann_mean=np.mean(obs_data[:])
#            popt, pcov = curve_fit(func24, xax_1hr, obs_data ,p0=(1.0,0.2))
#            p1_obs = popt[0]
#            p2_obs = popt[1]
#            yobs2=func24(xax_1hr,p1_obs,p2_obs)+np.mean(obs_data)
#            obs2,=plt.plot(np.concatenate((xax_1hr,[x+24 for x in xax_1hr])),np.concatenate((obs_data,obs_data)),'k.',label='OBS: %.2f'%ann_mean,lw=2,markersize=15)
#            obs_fit2,=plt.plot(np.concatenate((xax_1hr,[x+24 for x in xax_1hr])), np.concatenate((yobs2,yobs2)),'k',lw=2)
#            obs2_amp=abs(p1_obs)
#            obs2_phase=0.5*np.pi-p2_obs  #-5.0/24*2*np.pi
#    
#            #ax.plot(xax_1hr,obs_data[:],'k',label='OBS: %.2f'%ann_mean,lw=3)
#            #ann_mean=np.mean(mmm_data[:])
#            #ax.plot(xax_3hr,mmm_data[:],'b',label='MMM: %.2f'%ann_mean,lw=3)
#            my_xticks=['0h', '3h', '6h', '9h', '12h', '15h', '18h', '21h']
#            my_xticks_loc=np.array([3*x for x in range(8)])
#            plt.xticks(my_xticks_loc, my_xticks)
#            ax.set_xlim([0,24])
#            ax.set_ylim([-0.5,7])
#            ax.text(0.3, 0.95,'OBS',color='k',verticalalignment='top', horizontalalignment='left',transform=ax.transAxes)
#            ax.text(0.3, 0.85,'MOD',color='r',verticalalignment='top', horizontalalignment='left',transform=ax.transAxes)
#            plt.xlabel('local solar time [hr]')
#            plt.ylabel(var_longname[j])
#            fig.savefig(output_path+'/figures/'+variable+'_'+season+'_pdf_daily.png')
#            plt.close('all')
#           
#    
#    
#            ##########Generate hormonic dial plot: mapping phase and amplitude to Dial
#    
#            fig2 = plt.figure()
#            ax2  =fig2.add_axes([0.1, 0.1, 0.8, 0.8],polar=True)#, axisbg='#d5de9c')
#    
#            size=50
#            ax2.scatter(obs2_phase,obs2_amp,color='k',label='OBS',s=size*2)
#            ax2.scatter(mod_phase[:],abs(mod_amp[:]),color='grey',s=size)
#            ax2.scatter(test_phase,abs(test_amp),color='r',label='MOD',s=size*2)
#            ax2.legend(scatterpoints=1,loc='center right',bbox_to_anchor=(1.2,0.90),prop={'size':15})
#            ax2.set_rmax(3)
#            ax2.set_theta_direction(-1)
#            ax2.set_theta_offset(np.pi/2)
#            ax2.set_xticklabels(['0h', '3h', '6h', '9h', '12h', '15h', '18h', '21h'])
#            grid(True)
#    
#            fig2.savefig(output_path+'/figures/'+variable+'_'+season+'_pdf_daily_harmonic_diagram.png')
#
#
#    
#def pdf_daily_taylor_diagram(parameter):
#    """Calculate diurnal cycle climatology"""
#    variables = parameter.variables
#    seasons = parameter.season
#    output_path = parameter.output_path
#
#    var_longname = [ varid_longname[x] for x in variables]
#    for j, variable in enumerate(variables):
#        obs_data = genfromtxt(output_path+'/metrics/'+variable+'_obs_pdf_daily_std_corr.csv')
#        test_data = genfromtxt(output_path+'/metrics/'+variable+'_test_pdf_daily_std_corr.csv')
#        mmm_data = genfromtxt(output_path+'/metrics/'+variable+'_mmm_pdf_daily_std_corr.csv')
#        cmip_data = genfromtxt(output_path+'/metrics/'+variable+'_cmip_pdf_daily_std_corr.csv')
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
##        np.savetxt(basedir+'metrics/'+vas[va_ind]+'_'+mod+'std_corr.csv',mod_sample,fmt='%.3f')
#        fig.savefig(output_path+'/figures/'+variable+'_pdf_daily_taylor_diagram.png')
#        plt.close('all')
#
#
#    
#    
#    
#    
