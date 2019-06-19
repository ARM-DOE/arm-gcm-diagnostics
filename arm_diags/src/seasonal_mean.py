import os
import glob
import cdms2
import cdutil
import numpy as np
import csv
from varid_dict import varid_longname

def var_seasons(var, seasons):
    "Calculate seasonal climatology of each variable"
    var_season_data = np.empty([len(seasons)])*np.nan
    cdutil.setTimeBoundsMonthly(var)
    for k, season in enumerate(seasons):
        if season == 'ANN':
            months = cdutil.times.Seasons('DJFMAMJJASON')
        else:
            months = cdutil.times.Seasons(str(season))
        var_season_data[k] = months.climatology(var)
    # convert units
    if var.id == 'tas':
        var_season_data = var_season_data-273.15

    if var.id == 'pr':
        var_season_data = var_season_data*3600.*24.
       
        
    return var_season_data


def seasonal_mean_table(parameter):
    """Calculate seasonal mean climatology"""
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
    test_var_season=np.empty([len(variables),len(seasons)])*np.nan
    test_file = glob.glob(os.path.join(test_path,'*'+test_model+'*mo*'+ sites[0]+'.nc')) #read in monthly test data
    fin = cdms2.open(test_file[0])
    
    print 'test_model',test_model

    for j, variable in enumerate(variables): 
        try:
            var = fin (variable)
            test_var_season[j, :] = var_seasons(var, seasons)

        except:
            print (variable+" not processed for " + test_model)
    fin.close()

    # Calculate for observational data
    obs_var_season=np.empty([len(variables),len(seasons)])*np.nan
    print 'ARM data'
    if sites[0] == 'sgp':
        obs_file = glob.glob(os.path.join(obs_path,'*ARMdiag*monthly_stat_'+ sites[0]+'.nc')) #read in monthly test data
        print obs_file
        fin = cdms2.open(obs_file[0])
        for j, variable in enumerate(variables): 
            try:
                var = fin (variable)
                obs_var_season[j, :] = var_seasons(var, seasons)
    
            except:
                print (variable+" not processed for obs")
        fin.close()
    else:
        obs_file = glob.glob(os.path.join(obs_path,'*ARMdiag*monthly_climo*'+ sites[0]+'.nc')) #read in monthly test data
        print obs_file
        fin = cdms2.open(obs_file[0]) 
        for j, variable in enumerate(variables): 
            #try:
               var = fin (variable) 
               print var.shape
               
               #tmp
               print np.nanmean(np.reshape(var, (4,3)),axis=1)
               obs_var_season[j,1:] = np.nanmean(np.reshape(var, (4,3)),axis=1)
               if variable == 'tas':
                   obs_var_season[j,1:] = obs_var_season[j,1:] -273.15
               if variable == 'pr':
                   obs_var_season[j,1:] = obs_var_season[j,1:] * 24.0
               if variable == 'prw':
                   obs_var_season[j,1:] = obs_var_season[j,1:] * 10.0
               obs_var_season[j,0] = np.nanmean(obs_var_season[j,1:])
               print obs_var_season
                
               #var24 = np.concatenate((var,var),axis=0)
               
            #except:
            #    print (variable+" not processed for obs")
        fin.close() 
         
   
  
    # Calculate cmip model seasonal mean climatology
    cmip_var_season=np.empty([len(ref_models),len(variables),len(seasons)])*np.nan
 
    for i, ref_model in enumerate(ref_models):
         ref_file = glob.glob(os.path.join(cmip_path,'*'+ref_model+'*mo*'+ sites[0]+'.nc')) #read in monthly cmip data
         print 'ref_model', ref_model
         if not ref_file :
             print (ref_model+" not found!") 
         else:
             fin = cdms2.open(ref_file[0])
         
             for j, variable in enumerate(variables): 
                 try:
                     var = fin (variable)
                     cmip_var_season[i, j, :] = var_seasons(var, seasons)

                 except:
                     print (variable+" not processed for " + ref_model)
             fin.close()  
    # Calculate multi-model mean
    mmm_var_season =  np.nanmean(cmip_var_season,axis=0)
    

    # Save data as a table
    #header=['Variables','Model','Obs','Model-Obs','CMIP5','RMSE']
    header=['Variables','Model','Obs','Model-Obs','CMIP5']
    var_longname = [ varid_longname[x] for x in variables]
    table_data = np.empty([len(variables),len(seasons),4])

    for k, season in enumerate(seasons):
        for j, variable in enumerate(variables):
            table_data[j,k,:] = (round(test_var_season[j,k],3), round(obs_var_season[j,k],3),round(test_var_season[j,k]-obs_var_season[j,k],3),round(mmm_var_season[j,k],3))
           
        with open (output_path+'/metrics/seasonal_mean_table_'+season+'_'+sites[0]+'.csv','w') as f1:
            writer=csv.writer(f1, delimiter=',',lineterminator='\n', quoting=csv.QUOTE_NONE)
            writer.writerow(header)
            #use tuple to generate csv 
            writer.writerows([c]+row.tolist() for c, row in zip(var_longname,table_data[:,k,:]))

    
    
    
    
    
