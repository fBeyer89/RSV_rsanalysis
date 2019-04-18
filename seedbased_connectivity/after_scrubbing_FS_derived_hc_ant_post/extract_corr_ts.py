# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 08:48:41 2015

@author: fbeyer
"""
from nipype.pipeline.engine import Node, Workflow, MapNode
import nipype.interfaces.fsl as fsl
import nipype.interfaces.afni as afni
import nipype.interfaces.freesurfer as fs
import nipype.interfaces.utility as util
import nipype.algorithms.rapidart as ra
import nipype.interfaces.afni as afni
from nipype.interfaces.utility import Function


def create_corr_ts(name='corr_ts'):

    corr_ts = Workflow(name='corr_ts')
    # Define nodes
    inputnode=Node(util.IdentityInterface(fields=['ts', 
                                                  'hc_mask', 
                                                  ]),name='inputnode')
    
    outputnode = Node(interface=util.IdentityInterface
                     (fields=['corrmap', 'corrmap_z', 'hc_ts']), name='outputnode')
 
   
   
   
    #extract mean time series of mask
    mean_TS = MapNode(interface=fsl.ImageMeants() , name = "mean_TS", iterfield='mask' )
    #iterate over using Eigenvalues or mean
    #mean_TS.iterables = ("eig", [True, False])
    #mean_TS.inputs.order = 1
    #mean_TS.inputs.show_all = True
    mean_TS.inputs.eig=False #use only mean of ROI    
    mean_TS.inputs.out_file = "TS.1D"   
   
   
   
    #calculate correlation of all voxels with seed voxel
    corr_TS = MapNode(interface=afni.Fim(), name = 'corr_TS', iterfield='ideal_file')
    corr_TS.inputs.out = 'Correlation'
    corr_TS.inputs.out_file = "corr.nii.gz"
    
    apply_FisherZ = MapNode(interface = afni.Calc(), name = "apply_FisherZ",  iterfield='in_file_a')
    apply_FisherZ.inputs.expr = 'log((1+a)/(1-a))/2'  #log = ln
    apply_FisherZ.inputs.out_file =  'corr_Z.nii.gz'
    apply_FisherZ.inputs.outputtype = "NIFTI"
                  
    corr_ts.connect([
                    (inputnode, mean_TS, [('hc_mask', 'mask')]),
                    (inputnode, mean_TS, [('ts', 'in_file')]),
                    (mean_TS, outputnode, [('out_file', 'hc_ts')]),
                    (inputnode, corr_TS,[('ts', 'in_file')]),
                    (mean_TS,corr_TS,[('out_file', 'ideal_file')]),
                    (corr_TS, apply_FisherZ, [('out_file', 'in_file_a')]),
                    (corr_TS, outputnode, [('out_file', 'corrmap')]),
                    (apply_FisherZ, outputnode, [('out_file', 'corrmap_z')])     

                    ])
                        
                          
    return corr_ts