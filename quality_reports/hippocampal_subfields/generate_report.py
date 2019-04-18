from glob import glob
from reports import create_report, read_dists, check
import pandas as pd
from nipype.pipeline.engine import Workflow, Node
from nipype.interfaces.utility import Function, IdentityInterface
from nipype.interfaces.io import SelectFiles
import nipype.interfaces.freesurfer as fs


if __name__ == '__main__':
    
    data_dir = "/nobackup/schiller2/RSV_7T_preprocessing/Freesurfer/"
    out_dir= "/nobackup/schiller2/RSV_7T_preprocessing/hippocampal_subfields_QA/"
    #fs_dir= "/data/pt_nro148/3T/restingstate_and_freesurfer/preprocessing/freesurfer"    
    
    
    subjects_file = '/data/pt_nro148/3T/restingstate_and_freesurfer/Lists/RSV_3T_FU_all_available_subjects.txt'
    stats_file = out_dir+"summary_FU.csv"
    check_file = out_dir+'checklist_FU.txt'
    

    wf = Workflow("reports")
    wf.base_dir = "/nobackup/schiller2/RSV_7T_preprocessing/hippocampal_subfields_QA/wd/"
    wf.config['execution']['crashdump_dir'] = wf.base_dir + "crash_files/"

    with open(subjects_file, 'r') as f: # can be made dependent on scan
        subjects = [line.strip() for line in f]

    subjects=['01']    
    #subjects.sort()
    #subjects.remove('26858')
    #subjects.remove('26435')
    #subjects.remove('27062')
    
    
    #subjects = [x for x in subjects]
    
    
    
#    def make_stats(template):
#        return template
#    
#    make_statsfile = Node(Function(input_names=['template'],
#                                    output_names=['fname'],
#                                    function=make_stats),
#                           name='make_statsfile')
#    make_statsfile.inputs.template = stats_file
#    
#    
#    read_distributions = Node(Function(input_names=['csv_file'],
#                                       output_names=['similarity_distribution',
#                                                     'mean_FD_distribution',
#                                                     'tsnr_distributions'],
#                                       function=read_dists),
#                              name='read_distributions')
    
    
    subject_infosource = Node(IdentityInterface(fields=['subject_id']), 
                              name='subject_infosource')
    subject_infosource.iterables=('subject_id', subjects)
    
    
    # select files
    templates={'brain_fs' : "RSV0{subject_id}.long.RSVX{subject_id}_template/mri/brainmask.mgz",
               'subfields_left' : "RSV0{subject_id}.long.RSVX{subject_id}_template/mri/lh.hippoSfLabels-T1.long.v10.FSvoxelSpace.mgz",
               'subfields_right' : "RSV0{subject_id}.long.RSVX{subject_id}_template/mri/rh.hippoSfLabels-T1.long.v10.FSvoxelSpace.mgz"
               }
    selectfiles = Node(SelectFiles(templates, base_directory=data_dir),
                       name="selectfiles")
      
      
    extract_subfields= Node(fs.Binarize(out_type='nii.gz',
                                      binary_file='hc.nii.gz'),
                name='extract_subfields')
    #extract_hc.iterables= ('match', [[17],[53]])#
    extract_subfields.inputs.match=[206] #17=left, 53=right    
      
    
    brain_convert = Node(fs.MRIConvert(out_type='niigz',
                                       out_file='brain.nii.gz'),
                         name='brain_convert')
    
    def make_out(out_dir, subject_id):
        f = out_dir+"%s_report.pdf"%(subject_id)
        return f
    
    
    make_outfile = Node(Function(input_names=['out_dir',
                                              'subject_id',
                                             ],
                                 output_names=['output_file'], 
                                 function = make_out),
                        name='make_outfile')
    make_outfile.inputs.out_dir = out_dir
    
        
    report = Node(Function(input_names=['subject_id', 
                                         'anat_brain', 
                                         'subfield',
                                         'output_file'], 
                            output_names=['out', 'subject_id'],
                            function = create_report), name="report")
    #report.inputs.parameter_source = 'FSL'
    #report.inputs.fssubjects_dir = fs_dir
    
    check_report = Node(Function(input_names=['subject_id', 'checklist'],
                                 output_names=['checklist'],
                                 function=check),
                        name='check_report')
    check_report.inputs.checklist = check_file
    
    
    
    wf.connect([(subject_infosource, selectfiles, [('subject_id', 'subject_id')]),
                (subject_infosource, make_outfile, [('subject_id', 'subject_id')]),
                (subject_infosource, report, [('subject_id', 'subject_id')]),
                (selectfiles, brain_convert, [('brain_fs', 'in_file')]),
                (brain_convert, report, [('out_file', 'anat_brain')]),
                (selectfiles, extract_subfields, [('subfields_left', 'in_file')]),
                (extract_subfields, report, [('binary_file', 'subfield')]),
                (make_outfile, report, [('output_file', 'output_file')]),
                (report, check_report, [('subject_id', 'subject_id')])
                ])
                
    wf.run() #plugin='MultiProc', plugin_args={'n_procs' : 20})
         
