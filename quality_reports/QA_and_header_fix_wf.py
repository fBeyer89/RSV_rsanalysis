import nipype.pipeline.engine as pe
import nipype.interfaces.utility as util
import nipype.interfaces.io as nio
import sys

from poldrack_function import fmriqa
from scrub_vols import scrub_vols



#if __name__ == '__main__':

data_dir ="/data/pt_nro132/nil2/MRI"

excluded_subjects = []

# Subjects to iterate over
mode=sys.argv[1]            #takes the arguments in command line, pass them to python sys.argv[0] is the name of the script

if mode == 's':             #if the script is executed in the command line like "python dummy.py s NECOS001", sys.argv[0] --> 'dummy.py', sys.argv[1]--> s
    subject_list=[sys.argv[2]]
elif mode == 'f':
    with open(sys.argv[2], 'r') as f:
        full_list = [line.strip() for line in f]
       # Remove subjects from subjects (list)
        subject_list = [part for part in full_list if part not in excluded_subjects]

#with open('/nobackup/nil1/reinelt/owncloud/scripts/NECOS/preproc/motion/subject_list.txt', 'r') as f:
#    subject_list = [line.strip() for line in f]
#subject_list.sort()

scan_id_list = ['rest1', 'rest2', 'rest3', 'rest4', 'rest5', 'rest6'] #'rest1', 'rest2', 'rest3', 'rest4', 'rest5', 'rest6',

for subject in subject_list:
    print(subject)

    working_dir = '/data/pt_nro132/nil2/reinelt/NECOS/wd_QA_poldrack/' + subject + '/'

    ###############################################################################################################
    # SPECIFY WORKFLOW
    ###############################################################################################################
    wf = pe.Workflow("reports")
    wf.base_dir = working_dir
    wf.config['execution']['crashdump_dir'] = wf.base_dir + "crash_files/"



    # Infosource - a function free node to iterate over the list of subjects, scans & masks (function IdentityInterface from nipype.interfaces.utility)
    infosource = pe.Node(util.IdentityInterface(fields=['scan_id']),
                         name="infosource")
    infosource.iterables = [('scan_id', scan_id_list)]


    # function to create QA dir
    def create_QA(subject, scan, data_dir):
        import os
        tmp = scan + '_QA/'
        QA_dir = os.path.join(data_dir, subject, 'preprocessed/functional', tmp)

        if not os.path.exists(QA_dir):
            os.makedirs(QA_dir)

        return QA_dir


    # node to to create QA dir
    create_QA_dir_node = pe.Node(util.Function(input_names=['subject', 'scan', 'data_dir'],
                                               output_names=['QA_dir'],
                                               function=create_QA),
                                 name='create_QA_dir_node')

    create_QA_dir_node.inputs.subject = subject
    create_QA_dir_node.inputs.data_dir = data_dir
    wf.connect(infosource, 'scan_id', create_QA_dir_node, 'scan')

    # node to select files (function SelectFiles from nipype.interfaces.io)
    templates = {'infile': subject + '/preprocessed/functional/{scan_id}.feat/filtered_func_data.nii.gz',
                 'maskfile': subject + '/preprocessed/functional/{scan_id}.feat/mask.nii.gz',
                 'motfile':  subject +  '/preprocessed/functional/{scan_id}.feat/mc/prefiltered_func_data_mcf.par',
                 #'outdir':  subject +  '/preprocessed/functional/{scan_id}_QA/'
                 }
    selectfiles = pe.Node(nio.SelectFiles(templates,
                                          base_directory=data_dir),
                          name="selectfiles")

    wf.connect(infosource, 'scan_id', selectfiles, 'scan_id')


    # node for the QA from Poldrack (https://github.com/poldrack/fmriqa)
    QA_check = pe.Node(util.Function(input_names=['infile', 'maskfile', 'motfile',
                                                  'TR', 'outdir', ],
                                           output_names=['qadir'], #, 'scrub'
                                           function=fmriqa),
                             name='QA_check')

    QA_check.inputs.TR = 1.4

    #wf.connect(fix_header_node, 'out_file', QA_check, 'infile')
    wf.connect(selectfiles, 'infile', QA_check, 'infile')
    wf.connect(selectfiles, 'maskfile', QA_check, 'maskfile')
    wf.connect(selectfiles, 'motfile', QA_check, 'motfile')
    wf.connect(create_QA_dir_node, 'QA_dir', QA_check, 'outdir')

    # node for scrubbing bad volumes and fixing header info regrding TR (TR is fixed also if there is no volume to scrub)
    scrub_fixHD = pe.Node(util.Function(input_names=['infile', 'qadir', 'data_dir',
                                                     'motfile', 'subject', 'scan' ],
                                     output_names=[], #'out_file'
                                     function=scrub_vols),
                       name='scrub_fixHD')

    scrub_fixHD.inputs.subject = subject
    scrub_fixHD.inputs.data_dir = data_dir

    wf.connect(QA_check, 'qadir', scrub_fixHD, 'qadir')
    wf.connect(selectfiles, 'infile', scrub_fixHD, 'infile')
    wf.connect(selectfiles, 'motfile', scrub_fixHD, 'motfile')
    wf.connect(infosource, 'scan_id', scrub_fixHD, 'scan')

    # Node to sink data (function DataSink from nipype.interfaces.io)
    datasink = pe.Node(nio.DataSink(
                                 substitutions=[('_scan_id_', ''),
                                                ('_epi_mask_', ''),
                                                ('rest_preprocessed2mni_2mm_maths.nii.gz',
                                                 'temporal_std_2mni_2mm.nii.gz')
                                                ]),
                    name="datasink")
    wf.connect(QA_check, 'qadir', datasink, 'qadir')

    wf.write_graph(dotfilename='wf.dot', graph2use='colored', format='pdf', simple_form=True)
    wf.run()

