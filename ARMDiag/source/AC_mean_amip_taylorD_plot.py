import os,sys
import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt
from taylorD import TaylorDiagram
import config

mod = config.modelname

def AC_mean_amip_taylorD_plot():
    """ Prepare Taylor Diagram of annual cycle for set 2 of diag.."""
    pathname = os.path.dirname(sys.argv[0])
    basedir=os.path.abspath(pathname)+'/ARMDiag/'
    vas=['tas','pr','clt','hurs','hfss','hfls','rlus','rlds','rsus','rsds','ps','prw','cllvi','albedo']
    xaxis=['Surface Temperature (C)','Precipitation (mm/day)','Total Cloud Fraction (%)','Rel. Humidity (%)','Sensible Heat Flux (W/m2)','Latent Heat Flux(W/m2)','Upwelling LW (W/m2)','Downwelling LW (W/m2)','Upwelling SW (W/m2)','Downwelling SW (W/m2)','Surface Pressure (Pa)', 'Preciptable Water (mm)', 'Liquid Water Path (mm)','Surface Albedo']
    for va_ind in range(len(vas)):
        pr_cmip=genfromtxt(basedir+'cmip/'+vas[va_ind]+'_model_regrid_3x3_correct.csv')
        pr_mod=genfromtxt(basedir+'model/'+vas[va_ind]+'_'+mod+'_regrid_3x3_correct.csv')
        pr_obs=genfromtxt(basedir+'observation/all_'+vas[va_ind]+'_obs_regrid_3x3.csv')
        pr_obs=pr_obs[0]
        mod_num=pr_cmip.shape[0]-1
        pr_mmm=pr_cmip[mod_num,:]
        # Reference dapret
        data=pr_obs
        refstd = data.std(ddof=1)           # Reference standard deviation
        x=np.arange(12)
    
        # Compute stddev and correlation coefficient of models
        mod_num=pr_cmip.shape[0]-1
        m_all=[pr_cmip[x,:] for x in range(mod_num)]
        samples = np.array([ [m.std(ddof=1), np.corrcoef(data, m)[0,1]]
                         for m in m_all])
        mod_sample=np.array([ pr_mod[:].std(ddof=1), np.corrcoef(data, pr_mod[:])[0,1]])
        mmm_sample=np.array([ pr_cmip[mod_num,:].std(ddof=1), np.corrcoef(data, pr_cmip[mod_num,:])[0,1]])
    
        fig = plt.figure(figsize=(8,8))
        dia = TaylorDiagram(refstd, fig=fig,rect=111, label="Reference")
    
        # Add samples to Taylor diagram
        for i,(stddev,corrcoef) in enumerate(samples):
            dia.add_sample(stddev, corrcoef, marker='.',ms=10, c='grey')
    
        dia.add_sample(mod_sample[0], mod_sample[1],marker='.',ms=15, c='red',label='MOD') 
        dia.add_sample(mmm_sample[0], mmm_sample[1],marker='.',ms=15, c='b',label='MMM') 
        # Add RMS contours, and label them
        contours = dia.add_contours(colors='0.5')
        plt.clabel(contours, inline=1, fontsize=10)
        plt.title(xaxis[va_ind])
    
        # Add a figure legend
        fig.legend([dia.samplePoints[0],dia.samplePoints[-2],dia.samplePoints[-1]] ,
                   [ p.get_label() for p in [dia.samplePoints[0],dia.samplePoints[-2],dia.samplePoints[-1]] ],
                   numpoints=1,  loc='upper right',prop={'size':10})
        np.savetxt(basedir+'metrics/'+vas[va_ind]+'_'+mod+'std_corr.csv',mod_sample,fmt='%.3f')
        fig.savefig(basedir+'figures/AC_amip_taylorD_'+vas[va_ind]+'.png')
        plt.close('all')

#    plt.show()

