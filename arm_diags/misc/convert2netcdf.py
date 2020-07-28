import cdms2, MV2
import cdutil
import cdtime
import numpy as np
import numpy.ma as ma
import glob
import os
import scipy.io

#Read in Obs data
file_path = '/Users/zhang40/Documents/ARM_LLNL/ConvectionMetrics_UCLA/shared_ARM_diagnostics/Nauru_data/'
precip_filename = 'precip_nauru_1hravg_matchedtosondes_Apr2001_Aug2006.mat'
cwv_filename = 'cwv_nauru_sondes_Apr2001_Aug2006.mat'

precip_file1 = scipy.io.loadmat(file_path + precip_filename)
cwv_file1 = scipy.io.loadmat(file_path + cwv_filename)
#precip_file1 = scipy.io.loadmat(precip_filename)
#cwv_file1 = scipy.io.loadmat(cwv_filename)

print(cwv_file1)
cwv = cwv_file1['cwv_nauru_sondes_Apr2001_Aug2006']
print(cwv.shape)
precip = precip_file1['precip_nauru_1hravg_matchedtosondes_Apr2001_Aug2006']
cwv = np.squeeze(cwv)
precip = np.squeeze(precip)
#convective_onset_statistics(cwv, precip,'sondes')


out_file = cdms2.open('prw_nauru_sondes_Apr2001_Aug2006.nc','w')
start = "2001-04-01 00:00:00"
nTimes = cwv.shape[0]
time = cdms2.createAxis(list(range(nTimes)))
time.units = "hours since {}".format(start)
time.designateTime()
time.id = 'time'
data = MV2.array(np.arange(nTimes))
data[:] = cwv
data.setAxis(0,time)
data.id = "prw"
data.units = "mm"
cdutil.setTimeBoundsDaily(data, 24)
out_file.comment = "1 hourly averaged column water vapor derived from sondes from Apr2001_Aug2006.nc, postprocessed based on datastream-name"
out_file.timeperiod = 'time period for data'
out_file.write(data)

out_file = cdms2.open('pr_nauru_matchedtosondes_Apr2001_Aug2006.nc','w')
start = "2001-04-01 00:00:00"
nTimes = precip.shape[0]
time = cdms2.createAxis(list(range(nTimes)))
time.units = "hours since {}".format(start)
time.designateTime()
time.id = 'time'
data = MV2.array(np.arange(nTimes))
data[:] = precip
data.setAxis(0,time)
data.id = "pr"
data.units = "mm/hr"
cdutil.setTimeBoundsDaily(data, 24)
out_file.comment = "1 hourly averaged precipication matched to sondes from Apr2001_Aug2006.nc, postprocessed based on datastream-name"
out_file.timeperiod = 'time period for data'
out_file.write(data)


