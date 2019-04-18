# -*- coding: utf-8 -*-
"""
Created on Thu Dec  4 17:58:45 2014

@author: fbeyer
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Nov 14 12:09:10 2014

@author: fbeyer
"""


#do the complete registration in one workflow


#import the utility interface
import os
from nipype.interfaces.ants import Registration
#import nipype.interfaces.utility as util
from nipype.interfaces.utility import IdentityInterface, Function
import nipype.pipeline.engine as pe
import nipype.interfaces.io as nio
import nipype.interfaces.freesurfer as fs
import nipype.interfaces.fsl as fsl
import nipype.interfaces.afni as afni

#Workflow to create
check_freesurfer=pe.Workflow(name = "check_freesurfer")
check_freesurfer.base_dir = "/scr/kennedy2/data_fbeyer/BIPS/WDR/"

#define input files
input_Files=['LI03465793']
#define input nodes
infosource = pe.Node(IdentityInterface(fields=['subject_id']), name="infosource")
infosource.iterables = ('subject_id', input_Files)

dirsource = pe.Node(IdentityInterface(fields=['fs_dir']), name="dirsource")
dirsource.inputs.fs_dir = "/scr/kennedy2/data_fbeyer/freesurfer"

#datasink
#create the data sink Node
datasink = pe.Node(nio.DataSink(), name='datasink')
datasink.inputs.base_directory = '/scr/kennedy2/data_fbeyer/check_freesurfer'
datasink.parameterization=False
datasink.inputs.substitutions = [('__subject_id_', '')]

# import files from freesurfer
fs_import = pe.Node(interface=nio.FreeSurferSource(),
                 name = 'fs_import')
# convert Freesurfer T1 file to nifti
head_convert=pe.Node(fs.MRIConvert(out_type='niigz',
                                out_file='T1.nii.gz'),
                                name='head_convert')
# create brainmask from aparc+aseg with single dilation
def get_aparc_aseg(files):
    for name in files:
        if 'aparc+aseg' in name:
            return name

brainmask = pe.Node(fs.Binarize(min=0.5,    dilate=1,    out_type='nii.gz'),    name='brainmask')
# fill holes in mask, smooth, rebinarize
fillholes = pe.Node(fsl.maths.MathsCommand(args='-fillh -s 3 -thr 0.1 -bin',
                                        out_file='T1_brain_mask.nii.gz'),
                                        name='fillholes')
# mask T1 with the mask
brain = pe.Node(fsl.ApplyMask(out_file='T1_brain.nii.gz'),    name='brain')

# cortical and cerebellar white matter volumes to construct wm edge
# [lh cerebral wm, lh cerebellar wm, rh cerebral wm, rh cerebellar wm, brain stem]
wmseg = pe.Node(fs.Binarize(out_type='nii.gz',
                         match = [2, 7, 41, 46, 16],
                         binary_file='T1_brain_wmseg.nii.gz'),
            name='wmseg')
# make edge from wmseg to visualize coregistration quality
edge = pe.Node(fsl.ApplyMask(args='-edge -bin',
                          out_file='T1_brain_wmedge.nii.gz'),
       name='edge')


#visualize the segmentation
#apply smoothing
slicer = pe.Node(fsl.Slicer(sample_axial=6, image_width=750), name = 'visualize')

# connections
check_freesurfer.connect([
(infosource, fs_import, [('subject_id', 'subject_id')]),
(dirsource,  fs_import, [('fs_dir', 'subjects_dir')]),
(fs_import, brainmask, [(('aparc_aseg', get_aparc_aseg), 'in_file')]),
(fs_import, head_convert, [('T1', 'in_file')]),
(fs_import, wmseg, [(('aparc_aseg', get_aparc_aseg), 'in_file')]),
(brainmask, fillholes, [('binary_file', 'in_file')]),
(fillholes, brain, [('out_file', 'mask_file')]),
(head_convert, brain, [('out_file', 'in_file')]),
(wmseg, edge, [('binary_file', 'in_file'),
('binary_file', 'mask_file')]),
(head_convert, datasink, [('out_file', 'anat_head')]),
(fillholes, datasink, [('out_file', 'brain_mask')]),
(brain, datasink, [('out_file', 'anat_brain')]),
(wmseg, datasink, [('binary_file', 'wmseg')]),
(edge, datasink, [('out_file', 'wmedge')]),
(head_convert, slicer, [('out_file', 'in_file')]),
(edge, slicer,  [('out_file', 'image_edges')]),  
(fillholes, slicer, [('out_file', 'image_edges')]),   
(slicer, datasink,[('out_file', 'pictures.@wmedge')])
])

check_freesurfer.run()
