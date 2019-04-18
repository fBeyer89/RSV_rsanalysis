
######################
### IMPORT MODULES ###
######################
import os
import nipype.pipeline.engine as pe    
import nipype.interfaces.utility as util
import nipype.interfaces.io as nio
from nilearn_sc_SpheresMasker import calc_sc_sphere


def  create_sca_nilearn_session_wf(working_dir , data_dir, out_dir, 
                                   subject_id, MNI_brain_mask, radius, FWHM,
                                   out_folder_name, coords, coords_labels):       
        
    
    ###############################################################################################################
    # SPECIFY WORKFLOW
    ###############################################################################################################
    # Create a sca_nilearn_wf workflow
    sca_nilearn_wf = pe.Workflow(name='hyp_nilearn_wf')
    sca_nilearn_wf.base_dir =  working_dir
    sca_nilearn_wf.config['execution']['crashdump_dir'] = os.path.join(working_dir, 'crash')
    
    ###############################################################################################################
    # SPECIFY NODES
    ###############################################################################################################
    #####################################
    # Input & Output 
    #####################################
    # Infosource - a function free node to iterate over the list of subjects, scans & masks (function IdentityInterface from nipype.interfaces.utility)
    templates = {'func':  'resting_state/ants/rest_mni_unsmoothed.nii.gz',
                    }
    selectfiles = pe.Node(nio.SelectFiles(templates,
                                          base_directory = data_dir),
                       name="selectfiles")
    
    
    #####################################
    # Analysis 
    #####################################
    # Create the sca_MNI_coords Node, as output nifti file 
    sca_MNI_coords = pe.Node(util.Function(input_names = ['in_file', 'coords', 
                                                           'coords_labels',  'MNI_brain_mask',
                                                           'radius', 'radius',
                                                           'FWHM', 'FWHM'],
                                     output_names = ['corr_maps_dict'],
                                     function = calc_sc_sphere),
                    name='sca_MNI_coords') 
    sca_MNI_coords.inputs.coords = coords
    sca_MNI_coords.inputs.coords_labels = coords_labels
    sca_MNI_coords.inputs.MNI_brain_mask = MNI_brain_mask
    sca_MNI_coords.inputs.radius = radius
    sca_MNI_coords.inputs.FWHM = FWHM
                      
    sca_nilearn_wf.connect(selectfiles, 'func', sca_MNI_coords, 'in_file')
    
   
       
    #####################################
    ### Output ###
    #####################################
    
    # function to extract corr_maps from the output dictionary of the sca_MNI_coords node
    def get_corr_map(seed_name, corr_maps_dict):
        corr_map = corr_maps_dict[seed_name]
        return corr_map
        
    # node to extract corr_maps from the output dictionary of the sca_MNI_coords node
    extract_corr_map = pe.Node(util.Function(input_names=['seed_name', 'corr_maps_dict'],
                                                      output_names=['corr_map'],
                                                      function = get_corr_map),
                                  name='extract_corr_map')
    extract_corr_map.iterables= [('seed_name', coords_labels)]   
                                                               
    sca_nilearn_wf.connect(sca_MNI_coords, 'corr_maps_dict', extract_corr_map, 'corr_maps_dict')       
       
       
         
    # Node to sink data (function DataSink from nipype.interfaces.io)
    datasink = pe.Node(nio.DataSink(base_directory = out_dir,
                                    parameterization=False),
                      name="datasink")                
    # Use the following DataSink output substitutions
    #substitutions = [('_scan_id_', '')]
    #datasink.inputs.substitutions = substitutions
    
    
    
    
    sca_nilearn_wf.connect(extract_corr_map, 'corr_map', datasink, 'fwhm_6')


    
    
    
    
    ###############################################################################################################
    # RUN WORKFLOW
    ###############################################################################################################
    
    #sca_nilearn_wf.write_graph(dotfilename='sca_nilearn_wf', graph2use='flat', format='pdf')
    #sca_nilearn_wf.run()
    sca_nilearn_wf.run()    
    #sca_nilearn_wf.run(plugin='MultiProc', plugin_args={'n_procs' : 16})plugin='CondorDAGMan'

