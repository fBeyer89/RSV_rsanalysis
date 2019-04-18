
######################
### IMPORT MODULES ###
######################
import os
import nipype.pipeline.engine as pe    
import nipype.interfaces.utility as util
import nipype.interfaces.io as nio
from nilearn_sc_MapsMasker import calc_sc_probabilistic


def  create_sca_nilearn_session_wf(working_dir , data_dir, out_dir, preproc_dir,
                                   subject_id, scan_id_list, MNI_brain_mask, 
                                   out_folder_name, prob_masks, prob_masks_labels):       
        
    
    ###############################################################################################################
    # SPECIFY WORKFLOW
    ###############################################################################################################
    # Create a sca_nilearn_wf workflow
    sca_nilearn_wf = pe.Workflow(name='sca_nilearn_wf')
    sca_nilearn_wf.base_dir =  working_dir
    sca_nilearn_wf.config['execution']['crashdump_dir'] = os.path.join(working_dir, 'crash')
    
    ###############################################################################################################
    # SPECIFY NODES
    ###############################################################################################################
    #####################################
    # Input & Output 
    #####################################
    # Infosource - a function free node to iterate over the list of subjects, scans & masks (function IdentityInterface from nipype.interfaces.utility)
    infosource = pe.Node(util.IdentityInterface(fields=['scan_id']),
                      name="infosource")
    infosource.iterables = [('scan_id', scan_id_list)]
    
    # Node to select files (function SelectFiles from nipype.interfaces.io)
    templates = {'func': 'MRI/'+ subject_id + '/preprocessed/functional/{scan_id}/rest_preprocessed2mni_2mm.nii.gz',
                    }
    selectfiles = pe.Node(nio.SelectFiles(templates,
                                          base_directory = data_dir),
                       name="selectfiles")
    sca_nilearn_wf.connect(infosource, 'scan_id', selectfiles, 'scan_id')
    
    #####################################
    # Analysis 
    #####################################
    
    
    
    # Create the sca_prob_seeds Node, as output nifti file 
    sca_prob_seeds = pe.Node(util.Function(input_names = ['in_file', 'prob_masks', 
                                                           'prob_masks_labels',  'MNI_brain_mask'],
                                     output_names = ['corr_maps_dict'],
                                     function = calc_sc_probabilistic),
                    name='sca_prob_seeds') 
    sca_prob_seeds.inputs.prob_masks = prob_masks
    sca_prob_seeds.inputs.prob_masks_labels = prob_masks_labels
    sca_prob_seeds.inputs.MNI_brain_mask = MNI_brain_mask
                      
    sca_nilearn_wf.connect(selectfiles, 'func', sca_prob_seeds, 'in_file')
    
   
       
    #####################################
    ### Output ###
    #####################################
    
    # function to extract corr_maps from the output dictionary of the sca_prob_seeds node
    def get_corr_map(seed_name, corr_maps_dict):
        corr_map = corr_maps_dict[seed_name]
        return corr_map
        
    # node to extract corr_maps from the output dictionary of the sca_prob_seeds node
    extract_corr_map = pe.Node(util.Function(input_names=['seed_name', 'corr_maps_dict'],
                                                      output_names=['corr_map'],
                                                      function = get_corr_map),
                                  name='extract_corr_map')
    extract_corr_map.iterables= [('seed_name', prob_masks_labels)]   
                                                               
    sca_nilearn_wf.connect(sca_prob_seeds, 'corr_maps_dict', extract_corr_map, 'corr_maps_dict')       
       
       
       
    # make base directory
    def makebase(scan_id, out_folder_name, out_dir):
        return out_dir + out_folder_name + scan_id 
  
    # Node to sink data (function DataSink from nipype.interfaces.io)
    datasink = pe.Node(nio.DataSink(base_directory = out_dir,
                                    parameterization=False),
                      name="datasink")                
    # Use the following DataSink output substitutions
    substitutions = [('_scan_id_', '')]
    datasink.inputs.substitutions = substitutions
    
    sca_nilearn_wf.connect(infosource, ('scan_id', makebase, out_folder_name, out_dir), datasink, 'base_directory')
    
    
    sca_nilearn_wf.connect(extract_corr_map, 'corr_map', datasink, 'fwhm_6')


    
    
    
    
    ###############################################################################################################
    # RUN WORKFLOW
    ###############################################################################################################
    
    #sca_nilearn_wf.write_graph(dotfilename='sca_nilearn_wf', graph2use='flat', format='pdf')
    #sca_nilearn_wf.run()
    #sca_nilearn_wf.run(plugin='CondorDAGMan')    
    sca_nilearn_wf.run(plugin='MultiProc', plugin_args={'n_procs' : 32})

