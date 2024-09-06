#===========================================================================================================================
# Functions for calculate annual/seasonal cycle from monthly data -- Original written by Dr. Chengzhu Zhang @ LLNL
#---------------------------------------------------------------------------------------------------------------------------
# V3 Development
    # ---------------------------------------------------------------------------------------
    # Xiaojian Zheng - Nov2021
    # ### Add the array treatment: filled the output masked (missing) value with numpy NaN
    # ### to avoid the issue of plotting masked value as 0 value in the plotting code
    # ---------------------------------------------------------------------------------------
#===========================================================================================================================

import numpy as np
import numpy.ma as ma
import cdms2
import cdutil
import pdb
from copy import deepcopy
import MV2
import calendar

def climo(var, season):
    """
    Compute the climatology for var for the given season.
    The returned variable must be 2 dimensional.
    """
    season_idx = {
        '01': [1,0,0,0,0,0,0,0,0,0,0,0],
        '02': [0,1,0,0,0,0,0,0,0,0,0,0],
        '03': [0,0,1,0,0,0,0,0,0,0,0,0],
        '04': [0,0,0,1,0,0,0,0,0,0,0,0],
        '05': [0,0,0,0,1,0,0,0,0,0,0,0],
        '06': [0,0,0,0,0,1,0,0,0,0,0,0],
        '07': [0,0,0,0,0,0,1,0,0,0,0,0],
        '08': [0,0,0,0,0,0,0,1,0,0,0,0],
        '09': [0,0,0,0,0,0,0,0,1,0,0,0],
        '10': [0,0,0,0,0,0,0,0,0,1,0,0],
        '11': [0,0,0,0,0,0,0,0,0,0,1,0],
        '12': [0,0,0,0,0,0,0,0,0,0,0,1],
        'DJF':[1,1,0,0,0,0,0,0,0,0,0,1],
        'MAM':[0,0,1,1,1,0,0,0,0,0,0,0],
        'JJA':[0,0,0,0,0,1,1,1,0,0,0,0],
        'SON':[0,0,0,0,0,0,0,0,1,1,1,0],
        'ANN':[1,1,1,1,1,1,1,1,1,1,1,1],
    }

    # Redefine time to be in the middle of the time interval
    var_time = var.getTime()
    if var_time is None:
        # Climo cannot be ran on this variable.
        return var

    tbounds = var_time.getBounds()
    if tbounds is None:
        cdutil.setTimeBoundsMonthly(var)
        tbounds = var.getTime().getBounds()
        
    var_time[:] = 0.5*(tbounds[:,0]+tbounds[:,1])
    var_time_absolute = var_time.asComponentTime()

    # Compute time length
    dt = tbounds[:,1] - tbounds[:,0]

    # Convert to masked array
    v = var.asma()

    # Compute climatology
    if season == 'ANNUALCYCLE':
        cycle = ['01','02','03','04','05','06','07','08','09','10','11','12']
    elif season == 'SEASONALCYCLE':
        cycle = ['DJF','MAM','JJA','SON']
    else:
        cycle = season

    ncycle = len(cycle)
    climo = ma.zeros([ncycle])#+list(np.shape(v))[1:])
    for n in range(ncycle):
        idx = np.array( [ season_idx[cycle[n]][var_time_absolute[i].month-1]
                          for i in range(len(var_time_absolute)) ], dtype=int).nonzero()
        climo[n] = ma.average(v[idx], axis=0, weights=dt[idx])

    # ---------------------------------------------------------------------------------------
    # filled the masked array with NaN [XZ]
    climo = climo.filled(np.nan)
    # ---------------------------------------------------------------------------------------

    if var.id == 'tas':
        climo  = climo - 273.15

    if var.id == 'pr':
        climo = climo*3600.*24.

    return climo

#============================================================================================
# Functions to get the diurnal cycle for particular seasons/years
# Output: var_seasons [nyears,nseasons,365,nhour] 
#============================================================================================

def get_diurnal_cycle_seasons(var,seasons,years):
    
    '''Get seasonal data for each variable'''
    nyears = len(years)
    nseasons = len(seasons)
    t0 = 0

    time = var.getTime()[:]
    if time[1]-time[0]==1: nhour=24
    if time[1]-time[0]==3: nhour=8
    #print('Time resolution: ', nhour)

    var_seasons = MV2.zeros([nyears,nseasons,365,nhour])*np.nan  #diurnal cycle for each day
    for iyear in range(nyears):
        if calendar.isleap(int(years[iyear]))==True:
            nday = 366
        else:
            nday = 365
        ntime = int(nday*nhour)
        var1 = var[t0:t0+ntime]
        var1_ext = np.concatenate((var1,var1),axis=0)
        t0 = t0+ntime

        for iseason in range(nseasons):
            if seasons[iseason]=='ANN':
                length = int(365*nhour)
                var_seasons0 = var1[0:length]
                var_seasons1 = np.reshape(var_seasons0,(365,nhour))
                var_seasons[iyear,iseason,:,:] = var_seasons1
            else:
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
                var_seasons0 = var1_ext[int(t1*nhour):int(t1*nhour)+90*nhour]
                var_seasons1 = np.reshape(var_seasons0,(90,nhour))
                var_seasons[iyear,iseason,0:90,:] = var_seasons1

    return var_seasons


