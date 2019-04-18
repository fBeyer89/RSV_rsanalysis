from glob import glob
import nipype.pipeline.engine as pe
import nipype.interfaces.utility as util
import nipype.interfaces.io as nio
#import os

from poldrack_function import fmriqa
from scrub_vols import scrub_vols



if __name__ == '__main__':

    data_dir = "/data/pt_nro148/3T/restingstate_and_freesurfer/"

    #test_dir = "/scr/nil2/reinelt/NECOS/MRI/test"

    #with open('/data/pt_nro148/3T/restingstate_and_freesurfer/Lists/RSV_3T_FUf_all_available_subjects.txt', 'r') as f:
    #    subjects = [line.strip() for line in f]
    #subjects.sort()
    subjects = ['RSV114']
    #scan_id_list = [ 'rest2', 'rest3'] #'rest1', 'rest2', 'rest3', 'rest4', 'rest5', 'rest6',

    for subject in subjects:
        print(subject)

        working_dir = "/data/pt_nro148/3T/restingstate_and_freesurfer/quality_reports/wd_poldrack/" + subject + '/'

        ###############################################################################################################
        # SPECIFY WORKFLOW
        ###############################################################################################################
        wf = pe.Workflow("reports_after_scrubbing")
        wf.base_dir = working_dir
        wf.config['execution']['crashdump_dir'] = wf.base_dir + "crash_files/"



        # Infosource - a function free node to iterate over the list of subjects, scans & masks (function IdentityInterface from nipype.interfaces.utility)
        #infosource = pe.Node(util.IdentityInterface(fields=['scan_id']),
        #                     name="infosource")
        #infosource.iterables = [('scan_id', scan_id_list)]


        # function to create QA dir
        def create_QA(subject, data_dir):
            import os
            QA_dir = os.path.join(data_dir,'quality_reports', 'poldrack_reports', subject)

            if not os.path.exists(QA_dir):
                os.makedirs(QA_dir)
            print QA_dir
            return QA_dir


        # node to to create QA dir
        create_QA_dir_node = pe.Node(util.Function(input_names=['subject', 'data_dir'],
                                                   output_names=['QA_dir'],
                                                   function=create_QA),
                                     name='create_QA_dir_node')

        create_QA_dir_node.inputs.subject = subject
        create_QA_dir_node.inputs.data_dir = data_dir
        #wf.connect(infosource, 'scan_id', create_QA_dir_node, 'scan')

        # node to select files (function SelectFiles from nipype.interfaces.io)
        templates = {#'infile_filtered': 'preprocessing/preprocessed/'+subject +'/resting_state/denoise/rest_preprocessed_nativespace.nii.gz', #with denoising
                     #first run of reports (running without denoising):'infile': '', #without denoising
                     'infile': 'preprocessing/preprocessed/'+ subject + '/resting_state/coregister/rest_coregistered_nativespace.nii.gz',
                     #'preprocessing/preprocessed/'+ subject + '/scrubbed_interpolated/rest2anat_denoised_scrubbed_intep.nii.gz',                     
                     'maskfile': 'preprocessing/preprocessed/'+ subject + '/resting_state/denoise/mask/T1_brain_mask_lowres.nii.gz',
                     'motfile':  'preprocessing/preprocessed/'+ subject + '/resting_state/realign/rest_realigned.par',
                     #'outdir':  subject +  '/preprocessed/functional/{scan_id}_QA/'
                     }
        selectfiles = pe.Node(nio.SelectFiles(templates,
                                              base_directory=data_dir),
                              name="selectfiles")

        #wf.connect(infosource, 'scan_id', selectfiles, 'scan_id')


        # function to create QA dir
        # def fix_header(infile):
        #     import nibabel as nb
        #     import os
        #     img = nb.load(infile)
        #     img.header['pixdim'][4] = 1.4
        #
        #     #out_file = infile
        #     out_file = os.path.dirname(infile) + '/filtered_func_data.nii.gz'
        #     img.to_filename(out_file)
        #
        #     print(img.header['pixdim'][4])
        #     #print(out_file.header['pixdim'][4])
        #
        #     return out_file


        # node to fix TR in header info
        # fix_header_node = pe.Node(util.Function(input_names=['infile'],
        #                                        output_names=['out_file'],
        #                                        function=fix_header),
        #                           name='fix_header_node')
        #
        # wf.connect(selectfiles, 'infile', fix_header_node, 'infile')



        # node for the QA from Poldrack (https://github.com/poldrack/fmriqa)
        QA_check = pe.Node(util.Function(input_names=['infile', 'maskfile', 'motfile',
                                                      'TR', 'outdir', ],
                                               output_names=['qadir'],
                                               function=fmriqa), #from poldrack_function.py!!
                                 name='QA_check')

        QA_check.inputs.TR = 1.4

        #wf.connect(fix_header_node, 'out_file', QA_check, 'infile')
        wf.connect(selectfiles, 'infile', QA_check, 'infile')
        wf.connect(selectfiles, 'maskfile', QA_check, 'maskfile')
        wf.connect(selectfiles, 'motfile', QA_check, 'motfile')
        wf.connect(create_QA_dir_node, 'QA_dir', QA_check, 'outdir')

        # node for scrubbing of bad volumes
       # scrub_fixHD = pe.Node(util.Function(input_names=['infile', 'QA_dir', 'data_dir',
       #                                             'subject'],
       #                                  output_names=[], #'out_file'
       #                                  function=scrub_vols),
       #                    name='scrub_fixHD')

        #scrub_fixHD.inputs.subject = subject
        #scrub_fixHD.inputs.data_dir = data_dir

        #wf.connect(fix_header_node, 'out_file', scrub, 'infile')
        #wf.connect(selectfiles, 'infile', scrub_fixHD, 'infile')
        #wf.connect(create_QA_dir_node, 'QA_dir', scrub_fixHD, 'QA_dir')
        #wf.connect(infosource, 'scan_id', scrub_fixHD, 'scan')

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

