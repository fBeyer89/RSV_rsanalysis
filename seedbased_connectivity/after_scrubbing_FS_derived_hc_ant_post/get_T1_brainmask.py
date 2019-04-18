# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 14:53:04 2015

@author: fbeyer
"""
from nipype.pipeline.engine import Node, Workflow, MapNode
import nipype.interfaces.fsl as fsl
import nipype.interfaces.freesurfer as fs
import nipype.interfaces.utility as util
import nipype.algorithms.rapidart as ra
import nipype.interfaces.afni as afni
from nipype.interfaces.utility import Function
import nipype.interfaces.io as nio

def create_get_T1_brainmask(name='get_T1_brainmask'):

    get_T1_brainmask = Workflow(name='get_T1_brainmask')
    # Define nodes
    inputnode=Node(util.IdentityInterface(fields=['fs_subjects_dir', 
                                                  'fs_subject_id', 
                                                  ]),name='inputnode')
    
    outputnode = Node(interface=util.IdentityInterface(fields=['T1', 'brain_mask'
                                                           ]),
              name='outputnode')
    
    # import files from freesurfer
    fs_import = Node(interface=nio.FreeSurferSource(),
                 name = 'fs_import')

    #transform to nii
    convert_mask = Node(interface=fs.MRIConvert(), name = "convert_mask")
    convert_mask.inputs.out_type = "niigz"
    convert_T1 = Node(interface=fs.MRIConvert(), name = "convert_T1")
    convert_T1.inputs.out_type = "niigz"
    
    #binarize brain mask (like done in Lemon_Scripts_mod/struct_preproc/mgzconvert.py)
    brain_binarize=Node(fsl.ImageMaths(op_string='-bin', out_file='T1_brain_mask.nii.gz'), name='brain_binarize')
  
    
    get_T1_brainmask.connect([
                             (inputnode, fs_import, [('fs_subjects_dir','subjects_dir'),
                                                     ('fs_subject_id', 'subject_id')]),
                             (fs_import, convert_mask,   [('brainmask', 'in_file')]),
                             (fs_import, convert_T1,     [('T1', 'in_file')]),
                             (convert_mask, brain_binarize, [('out_file','in_file')]),
                             (brain_binarize,outputnode,  [('out_file','brain_mask')]),
                             (convert_T1, outputnode,    [('out_file','T1')])
    ])
    
 



    
    return get_T1_brainmask