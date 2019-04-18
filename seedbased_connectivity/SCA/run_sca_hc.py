#from necos_MapsMasker_session  import create_sca_nilearn_session_wf

from SpheresMasker_session  import create_sca_nilearn_session_wf


import sys

'''
Meta script to run analysis
-------------------------------------------------
Can run in two modes:
python meta.py s {subject_id}
python meta.py f {text file containing list of subjects}
'''

##########################
### excluded Subjects ###
##########################
excluded_subjects = []
			

################
### MNI mask ###
################
MNI_brain_mask = "/data/pt_nro148/3T/restingstate_and_freesurfer/hipp_analysis/avg152T1_gray_mask_thr100.nii.gz"
#"/home/raid1/fbeyer/Documents/Scripts/ICA_RSN_analysis/MNI/FSL_GM_prob_masks/MNI152_GM_prob_bin_100_3mm.nii.gz"
#'/home/raid1/fbeyer/Documents/Scripts/ICA_RSN_analysis/MNI/MNI_resampled_brain_mask.nii'

################################################
### 4d nifti with probabilistic seed regions ###
###         & corresponding labels           ### 
################################################
#prob_masks = '/scr/nil3/reinelt/NECOS/templates/nilearn_masks/maps/blood_group/anat_prob_amygdala_uni_bilat.nii.gz'

# read in labels file & convert to list
#label_file = open('/scr/nil3/reinelt/NECOS/templates/nilearn_masks/maps/blood_group/anat_prob_amygdala_uni_bilat.txt', 'r')
#prob_masks_labels = label_file.read().split(',')
#prob_masks_labels = [x.strip(' ') for x in prob_masks_labels]
#prob_masks_labels = [x.strip('\n') for x in prob_masks_labels]

#############################
###   MNI coordinates &   ###
### corresponding labels  ### 
#############################

coords =[(-30, -10, -20),(-32, -34, -6),(30, -10, -20),(32, -34, -6)]

coords_labels = ['leftAHc', 'leftpHc', 'rightAHc', 'rightpHc']
#rFI=(38, 26, -10), 
radius=5 #they used 6 but 5 seems more appropriate
FWHM=6

###########################
### output folder name for sca ###
###########################
out_folder_name = '/MNI_coords/'

# Subjects to iterate over
mode=sys.argv[1]            #takes the arguments in command line, pass them to python sys.argv[0] is the name of the script

if mode == 's':             #if the script is executed in the command line like "python dummy.py s NECOS001", sys.argv[0] --> 'dummy.py', sys.argv[1]--> s
    subject_list=[sys.argv[2]]
elif mode == 'f':
    with open(sys.argv[2], 'r') as f:
        full_list = [line.strip() for line in f]
        # Remove subjects from subjects (list)        
        subject_list = [part for part in full_list if part not in excluded_subjects]

   
for subject in subject_list:
    
    print 'Running subject '+subject
    print(coords_labels)

    working_dir = '/data/pt_nro148/3T/restingstate_and_freesurfer/wd/SCA/'+subject+'/' 
    data_dir = '/data/pt_nro148/3T/restingstate_and_freesurfer/preprocessing/preprocessed/'+subject+'/'
    out_dir = '/data/pt_nro148/3T/restingstate_and_freesurfer/preprocessing/preprocessed/'+subject+'/sca/'
          
                                               
    create_sca_nilearn_session_wf(working_dir = working_dir, data_dir = data_dir,
                                 out_dir = out_dir,subject_id = subject,
                                 MNI_brain_mask = MNI_brain_mask, radius=radius, FWHM=FWHM,
                                 out_folder_name = out_folder_name, coords = coords, coords_labels = coords_labels)

                     