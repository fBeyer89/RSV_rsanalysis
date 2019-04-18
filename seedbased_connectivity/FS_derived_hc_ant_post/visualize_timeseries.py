# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 09:18:48 2017

@author: fbeyer
"""

import numpy as np
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
import numpy as N
import time
import os

with open('/data/pt_nro148/3T/restingstate_and_freesurfer/Lists/RSV_3T_Baseline_all_available_subjects.txt', 'r') as f:
    subjects = [line.strip() for line in f]

savedir='/data/pt_nro148/3T/restingstate_and_freesurfer/quality_reports/hippocampus_connectivity/'
basedir='/data/pt_nro148/3T/restingstate_and_freesurfer/wd/hipp_connectivity/'
c = canvas.Canvas(os.path.join(savedir,"HC_report.pdf"))
for subject in subjects:
        yloc=820
        stepsize=16
#        ts_l_ant = np.loadtxt(basedir+'left/'+subject+'/hc_connec/corr_ts/mean_TS/mapflow/_mean_TS1/TS.1D')
#        ts_r_ant = np.loadtxt(basedir+'right/'+subject+'/hc_connec/corr_ts/mean_TS/mapflow/_mean_TS1/TS.1D')
#        ts_l_post = np.loadtxt(basedir+'left/'+subject+'/hc_connec/corr_ts/mean_TS/mapflow/_mean_TS0/TS.1D')
#        ts_r_post = np.loadtxt(basedir+'right/'+subject+'/hc_connec/corr_ts/mean_TS/mapflow/_mean_TS0/TS.1D')
#        meanfd=np.loadtxt('/data/pt_nro148/3T/restingstate_and_freesurfer/quality_reports/poldrack_reports/'+subject+'/fd.txt')
#        #print (basedir+side+subject+'/hc_connec/corr_ts/mean_TS/mapflow/_mean_TS0/TS.1D')
#        x=np.arange(0,np.size(ts_l_ant))
#        f=plt.figure
#        plt.subplots_adjust(left=None, bottom=None, right=None, top=None,
#                wspace=None, hspace=0.5)
#        ax0 = plt.subplot(311)
#        plt.plot(x,meanfd,'blue',label='meanfd')
#        plt.plot(x,0.5*np.ones(shape=np.shape(meanfd)),'red',label='cutoff@0.5mm meanFD')
#        ax0.legend(loc='center', bbox_to_anchor=(0.5, 1.3),
#          ncol=3, fancybox=True, shadow=True)  
#        ax = plt.subplot(312)
#        plt.plot(x,ts_l_ant,'maroon',label='left anterior')
#        plt.plot(x,ts_l_post,'deeppink',label='left posterior')
#        ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.55),
#          ncol=3, fancybox=True, shadow=True)            
#        ax1=plt.subplot(313)
#        plt.plot(x,ts_r_ant,'b',label='right anterior')
#        plt.plot(x,ts_r_post,'g',label='right posterior')
#        ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 1.55),
#          ncol=3, fancybox=True, shadow=True)  
        
        
        imfile=savedir+subject+'_hc_ts.png'
        #plt.savefig(imfile, dpi=500, bbox_inches='tight')  
        #plt.show()   
        #plt.close()
        line='HC connectivity of subject %s' %subject
        c.drawString(10,yloc,line)
        ts_img_size=[400,220]
        yloc=yloc-(10+ts_img_size[1])
        c.drawImage(imfile,45,yloc,width=ts_img_size[0],height=ts_img_size[1])
        c.showPage()  
        
#
c.save()
 