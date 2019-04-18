# -*- coding: utf-8 -*-
"""
Created on Mon Feb  9 14:33:51 2015

@author: fbeyer
"""

'''
Main workflow for preprocessing of mprage data
===============================================
Uses file structure set up by conversion
'''
from nipype.pipeline.engine import Node, Workflow
import nipype.interfaces.io as nio
from reconall import create_reconall_pipeline
from mgzconvert import create_mgzconvert_pipeline
from ants import create_normalize_pipeline
#from brainextract import create_brainextract_pipeline

def create_structural(subject, working_dir, data_dir, freesurfer_dir, out_dir, standard_brain):
   
   
    # main workflow
    struct_preproc = Workflow(name='anat_preproc')   
    struct_preproc.base_dir = working_dir
    struct_preproc.config['execution']['crashdump_dir'] = struct_preproc.base_dir + "/crash_files"
    
    # select files
    #templates={'anat': '3T/nifti/MPRAGEADNI32Ch.nii.gz'}
    #selectfiles = Node(nio.SelectFiles(templates, base_directory=data_dir),    name="selectfiles")
    
    # workflow to run freesurfer reconall
    reconall=create_reconall_pipeline()
    reconall.inputs.inputnode.fs_subjects_dir=freesurfer_dir
    reconall.inputs.inputnode.fs_subject_id=subject
    
    # workflow to get brain, head and wmseg from freesurfer and convert to nifti
    mgzconvert = create_mgzconvert_pipeline()
    mgzconvert.inputs.inputnode.fs_subjects_dir=freesurfer_dir
    mgzconvert.inputs.inputnode.fs_subject_id=subject
   
    normalize = create_normalize_pipeline()
    normalize.inputs.inputnode.standard = standard_brain

    # sink to store files
    sink = Node(nio.DataSink(base_directory=out_dir,
                             parameterization=False,
                             substitutions=[
                                 ('transform_Warped', 'T1_brain2mni')]),
                name='sink')

    # connections
    struct_preproc.connect(
        [#(selectfiles, sink, [('anat', 'outputnode.test')]),
         #(selectfiles, reconall, [('anat', 'inputnode.anat')]),   
         #(reconall, mgzconvert,  [('outputnode.fs_subject_id', 'inputnode.fs_subject_id'),
         #                         ('outputnode.fs_subjects_dir', 'inputnode.fs_subjects_dir')]),    
         #for second round of structural don't redo FREESURFER
         (mgzconvert, normalize, [('outputnode.anat_brain', 'inputnode.anat')]),
         (mgzconvert, sink, [('outputnode.anat_head', '@head')]),
         (mgzconvert, sink, [('outputnode.anat_brain', '@brain')]),
         (mgzconvert, sink, [('outputnode.anat_brain_mask', '@mask')]),
         (mgzconvert, sink, [('outputnode.wmedge', '@wmedge')]),
         (normalize, sink, [('outputnode.anat2std', '@anat2std'),
                            ('outputnode.anat2std_transforms', 'transforms2mni.@anat2std_transforms'),
                            ('outputnode.std2anat_transforms', 'transforms2mni.@std2anat_transforms')])
         ])

    struct_preproc.write_graph(dotfilename='struct_preproc.dot', graph2use='colored', format='pdf', simple_form=True)
    # struct_preproc.run()
    struct_preproc.run()  #, plugin_args = {'initial_specs': 'request_memory = 1500'}plugin='CondorDAGMan'
    #struct_preproc.run(plugin='MultiProc')
