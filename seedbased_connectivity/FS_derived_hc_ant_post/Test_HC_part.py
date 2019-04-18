# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 10:23:08 2017

@author: fbeyer
"""

#test only hippocampus_part
from nipype.pipeline.engine import Node, Workflow
import nipype.interfaces.utility as util
import nipype.interfaces.io as nio
import nipype.interfaces.fsl as fsl
from hc import create_transform_hc
from get_T1_brainmask import create_get_T1_brainmask

freesurfer_dir="/data/pt_nro148/3T/restingstate_and_freesurfer/preprocessing/freesurfer"
subject='RSV002'
working_dir="/data/pt_nro148/3T/restingstate_and_freesurfer/wd/hipp_connectivity/left/" + subject

hc_connec = Workflow(name='hc_connec')
hc_connec.base_dir = working_dir


get_T1_brainmask=create_get_T1_brainmask()    
get_T1_brainmask.inputs.inputnode.fs_subjects_dir=freesurfer_dir
get_T1_brainmask.inputs.inputnode.fs_subject_id=subject


transform_hc=create_transform_hc()
transform_hc.inputs.inputnode.fs_subjects_dir=freesurfer_dir
transform_hc.inputs.inputnode.fs_subject_id=subject
transform_hc.inputs.inputnode.resolution=2
transform_hc.inputs.inputnode.working_dir=working_dir

hc_connec.connect([
    (get_T1_brainmask, transform_hc, [('outputnode.T1', 'inputnode.anat_head')])
    ])
    
hc_connec.run()