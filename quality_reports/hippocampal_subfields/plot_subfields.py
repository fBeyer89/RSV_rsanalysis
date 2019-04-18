# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 09:52:52 2017

@author: fbeyer
"""
import nibabel as nb
import numpy as np
#import seaborn as sns
from pylab import cm
from nipype.interfaces.freesurfer.preprocess import ApplyVolTransform
from nipy.labs import viz
from misc import plot_vline
from matplotlib.figure import Figure
from matplotlib.backends.backend_pdf import FigureCanvasPdf as FigureCanvas
from matplotlib.gridspec import GridSpec
import pylab as plt

def plot_hipp_subfields(brain_file, subfield_file,figsize=(40.7,20.3)):
       
    fig = plt.figure(figsize=figsize)
    ax = plt.subplot(1,1,1)
    
    print "hello"
    brain = nb.load(brain_file).get_data()
    brain_affine = nb.load(brain_file).get_affine()
    subfield = nb.load(subfield_file).get_data()
    subfield_affine = nb.load(subfield_file).get_affine()
    
    plt.histogram(subfield[:])
    #
    #plt.imshow(subfield[:,:,175], cmap="gray", origin="lower")
    #plt.show()
    subfield[subfield>1]=1
    slicer = viz.plot_anat(np.asarray(brain),np.asarray(brain_affine), 
                           cut_coords=np.arange(-238, -220, 2),#None, #[0,50,100,150,200,250],
                           slicer='z',
                           black_bg=True,
                           cmap = cm.Greys_r,  # @UndefinedVariable
                           figure = fig,
                           axes = ax,
                           draw_cross = False)
    slicer.edge_map(np.asarray(subfield), np.asarray(subfield_affine),color='r')
#    
#    fig.suptitle('subfields', fontsize='14')
    plt.show()
    
    return fig
    
    
plot_hipp_subfields('/nobackup/schiller2/RSV_7T_preprocessing/hippocampal_subfields_QA/wd/reports/_subject_id_01/brain_convert/brain.nii.gz','/nobackup/schiller2/RSV_7T_preprocessing/hippocampal_subfields_QA/wd/reports/_subject_id_01/extract_subfields/hc.nii.gz')