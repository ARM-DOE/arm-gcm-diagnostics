#===========================================================================================================================
# Program for generate the two-legged metrics: Terrestrial and Atmospheric Coupling Legs
#---------------------------------------------------------------------------------------------------------------------------
# V4 Development
    # ----------------------------------------------------------------------------------------------------
    # Cheng Tao - Jul2024 @ LLNL
    # ### Scatter plot of soil moisture vs. SH/LH/EF
    # ### Scatter plot of SH/LH/EF vs. LCL
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
import MV2
import matplotlib.gridspec as gridspec
import scipy.stats
from scipy import interpolate
import calendar

def get_seasonal_data_3hr(var,seasons,years):

    '''Get seasonal data for each variable'''
    nyears = len(years)
    nseasons = len(seasons)
    nsteps = int(nyears*90)
    t0 = 0

    var_seasons = MV2.zeros([nyears,nseasons,90])*np.nan #Daily mean for each season
    var_seasons_f = MV2.zeros([nsteps,nseasons])*np.nan
    for iyear in range(nyears):
        if calendar.isleap(int(years[iyear]))==True:
            nday = 366
        else:
            nday = 365
        ntime = int(nday*8)
        var1 = var[t0:t0+ntime]
        var1_ext = np.concatenate((var1,var1),axis=0)
        t0 = t0+ntime

        for iseason in range(nseasons):
            if seasons[iseason]=='MAM':
                if nday==366: t1 = 60
                else: t1 = 59
            if seasons[iseason]=='JJA':
                if nday==366: t1 = 152
                else: t1 = 151
            if seasons[iseason]=='SON':
                if nday==366: t1 = 244
                else: t1 = 243
            if seasons[iseason]=='DJF':
                if nday==366: t1 = 335
                else: t1 = 334
            var_seasons0 = var1_ext[int(t1*8):int(t1*8)+720]
            var_seasons1 = np.reshape(var_seasons0,(90,8))
            var_seasons2 = MV2.average(var_seasons1,axis=1) #daily mean for 90 days
            #print(var_seasons2.shape)
            var_seasons[iyear,iseason,:] = var_seasons2
            var_seasons_f[iyear*90:iyear*90+90,iseason] = var_seasons2

    return var_seasons_f

def get_seasonal_data(var,seasons,years):
    
    '''Get seasonal data for each variable'''
    nyears = len(years)
    nseasons = len(seasons)
    nsteps = int(nyears*90)
    t0 = 0
    
    var_seasons = MV2.zeros([nyears,nseasons,90])*np.nan #Daily mean for each season
    var_seasons_f = MV2.zeros([nsteps,nseasons])*np.nan
    for iyear in range(nyears):
        if calendar.isleap(int(years[iyear]))==True:
            nday = 366
        else:
            nday = 365
        ntime = int(nday*24)
        var1 = var[t0:t0+ntime]
        var1_ext = np.concatenate((var1,var1),axis=0)
        t0 = t0+ntime

        for iseason in range(nseasons):
            if seasons[iseason]=='MAM':
                if nday==366: t1 = 60
                else: t1 = 59
            if seasons[iseason]=='JJA':
                if nday==366: t1 = 152
                else: t1 = 151
            if seasons[iseason]=='SON':
                if nday==366: t1 = 244 
                else: t1 = 243
            if seasons[iseason]=='DJF':
                if nday==366: t1 = 335
                else: t1 = 334
            var_seasons0 = var1_ext[int(t1*24):int(t1*24)+2160]   
            var_seasons1 = np.reshape(var_seasons0,(90,24)) 
            var_seasons2 = MV2.average(var_seasons1,axis=1) #daily mean for 90 days
            #print(var_seasons2.shape)
            var_seasons[iyear,iseason,:] = var_seasons2
            var_seasons_f[iyear*90:iyear*90+90,iseason] = var_seasons2

    return var_seasons_f
            
