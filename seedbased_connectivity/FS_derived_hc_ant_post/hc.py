# -*- coding: utf-8 -*-
"""
Created on Mon Feb  9 12:34:01 2015

@author: fbeyer
"""

from nipype.pipeline.engine import Node, Workflow, MapNode
import nipype.interfaces.fsl as fsl
import nipype.interfaces.freesurfer as fs
import nipype.interfaces.utility as util
import nipype.algorithms.rapidart as ra
import nipype.interfaces.io as nio

'''
Main workflow for denoising
Largely based on https://github.com/nipy/nipype/blob/master/examples/
rsfmri_vol_surface_preprocessing_nipy.py#L261
but denoising in anatomical space
'''
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 15:00:44 2015

@author: fbeyer
"""

import os
from load_prep_cog import load_prep_cog
from create_anterior_posterior_hc import create_anterior_posterior_hippocampus

def create_transform_hc(name='transform_hc'):

    transform_hc = Workflow(name='transform_hc')
    # Define nodes
    inputnode=Node(util.IdentityInterface(fields=['fs_subjects_dir', 
                                                  'fs_subject_id',
                                                  'anat_head',
                                                   'resolution',
                                                   'working_dir'
                                                 ]),name='inputnode')
    
    outputnode = Node(interface=util.IdentityInterface(fields=['hc_transformed_bin',
                                                           ]),
              name='outputnode')
              
              
              
### ALL OF THIS PART IS DEPRECATED NOW AS IT WRITES TO ONE FILE AND INTRODUCES ERROR IN ant-post division    
#    # import files from freesurfer
#    fs_import = Node(interface=nio.FreeSurferSource(),
#                 name = 'fs_import')
#
#    extract_hc= Node(fs.Binarize(out_type='nii.gz',
#                                      binary_file='hc.nii.gz'),
#                name='extract_hc')
#    #extract_hc.iterables= ('match', [[17],[53]])#
#    extract_hc.inputs.match=[53] #17=left, 53=right   
#
#    
#    #divide hc at center of gravity
#    #first determine center of gravity.
#    print os.getcwd()
#    center_og=Node(fsl.ImageStats(op_string= '-C >' + os.getcwd() + '/cog.txt'), name='center_og')
#    
#    #then round and calculate cutoff points
#    round_cog_dim = Node(util.Function(input_names=['textfile'],
#                                                   output_names=['y_coord_rounded', 'dim_y_anterior', 'dim_y_posterior'],
#                                                   function=load_prep_cog),
#                                     name='round_cog_dim')
#    round_cog_dim.inputs.textfile=os.getcwd() + '/cog.txt'
#     
#    #slow FSL way how to do it 
#    #cut image into two parts
##    roi_hc=Node(fsl.ExtractROI(), name='roi_hc')
##    roi_hc.inputs.x_min=0
##    roi_hc.inputs.x_size=-1
##    roi_hc.inputs.y_min=0
##    roi_hc.inputs.y_size=-1
##    
##    #now create an image with opposite size
##    roi_fill=Node(fsl.ExtractROI(), name='roi_fill')
##    roi_fill.inputs.x_min=0
##    roi_fill.inputs.x_size=-1
##    roi_fill.inputs.y_min=0
##    roi_fill.inputs.y_size=-1
##    roi_fill.inputs.z_min=0
##    
##    #multiply the image by 0
##    fill_zeros=Node(fsl.ImageMaths(), name='fill_zeros')
##    fill_zeros.inputs.op_string= '-mul 0'
##    
##    #concatenate two files for merging
##    def merge_files(file1,file2):
##        print "XXXXXXXXX"
##        print "mergefiles function"
##        merged_list=[file1, file2]
##        print merged_list
##        return [file1, file2]
##    conc = Node(util.Function(input_names=['file1', 'file2'],
##                              output_names=['merged_list'], function=merge_files),
##                              name='conc')    
##    
##
##    
##    #merge files
##    merge=Node(fsl.Merge(), name='merge')
##    merge.inputs.dimension='z'
#       
#    antpost=Node(util.Function(input_names=['in_file', 'cog', 'working_dir','subject_id'],#, 
#                               output_names=['outvalue'],
#                               function=create_anterior_posterior_hippocampus),
#                               name='antpost')
    
    
#    #resample to functional space (128x128x128 (2x2x2) or in LIFE (85x85x85 (3x3x3mm))
    #using from NOW on especially calculated division!

    def iterable_list(fs_subjects_dir, fs_subject_id):
        filename= [fs_subjects_dir + '/'+ fs_subject_id + '/mri/PCA_rhposterior.nii.gz', fs_subjects_dir + '/'+ fs_subject_id + '/mri/PCA_rhhead.nii.gz']
        print filename
        return filename
    
    it_list=Node(util.Function(input_names=['fs_subjects_dir', 'fs_subject_id'],output_names=['filename'],function=iterable_list),
                 name='it_list')
        
        
    resample = MapNode(interface=fsl.FLIRT(datatype='float',
    out_file='hc_resampled.nii.gz'),
    name = 'resample', iterfield='in_file')
                   
    
    #binarize mask in functional space
    binarize=MapNode(fsl.ImageMaths(op_string='-thr 0.99 -bin', #maybe lower threshold from 0.5 to 0.2?
                                 out_file='hc_mask_thr0.99.nii.gz'), 
                                 name='binarize',iterfield='in_file') 
  
    
    transform_hc.connect([
#                      (inputnode, fs_import, [('fs_subjects_dir','subjects_dir'),
#                                             ('fs_subject_id', 'subject_id')
#                                             ]),
#                      (inputnode, antpost, [('working_dir','working_dir'),
#                                            ('fs_subject_id', 'subject_id')
#                                             ]),
#                      
#                      (fs_import, extract_hc, [('aseg', 'in_file')]),
#                      (extract_hc, center_og, [('binary_file', 'in_file')]),
                      #for anterior ROI_
                      #(round_cog_dim, roi_hc, [('y_coord_rounded', 'z_min'), ('dim_y_anterior', 'z_size')]),
                      #(extract_hc, roi_hc, [('binary_file', 'in_file')]),    
                      #create empty roi
                      #(extract_hc, roi_fill, [('binary_file', 'in_file')]),    
                      #(round_cog_dim, roi_fill, [('dim_y_posterior', 'z_size')]),
                      #fill it with zeros
                      #(roi_fill, fill_zeros, [('roi_file', 'in_file')]),
                      #concatenate and merge files
                      #(fill_zeros, conc, [('out_file', 'file1')]),
                      #(roi_hc, conc, [('roi_file', 'file2')]),
                      #(conc, merge, [('merged_list', 'in_files')])
                      
#                      (extract_hc, antpost, [('binary_file', 'in_file')]),     
#                      (round_cog_dim, antpost, [('y_coord_rounded', 'cog')]),
                      #(antpost, resample, [('out_file', 'in_file')]),
                      (inputnode, it_list, [('fs_subjects_dir','fs_subjects_dir'),
                                            ('fs_subject_id', 'fs_subject_id')
                                             ]),  
                      #(antpost, resample, [('outvalue', 'save_log')]),                       
                      (it_list, resample, [('filename', 'in_file')]),
                      (inputnode, resample, [('anat_head', 'reference')]),
                      (inputnode, resample, [('resolution', 'apply_isoxfm')]),
                      (resample, binarize, [('out_file', 'in_file')]),                             
                      (binarize, outputnode, [('out_file', 'hc_transformed_bin')])
                      ])
    
    
    return transform_hc