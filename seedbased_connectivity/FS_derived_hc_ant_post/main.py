# -*- coding: utf-8 -*-
"""
Created on Mon Feb  9 12:26:20 2015

@author: fbeyer
"""

from nipype.pipeline.engine import Node, Workflow
import nipype.interfaces.utility as util
import nipype.interfaces.io as nio
import nipype.interfaces.fsl as fsl



from hc import create_transform_hc
#from create_corr_maps import create_corr_ts
from extract_corr_ts import create_corr_ts
from get_T1_brainmask import create_get_T1_brainmask
from ants_registration import create_ants_registration_pipeline
from smoothing import create_smoothing_pipeline

'''
Main workflow for seed-based hc connectivity preprocessing.
====================================================
Uses file structure set up by conversion script.
'''
def create_hc_connec(subject, working_dir, data_dir,
                  freesurfer_dir, 
                  out_dir,epi_resolution, 
                  standard_brain,
                  standard_brain_resampled, 
                  standard_brain_mask,
                  standard_brain_mask_resampled,
                  fwhm_smoothing,
                  side):
    # set fsl output type to nii.gz
    fsl.FSLCommand.set_default_output_type('NIFTI_GZ')
    # main workflow
    hc_connec = Workflow(name='hc_connec_thr099')
    hc_connec.base_dir = working_dir
    hc_connec.config['execution']['crashdump_dir'] = hc_connec.base_dir + "/crash_files"
    
    
    # select files
    templates={
    'rest_head': 'resting_state/denoise/rest_preprocessed_nativespace.nii.gz', #denoised and bandpass-filtered native space (2x2x2mm) image
    #'rest_head': 'scrubbed_interpolated/denoise/rest_denoised_scrubbed_int_bp.nii.gz', #denoised, scrubbed, interp, bp-filtered native space
    'ants_affine':  'structural/transforms2mni/transform0GenericAffine.mat',
    'ants_warp':    'structural/transforms2mni/transform1Warp.nii.gz',
    'ts_smoothed_nativ': 'resting_state/denoise/rest_preprocessed_nativespace.nii.gz'

    }
         
    selectfiles = Node(nio.SelectFiles(templates, base_directory=data_dir),    name="selectfiles")

 
    #get T1 brainmask
    get_T1_brainmask=create_get_T1_brainmask()    
    get_T1_brainmask.inputs.inputnode.fs_subjects_dir=freesurfer_dir
    get_T1_brainmask.inputs.inputnode.fs_subject_id=subject


    #workflow to extract HC and transform into individual space
    transform_hc=create_transform_hc()
    transform_hc.inputs.inputnode.fs_subjects_dir=freesurfer_dir
    transform_hc.inputs.inputnode.fs_subject_id=subject
    transform_hc.inputs.inputnode.resolution=2
    transform_hc.inputs.inputnode.working_dir=working_dir
    
   
    #workflow to extract timeseries and correlate
    corr_ts=create_corr_ts()
    
    #workflow to tranform correlations to MNI space
    ants_registration=create_ants_registration_pipeline()
    ants_registration.inputs.inputnode.ref=standard_brain #_resampled: 2x2x2mm brain for RSV
    
    
    #
    smoothing = create_smoothing_pipeline() 
    smoothing.inputs.inputnode.fwhm=fwhm_smoothing
    #sink to store files
    sink = Node(nio.DataSink
    (parameterization=True,
    base_directory=out_dir),
#   substitutions=[('_binarize', 'binarize'), -> don't really seem to work and I don't know why.
#                   #('_binarize', 'anterior_hc'),
#                   ('_ants_reg1', 'posterior_hc'),
#                   #('_ants_reg', 'anterior_hc'),
#                   ('_smooth1', 'posterior_hc'),
#                   ('_smooth0', 'anterior_hc'),
#                   ('corr_Z_trans', 'corr_Z_MNI')],
    name='sink')
    
    sink.inputs.substitutions=[('_binarize0', 'posterior_hc'),
                               ('_binarize1', 'anterior_hc'),
                               ('_ants_reg0', 'posterior_hc'),
                               ('_ants_reg1', 'anterior_hc'),
                               ('_smooth0', 'posterior_hc'),
                               ('_smooth1', 'anterior_hc'),
                               ('_apply_FisherZ0', 'posterior_hc'),
                               ('_apply_FisherZ1', 'anterior_hc')]
    
    
    
    # connections
    hc_connec.connect([
    (get_T1_brainmask, transform_hc, [('outputnode.T1', 'inputnode.anat_head')]),  
    #(selectfiles, transform_hc, [('rest_head', 'inputnode.anat_head')]),  
    (selectfiles, corr_ts, [('ts_smoothed_nativ', 'inputnode.ts')]),
    (transform_hc, corr_ts, [('outputnode.hc_transformed_bin', 'inputnode.hc_mask')]),  
    (transform_hc,sink, [('outputnode.hc_transformed_bin', 'hc_connectivity_thr099.'+side+'.hc_masks')]),
    (corr_ts, sink, [('outputnode.corrmap_z', 'hc_connectivity_thr099.'+side+'.corr.nativespace.@transformed')]),
    (corr_ts, ants_registration,    [('outputnode.corrmap_z', 'inputnode.corr_Z')]),
    (selectfiles, ants_registration, [('ants_affine', 'inputnode.ants_affine')] ),
    (selectfiles, ants_registration, [('ants_warp', 'inputnode.ants_warp')] ),

    (ants_registration, sink, [('outputnode.ants_reg_corr_Z', 'hc_connectivity_thr099.'+side+'.corr.ants')]),
    (ants_registration, smoothing, [('outputnode.ants_reg_corr_Z', 'inputnode.ts_transformed')]),

    (smoothing, sink,  [('outputnode.ts_smoothed', 'hc_connectivity_thr099.'+side+'.corr.smoothed')]),
    
    ])

    
    hc_connec.run() #it can't run in multiproc as in one moment one file is hardcoded and saved to the disk which is
    #not obvious for the distributing system
    # 'plugin='MultiProc'plugin='CondorDAGMan'))plugin='MultiProc'
    #func_preproc.run()plugin='CondorDAGMan'plugin='CondorDAGMan'plugin='CondorDAGMan'
