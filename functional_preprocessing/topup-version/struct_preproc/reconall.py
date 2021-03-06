# -*- coding: utf-8 -*-
"""
Created on Mon Feb  9 11:12:37 2015

@author: fbeyer
"""

from nipype.pipeline.engine import Workflow, Node
import nipype.interfaces.utility as util
import nipype.interfaces.freesurfer as fs
'''
Workflow to run freesurfer recon-all -all and collect original output
'''
def create_reconall_pipeline(name='reconall'):
    reconall=Workflow(name='reconall')
    #inputnode
    inputnode=Node(util.IdentityInterface(fields=['anat',
    'fs_subjects_dir',
    'fs_subject_id'
    ]),
    name='inputnode')
    outputnode=Node(util.IdentityInterface(fields=['fs_subjects_dir',
    'fs_subject_id']),
    name='outputnode')
    # run reconall
    recon_all = Node(fs.ReconAll(args='-all -hippo-subfields -no-isrunning'), #for RSV152 took out s because of preprocessing with version 6.0
    name="recon_all")
    #recon_all.inputs.directive= 'autorecon2-wm' # -autorecon3
    recon_all.plugin_args={'submit_specs': 'request_memory = 9000'}
    # function to replace / in subject id string with a _
    def sub_id(sub_id):
        return sub_id.replace('/','_')
    reconall.connect([(inputnode, recon_all, [('fs_subjects_dir', 'subjects_dir'),
    ('anat', 'T1_files'),
    (('fs_subject_id', sub_id), 'subject_id')]),
    (recon_all, outputnode, [('subject_id', 'fs_subject_id'),
    ('subjects_dir', 'fs_subjects_dir')])
    ])
    return reconall