def twolegged_metric_plot(parameter):
    variables = parameter.variables
    test_path = parameter.test_data_path
    test_model = parameter.test_data_set
    obs_path = parameter.obs_path
    cmip_path = parameter.cmip_path
    output_path = parameter.output_path
    sites = parameter.sites
    seasons = parameter.season
    nseasons = len(seasons)

    if not os.path.exists(os.path.join(output_path,'figures',sites[0])):
        os.makedirs(os.path.join(output_path,'figures',sites[0]))
    #==========================================================================
    # Calculate for observational data
    #==========================================================================
    print('ARM data',sites[0])
    obs_file = glob.glob(os.path.join(obs_path,sites[0][:3]+'armdiagsLAcoupling' + sites[0][3:5].upper()+'*c1.nc')) #read in data
    print('Processing obs_file',obs_file)
    fin = cdms2.open(obs_file[0])
    sh0 = fin('SH')
    lh0 = fin('LH')
    LCL0 = fin('LCL')
    sm_ebbr0 = fin('soil_moisture_ebbr')
    sm_swats0 = fin('soil_moisture_swats')
    fin.close()

    #==========================================================================
    # Calculate for model data
    #==========================================================================
    test_file = glob.glob(os.path.join(test_path,sites[0][:3]+'testmodel3hrLAcoupling' + sites[0][3:5].upper()+'*c1.nc')) #read in data
    print('Processing test_file',test_file)
    fin = cdms2.open(test_file[0])
    sh1 = fin('SH')
    lh1 = fin('LH')
    LCL1 = fin('LCL')
    print('sh1: ',np.min(sh1),np.max(sh1))
    print('lh1: ',np.min(lh1),np.max(lh1))
    print('LCL1: ',np.min(LCL1),np.max(LCL1))
    fin.close()

    #=================
    # Seasons: obs
    #=================
    years_obs = list(range(2004,2016))
    nday_obs = 90*len(years_obs)
    sh = get_seasonal_data(sh0,seasons,years_obs)
    lh = get_seasonal_data(lh0,seasons,years_obs)
    LCL = get_seasonal_data(LCL0,seasons,years_obs)
    sm_ebbr = get_seasonal_data(sm_ebbr0,seasons,years_obs)
    sm_swats = get_seasonal_data(sm_swats0,seasons,years_obs)
    
    EF = MV2.zeros([nday_obs,nseasons])*np.nan
    for im in range(nday_obs):
        for iseason in range(nseasons):
            EF[im,iseason] = lh[im,iseason]/(lh[im,iseason]+sh[im,iseason])

    #==================
    # Seasons: models
    #==================
    years_mod = list(range(2003,2015))
    nday_mod = 90*len(years_mod)
    sh_mod = get_seasonal_data_3hr(sh1,seasons,years_mod)
    lh_mod  = get_seasonal_data_3hr(lh1,seasons,years_mod)
    LCL_mod  = get_seasonal_data_3hr(LCL1,seasons,years_mod)

    EF_mod = MV2.zeros([nday_mod,nseasons])*np.nan
    for im in range(nday_mod):
        for iseason in range(nseasons):
            EF_mod[im,iseason] = lh_mod[im,iseason]/(lh_mod[im,iseason]+sh_mod[im,iseason])

    #==========================================================================
    # Calculate daily_mean values (10-day means)
    #==========================================================================
    nt_10day = int(nday_obs/10)
     
    sh_10day = MV2.zeros([nt_10day,nseasons])*np.nan
    lh_10day = MV2.zeros([nt_10day,nseasons])*np.nan
    LCL_10day = MV2.zeros([nt_10day,nseasons])*np.nan
    EF_10day = MV2.zeros([nt_10day,nseasons])*np.nan
    sm_ebbr_10day = MV2.zeros([nt_10day,nseasons])*np.nan
    sm_swats_10day = MV2.zeros([nt_10day,nseasons])*np.nan
    for im in range(nt_10day):
        for iseason in range(nseasons):
            tmp1 = sh[:,iseason]
            tmp2 = np.mean(tmp1[10*im:10*im+10])
            sh_10day[im,iseason] = tmp2
         
            tmp1 = lh[:,iseason]
            tmp2 = np.mean(tmp1[10*im:10*im+10])
            lh_10day[im,iseason] = tmp2
     
            tmp1 = LCL[:,iseason]
            tmp2 = np.mean(tmp1[10*im:10*im+10])
            LCL_10day[im,iseason] = tmp2
   
            tmp1 = sm_ebbr[:,iseason]
            tmp2 = np.mean(tmp1[10*im:10*im+10])
            sm_ebbr_10day[im,iseason] = tmp2

            tmp1 = sm_swats[:,iseason]
            tmp2 = np.mean(tmp1[10*im:10*im+10])
            sm_swats_10day[im,iseason] = tmp2

            EF_10day[im,iseason] = lh_10day[im,iseason]/(lh_10day[im,iseason]+sh_10day[im,iseason])

    #==========================================================================
    # Calculate daily_mean values (10-day means) for models
    #==========================================================================
    nt_10day_mod = int(nday_mod/10)

    sh_10day_mod = MV2.zeros([nt_10day_mod,nseasons])*np.nan
    lh_10day_mod = MV2.zeros([nt_10day_mod,nseasons])*np.nan
    LCL_10day_mod = MV2.zeros([nt_10day_mod,nseasons])*np.nan
    EF_10day_mod = MV2.zeros([nt_10day_mod,nseasons])*np.nan
    for im in range(nt_10day_mod):
        for iseason in range(nseasons):
            tmp1 = sh_mod[:,iseason]
            tmp2 = np.mean(tmp1[10*im:10*im+10])
            sh_10day_mod[im,iseason] = tmp2

            tmp1 = lh_mod[:,iseason]
            tmp2 = np.mean(tmp1[10*im:10*im+10])
            lh_10day_mod[im,iseason] = tmp2

            tmp1 = LCL_mod[:,iseason]
            tmp2 = np.mean(tmp1[10*im:10*im+10])
            LCL_10day_mod[im,iseason] = tmp2

            EF_10day_mod[im,iseason] = lh_10day_mod[im,iseason]/(lh_10day_mod[im,iseason]+sh_10day_mod[im,iseason])

    #==================================================
    # Plots for observations
    #==================================================
    for iseason in range(nseasons):
        #==========================================================================
        # Plotting: Atmospheric coupling legs
        # SH/LH/EF vs. LCL
        #==========================================================================
        
        fig = plt.figure(figsize=[14,4], dpi=100)
        gs = gridspec.GridSpec(ncols=3,nrows=1,figure=fig)
        gs.update(wspace=0.25, hspace=0.15)

        ncols = 3
        nrows = 1    
        for row in range(nrows):
            for col in range(ncols):
                tmp = ncols*row+col
                ax = fig.add_subplot(gs[row,col])

                data2 = LCL_10day[0:nt_10day,iseason]/1000.
                
                if col==0:
                    data1 = sh_10day[0:nt_10day,iseason]
                    str_xlabel = 'Sensible heat flux (W/m\u00b2)'
                    if seasons[iseason]=='DJF': xmax = 100
                    if seasons[iseason]=='MAM': xmax = 150
                    if seasons[iseason]=='JJA': xmax = 200
                    if seasons[iseason]=='SON': xmax = 150
                    plt.xlim([0,xmax])
                    xx = xmax*0.6
                    xseq = np.linspace(5,0.8*xmax, num=500)
                if col==1:
                    data1 = lh_10day[0:nt_10day,iseason]
                    str_xlabel = 'Latent heat flux (W/m\u00b2)'
                    if seasons[iseason]=='DJF': xmax = 100
                    if seasons[iseason]=='MAM': xmax = 150
                    if seasons[iseason]=='JJA': xmax = 200
                    if seasons[iseason]=='SON': xmax = 150
                    plt.xlim([0,xmax])
                    xx = xmax*0.6
                    xseq = np.linspace(5,0.8*xmax, num=500)
                if col==2:
                    data1 = EF_10day[0:nt_10day,iseason]
                    str_xlabel = 'Evaporative fraction'
                    plt.xlim([0,1])
                    xx = 0.6
                    xseq = np.linspace(0.15, 0.85, num=500) 
    
                plt.scatter(data1, data2,s=30)
                b, a = np.polyfit(data1, data2, deg=1)
                r = scipy.stats.pearsonr(data1,data2)    # Pearson's r
                cc = '%.2f' % r[0]
                ax.plot(xseq, a + b * xseq, color="k", lw=2.5)
                plt.title('Obs. ('+seasons[iseason]+')',fontsize=14)        
                plt.xlabel(str_xlabel,fontsize=12)
                plt.ylim([0,3.5])
                plt.ylabel('LCL (km)',fontsize=12)
                plt.text(xx,2.8,"R = "+cc,fontsize=15)

        plt.savefig(output_path+'/figures/'+sites[0]+'/'+'Scatter_plot_'+seasons[iseason]+'_atmos_component_obs_'+sites[0]+'.png')

        #===========================================================
        # For models
        #===========================================================
      
        fig = plt.figure(figsize=[14,4], dpi=100)
        gs = gridspec.GridSpec(ncols=3,nrows=1,figure=fig)
        gs.update(wspace=0.25, hspace=0.15)

        ncols = 3
        nrows = 1    
        for row in range(nrows):
            for col in range(ncols):
                tmp = ncols*row+col
                ax = fig.add_subplot(gs[row,col])

                data2 = LCL_10day_mod[0:nt_10day_mod,iseason]/1000.

                if col==0:
                    data1 = sh_10day_mod[0:nt_10day_mod,iseason]
                    str_xlabel = 'Sensible heat flux (W/m\u00b2)'
                    if seasons[iseason]=='DJF': xmax = 100
                    if seasons[iseason]=='MAM': xmax = 150
                    if seasons[iseason]=='JJA': xmax = 200
                    if seasons[iseason]=='SON': xmax = 150
                    plt.xlim([0,xmax])
                    xx = xmax*0.6
                    xseq = np.linspace(5,0.8*xmax, num=500)
                if col==1:
                    data1 = lh_10day_mod[0:nt_10day_mod,iseason]
                    str_xlabel = 'Latent heat flux (W/m\u00b2)'
                    if seasons[iseason]=='DJF': xmax = 100
                    if seasons[iseason]=='MAM': xmax = 150
                    if seasons[iseason]=='JJA': xmax = 200
                    if seasons[iseason]=='SON': xmax = 150
                    plt.xlim([0,xmax])
                    xx = xmax*0.6
                    xseq = np.linspace(5,0.8*xmax, num=500)
                if col==2:
                    data1 = EF_10day_mod[0:nt_10day_mod,iseason]
                    str_xlabel = 'Evaporative fraction'
                    plt.xlim([0,1])
                    xx = 0.6
                    xseq = np.linspace(0.15, 0.85, num=500)
    
                plt.scatter(data1, data2,s=30)
                b, a = np.polyfit(data1, data2, deg=1)
                r = scipy.stats.pearsonr(data1,data2)    # Pearson's r
                cc = '%.2f' % r[0]
                #print(seasons[iseason],'r = ',cc)
                #print('data1: ',data1)
                #print('data2: ',data2)
                ax.plot(xseq, a + b * xseq, color="k", lw=2.5)
                plt.title('Mod. ('+seasons[iseason]+')',fontsize=14)
                plt.xlabel(str_xlabel,fontsize=12)
                plt.ylim([0,3.5])
                plt.ylabel('LCL (km)',fontsize=12)
                plt.text(xx,2.8,"R = "+cc,fontsize=15)

        plt.savefig(output_path+'/figures/'+sites[0]+'/'+'Scatter_plot_'+seasons[iseason]+'_atmos_component_testmod_'+sites[0]+'.png')

        #==========================================================================
        # Plotting: Terrestrial coupling legs
        # soil moisture vs. SH/LH/EF 
        #==========================================================================
    
        fig = plt.figure(figsize=[14,4], dpi=100)
        gs = gridspec.GridSpec(ncols=3,nrows=1,figure=fig)
        gs.update(wspace=0.25, hspace=0.15)

        for row in range(nrows):
            for col in range(ncols):
                tmp = ncols*row+col
                ax = fig.add_subplot(gs[row,col])

                data1 = sm_swats_10day[0:nt_10day,iseason]

                if col==0:
                    data2 = sh_10day[0:nt_10day,iseason]
                    str_ylabel = 'Sensible heat flux (W/m\u00b2)'
                    if seasons[iseason]=='DJF': ymax = 100
                    if seasons[iseason]=='MAM': ymax = 150
                    if seasons[iseason]=='JJA': ymax = 200
                    if seasons[iseason]=='SON': ymax = 150
                    plt.ylim([0,ymax])
                    yy = ymax*0.8
                    xseq = np.linspace(0.22,0.35,num=500)
                if col==1:
                    data2 = lh_10day[0:nt_10day,iseason]
                    str_ylabel = 'Latent heat flux (W/m\u00b2)'
                    if seasons[iseason]=='DJF': ymax = 100
                    if seasons[iseason]=='MAM': ymax = 150
                    if seasons[iseason]=='JJA': ymax = 200
                    if seasons[iseason]=='SON': ymax = 150
                    plt.ylim([0,ymax])
                    yy = ymax*0.8
                    xseq = np.linspace(0.22,0.35,num=500)
                if col==2:
                    data2 = EF_10day[0:nt_10day,iseason]
                    str_ylabel = 'Evaporative fraction'
                    plt.ylim([0,1])
                    yy = 0.098
                    xseq = np.linspace(0.22,0.35,num=500)        

                plt.scatter(data1, data2,s=30)
                b, a = np.polyfit(data1, data2, deg=1)
                r = scipy.stats.pearsonr(data1,data2)    # Pearson's r
                cc = '%.2f' % r[0]
                ax.plot(xseq, a + b * xseq, color="k", lw=2.5)
                plt.title('Obs. ('+seasons[iseason]+')',fontsize=14)
                plt.ylabel(str_ylabel,fontsize=12)
                plt.xlim([0.2,0.4])
                plt.xlabel('Soil moisture (m\u00b3/m\u00b3)',fontsize=12)
                plt.text(0.32,yy,"R = "+cc,fontsize=15)
    
        plt.savefig(output_path+'/figures/'+sites[0]+'/'+'Scatter_plot_'+seasons[iseason]+'_land_component_obs_'+sites[0]+'.png')
        #-------------------------------------------------------------------------
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=



