def scrub_vols(infile, qadir, data_dir,
               motfile ,subject, scan):

    import numpy as np
    import nibabel as nb
    import os, sys
    from time import sleep


    print('#####################')
    print('#####################')
    print('#####################')


    if os.path.isdir(qadir):

        #sleep(0.05)

        # check if scrubvols.txt exists
        scrub_file =  qadir + '/scrubvols.txt'

        if os.path.isfile(scrub_file):

            print('scrubvols.txt for ' + subject + ' ' + scan + ' exists! perform hd fix & scrubbing')

            #load 4d nifti image
            nifti = nb.load(infile)
            img = nb.Nifti1Image(nifti.get_data()[:, :, :, :], nifti.get_affine())
            print(img.header['pixdim'][4])
            img.header['pixdim'][4] = 1.4
            print(img.header['pixdim'][4])


            #read scrubvols.txt to get volumes that need to be scrubbed (minus 1 because deviant starting point, in python first vol = 0)
            with open(scrub_file) as f:
                vols = f.read().splitlines()
                vols_array = np.array(list(map(int, vols)))
                vols_array_minus1 = vols_array - 1

            #read prefiltered_func_data_mcf.par from feat/mc dir & delete volumes from realignment parameter, because they are used to classify motion within ICA AROMA
            with open(motfile) as mopar:
                content_mopar = mopar.read().splitlines()
                content_mopar_array = np.array(content_mopar)

            content_mopar = np.delete(content_mopar_array, vols_array_minus1)

            #write updated prefiltered_func_data_mcf_scrubbed.par
            mopar_scrubbed = data_dir + '/' + subject + '/preprocessed/functional/' + scan + '.feat/mc/prefiltered_func_data_mcf_scrubbed.par'
            with open(mopar_scrubbed, 'w') as mopar_scrubbed_file:
                mopar_scrubbed_file.write("\n".join(map(str, content_mopar)))
            mopar_scrubbed_file.close()

            #scrub volumes from 4d nifti img
            scrubbed_array = np.delete(img.dataobj, vols_array_minus1, axis=3)

            #transform numpy array to nifti object, with the dimensions from the original image
            scrubbed_img = nb.Nifti1Image(scrubbed_array, img.get_affine())
            #scrubbed_img.header['pixdim'][4] = 1.4

            # create empty outfile
            tmp = scan + '.feat/'
            out_file = os.path.join(data_dir, subject, 'preprocessed/functional', tmp, 'scrubbed_filtered_func_data.nii.gz')

            # assign ts to out_file
            scrubbed_img.to_filename(out_file)

            #return out_file


        else:
            print( 'Nothing to scrub but changing TR-info in header to 1.4 sec for ' + subject + ' ' + scan )
            img = nb.load(infile)
            img.header['pixdim'][4] = 1.4
            #print(img.header['pixdim'][4])

            # create empty outfile
            tmp = scan + '.feat/'
            out_file = os.path.join(data_dir, subject, 'preprocessed/functional', tmp, 'filtered_func_data.nii.gz')

            # assign ts to out_file
            img.to_filename(out_file)

    else:
        sys.exit('QA_dir does not exist!')
        #print('QA_dir does not exist!')

    print('#####################')
    print('#####################')
    print('#####################')


       #return out_file


