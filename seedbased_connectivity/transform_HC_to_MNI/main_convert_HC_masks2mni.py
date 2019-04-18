# -*- coding: utf-8 -*-
"""
Created on Mon Feb  9 12:26:20 2015

@author: fbeyer
"""

from nipype.pipeline.engine import Node, Workflow
import nipype.interfaces.utility as util
import nipype.interfaces.io as nio
import nipype.interfaces.fsl as fsl



from ants_registration import create_ants_registration_pipeline

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
                  side, half):
    # set fsl output type to nii.gz
    fsl.FSLCommand.set_default_output_type('NIFTI_GZ')
    # main workflow
    hc_connec = Workflow(name='transform_hc_mni')
    hc_connec.base_dir = working_dir
    hc_connec.config['execution']['crashdump_dir'] = hc_connec.base_dir + "/crash_files"
    
    
    # select files
    templates={
    'input': 'hc_connectivity_thr099/'+side+'/hc_masks/'+half+'/hc_mask_thr0.99.nii.gz',
    #'hc_connectivity/left/hc_masks/anterior_hc/hc_mask.nii.gz',
    #
    'ants_affine':  'structural/transforms2mni/transform0GenericAffine.mat',
    'ants_warp':    'structural/transforms2mni/transform1Warp.nii.gz',

    }
         
    selectfiles = Node(nio.SelectFiles(templates, base_directory=data_dir),    name="selectfiles")

    
    #workflow to tranform correlations to MNI space
    ants_registration=create_ants_registration_pipeline()
    ants_registration.inputs.inputnode.ref=standard_brain #_resampled: 2x2x2mm brain for RSV
    
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
    
    sink.inputs.substitutions=[('hc_mask_trans', 'hc_mask2mni'),
                               ('_ants_reg0', 'MNI')]
    
    
    
    # connections
    hc_connec.connect([
    (selectfiles, ants_registration,    [('input', 'inputnode.corr_Z')]),
    (selectfiles, ants_registration, [('ants_affine', 'inputnode.ants_affine')] ),
    (selectfiles, ants_registration, [('ants_warp', 'inputnode.ants_warp')] ),

    (ants_registration, sink, [('outputnode.ants_reg_corr_Z', 'hc_connectivity_thr099.'+side+'.hc_masks.' + half)])
        
    ])

    
    hc_connec.run() #it can't run in multiproc as in one moment one file is hardcoded and saved to the disk which is
    #not obvious for the distributing system
    # 'plugin='MultiProc'plugin='CondorDAGMan'))plugin='MultiProc'
    #func_preproc.run()plugin='CondorDAGMan'plugin='CondorDAGMan'plugin='CondorDAGMan'
