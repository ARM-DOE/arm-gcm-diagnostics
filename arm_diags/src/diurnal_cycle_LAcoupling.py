#===========================================================================================================================
# Program for generate the diurnal cycle on Land-Atmosphere Coupling
#---------------------------------------------------------------------------------------------------------------------------
# V4 Development
    # ----------------------------------------------------------------------------------------------------
    # Cheng Tao - Jul2024 @ LLNL
    # ### Diurnal cycle of SH, LH, T_srf, RH_srf, LCL, PBL
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
from .utils import get_diurnal_cycle_seasons
import MV2
import matplotlib.gridspec as gridspec
import scipy.stats
from scipy import interpolate
import calendar
import math

def diurnal_cycle_LAcoupling_plot(parameter):
    variables = parameter.variables
    test_path = parameter.test_data_path
    test_model = parameter.test_data_set
    obs_path = parameter.obs_path
    cmip_path = parameter.cmip_path
    output_path = parameter.output_path
    sites = parameter.sites
    varnames = parameter.varnames
    units = parameter.units
    seasons = parameter.season
    nseasons = len(seasons)
    nvariables = len(variables)

    print('test_path: ',test_path)

    if not os.path.exists(os.path.join(output_path,'figures',sites[0])):
        os.makedirs(os.path.join(output_path,'figures',sites[0]))

    #==========================================================================
    # Calculate for test model data
    #==========================================================================
    test_file = glob.glob(os.path.join(test_path,sites[0][:3]+'testmodel3hrLAcoupling'+sites[0][3:5].upper()+'*.nc' )) 
    print('Processing test_file: ',test_file)
    fin1 = cdms2.open(test_file[0])
    
    #==========================================================================
    # Calculate for observational data
    #==========================================================================
    print('ARM data',sites[0])
    obs_file = glob.glob(os.path.join(obs_path,sites[0][:3]+'armdiagsLAcoupling' + sites[0][3:5].upper()+'*c1.nc')) #read in data
    print('Processing obs_file',obs_file)
    fin = cdms2.open(obs_file[0])
   
    for ivar in range(nvariables):
        #============================
        # Seasons: for observations
        #============================
        var = fin(variables[ivar])           
        years_obs = list(range(2004,2016))
        nyears_obs = len(years_obs)

        #var_seasons = get_seasonal(var,seasons,years_obs)    #[year,season,90,24] 
        var_seasons = get_diurnal_cycle_seasons(var,seasons,years_obs)
        narray = nyears_obs*365
        var_seasons1 = np.empty([nseasons,narray,24])*np.nan
        var_array_err = np.empty([nseasons,24])*np.nan
        var_array = np.empty([nseasons,24])*np.nan
        for iseason in range(nseasons):
            for iyear in range(nyears_obs):
                for iday in range(365):
                    var_seasons1[iseason,365*iyear+iday,:] = var_seasons[iyear,iseason,iday,:]
 
            array_tmp = var_seasons1[iseason,:,:] 
            data0 = np.nanstd(array_tmp,axis=0) #stddev 
            var_array_err[iseason,:] = data0/(math.sqrt(narray))
            var_array[iseason,:] = np.nanmean(array_tmp,axis=0)
            
        #==========================
        # Seasons: for models
        #==========================
        try:
            var_mod = fin1(variables[ivar])  
            years_mod = list(range(2003,2015))
            nyears_mod = len(years_mod)

            #var_mod_seasons = get_seasonal_3hr(var_mod,seasons,years_mod)    #[year,season,90,24]
            var_mod_seasons = get_diurnal_cycle_seasons(var_mod,seasons,years_mod)
            narray = nyears_mod*365
            var_mod_seasons1 = np.empty([nseasons,narray,8])*np.nan
            var_mod_array_err = np.empty([nseasons,8])*np.nan
            var_mod_array = np.empty([nseasons,8])*np.nan
            for iseason in range(nseasons):
                for iyear in range(nyears_mod):
                    for iday in range(365):
                        var_mod_seasons1[iseason,365*iyear+iday,:] = var_mod_seasons[iyear,iseason,iday,:]
 
                array_tmp = var_mod_seasons1[iseason,:,:]
                data0 = np.nanstd(array_tmp,axis=0) #stddev
                var_mod_array_err[iseason,:] = data0/(math.sqrt(narray))
                var_mod_array[iseason,:] = np.nanmean(array_tmp,axis=0)
        except:
            var_mod_array_err = np.empty([nseasons,8])*np.nan
            var_mod_array = np.empty([nseasons,8])*np.nan

        #==========================================================================
        # Plotting: Diurnal cycle (daytime)
        #==========================================================================
        for iseason in range(nseasons):
            fig = plt.figure(figsize=[8,4], dpi=100)
            xax = np.array([x for x in range(26)])-0.5
            y_data = np.empty([26])*np.nan
            y_data[0:19] = var_array[iseason,5:24]  
            y_data[19:26] = var_array[iseason,0:7]
         
            e_data = np.empty([26])*np.nan
            e_data[0:19] = var_array_err[iseason,5:24]
            e_data[19:26] = var_array_err[iseason,0:7]
            plt.errorbar(xax,y_data,e_data,color='black',label='OBS',linewidth=2)

            
            if variables[ivar]=='SH' or variables[ivar]=='LH':
                xax1 = np.array([x for x in range(10)])*3-1.5
            else:
                xax1 = np.array([x for x in range(10)])*3-3.0
            y1_data = np.empty([10])*np.nan
            y1_data[0:7] = var_mod_array[iseason,1:8]
            y1_data[7:10] = var_mod_array[iseason,0:3]

            e1_data = np.empty([10])*np.nan
            e1_data[0:7] = var_mod_array_err[iseason,1:8]
            e1_data[7:10] = var_mod_array_err[iseason,0:3]
            plt.errorbar(xax1,y1_data,e1_data,color='red',label='MOD',linewidth=2)

            plt.ylabel(units[ivar],fontsize=12)
            plt.title(variables[ivar]+' ('+seasons[iseason]+')',fontsize=14)
            plt.xticks([0,2,4,6,8,10,12,14,16,18,20,22,24],\
               ["0","2","4","6","8","10","12","14","16","18","20","22","24"])
            plt.xlabel('LST (hour)',fontsize=12)
            plt.xlim([-0.1,24.1])
            if variables[ivar]=='pbl':
                plt.xlim([7.4,17.6])
            plt.legend()
            plt.savefig(output_path+'/figures/'+sites[0]+'/'+'Diurnal_cycle_'+seasons[iseason]+'_'+variables[ivar]+'_'+sites[0]+'.png')
            

    fin.close()
