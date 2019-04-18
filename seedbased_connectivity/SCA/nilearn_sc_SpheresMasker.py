def calc_sc_sphere(in_file, coords, coords_labels ,MNI_brain_mask, radius, FWHM):
                      
    from nilearn.input_data import NiftiMasker,  NiftiSpheresMasker
    import numpy as np
    import os   
     
    # MNI mask
    MNI_brain_mask = MNI_brain_mask
    
    # probabilistic seed regions, 4d nifti file &  corresponding labels
    coords = coords
    coords_labels = coords_labels
    
    # extract time series from coords 
    seed_masker = NiftiSpheresMasker(coords, radius = radius,
                                     standardize=True,
                                    memory='nilearn_cache', 
                                    memory_level=5, verbose=5)
                                    

    seed_time_series_array = seed_masker.fit_transform(in_file)   
    
    # extract time series brain-wide
    brain_masker = NiftiMasker(mask_img = MNI_brain_mask,
                                   smoothing_fwhm= FWHM, standardize=True,
                                   memory='nilearn_cache', 
                                   memory_level=5, verbose=2)
    
    brain_time_series = brain_masker.fit_transform(in_file)
    
    # check if length of coords_labels is equal to number of seed time series 
    # (dependend on number of coordinate sets given with "coords") 
    # break if not equal
    if len(coords_labels) == seed_time_series_array.shape[1]:
        
        icoord = 0
        corr_maps_dict = dict.fromkeys(coords_labels)
        for seed in coords_labels:
            print("##################################")
            print(seed)
            print("##################################")
            
            # assign extracted seed time series from seed_time_series_array 
            # at column icoord to seed_time_series & transpose it (because otherwise they have not the right dimensions?)
            seed_time_series = np.matrix(seed_time_series_array[:,icoord]).T
            
            # compute correlation of all voxels with seed regions
            seed_based_correlations = np.dot(brain_time_series.T, seed_time_series) / \
                                              seed_time_series.shape[0]

            # increase imask to iterate through columns of seed_time_series_array                                  
            icoord = icoord +1 

            # Fisher-z transform the data to achieve a normal distribution
            seed_based_correlations_fisher_z = np.arctanh(seed_based_correlations)    
            
            # transform the 2 dim matrix with the value of each voxel back to a 3 dim image
            seed_based_correlation_img = brain_masker.inverse_transform(seed_based_correlations_fisher_z.T)
            print("##################################")
                      
    
            # initialize  an empty file & "fill" it with the calculated img, necessary becaus nipype needs file types or so... aehm hmm 
            out_file = os.path.abspath('corr_map_' + seed + '_rad5.nii.gz')    
            seed_based_correlation_img.to_filename(out_file)
            
            corr_maps_dict[seed] = out_file            
            
        return  corr_maps_dict            
            
    else :
        print("#####################################################################################")
        print("#####################################################################################")
        print("Number of labels in prob_masks_labels and volumes in prob_masks does not match!!!!!!!")
        print("#####################################################################################")
        print("#####################################################################################")    
