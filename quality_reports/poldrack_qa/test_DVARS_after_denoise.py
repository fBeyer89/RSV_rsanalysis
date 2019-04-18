# -*- coding: utf-8 -*-
"""
Created on Mon May 15 13:15:30 2017

@author: fbeyer
"""
import nibabel as nib
import numpy as N
import matplotlib.pyplot as plt

verbose=1
orig_input='/data/pt_nro148/3T/restingstate_and_freesurfer/preprocessing/preprocessed/RSV114/resting_state/coregister/rest_coregistered_nativespace.nii.gz'
infile_wo_scrubbing='/data/pt_nro148/3T/restingstate_and_freesurfer/wd/RSV114/lemon_resting/denoise/fix_tr/rest2anat_denoised.nii.gz'
infile='/data/pt_nro148/3T/restingstate_and_freesurfer/preprocessing/preprocessed/RSV114/scrubbed_interpolated/rest2anat_denoised_scrubbed_intep.nii.gz'
maskfile='/data/pt_nro148/3T/restingstate_and_freesurfer/preprocessing/preprocessed/RSV114/resting_state/denoise/mask/T1_brain_mask_lowres.nii.gz'
print "start loading infile"
img = nib.load(infile)
imgdata = img.get_data()
print "finished loading infile"

img_wo_scrubbing = nib.load(infile_wo_scrubbing)
imgdata_wo_scrubbing = img_wo_scrubbing.get_data()

img_orig_input= nib.load(orig_input)
imgdata_orig_input = img_orig_input.get_data()


maskimg = nib.load(maskfile)
maskdata = maskimg.get_data()
maskvox = N.where(maskdata > 0)
nonmaskvox = N.where(maskdata == 0)
if verbose:
    print 'nmaskvox:', len(maskvox[0])

## load motion parameters and compute FD and identify bad vols for
## potential scrubbing (ala Power et al.)
#
#motpars = N.loadtxt(motfile)
#fd = compute_fd(motpars)
#N.savetxt(os.path.join(qadir, 'fd.txt'), fd)
#
#voxmean = N.mean(imgdata, 3) #temporal mean for each voxel 3 =4th dimension = time
#voxstd = N.std(imgdata, 3) #temporal standard deviation for each voxel
#voxcv = voxstd / N.abs(voxmean)
#voxcv[N.isnan(voxcv)] = 0
#voxcv[voxcv > 1] = 1
#
## compute timepoint statistics
#
#
maskmedian = N.zeros(imgdata.shape[3])
maskmean = N.zeros(imgdata.shape[3])
maskmean_wo_scrubbing= N.zeros(imgdata.shape[3])
maskmean_orig_input= N.zeros(imgdata.shape[3])
maskmad = N.zeros(imgdata.shape[3]) #median absolute deviation = median(abs(a-median(a)/const)
maskcv = N.zeros(imgdata.shape[3])
imgsnr = N.zeros(imgdata.shape[3])
#
for t in range(imgdata.shape[3]):
    tmp = imgdata[:, :, :, t]
    tmp_wo_scrubbing=imgdata_wo_scrubbing[:,:,:,t]
    tmp_orig_data=imgdata_orig_input[:,:,:,t]
    tmp_brain = tmp[maskvox]
    tmp_nonbrain = tmp[nonmaskvox]
    #maskmad[t] = MAD(tmp_brain)
    maskmedian[t] = N.median(tmp_brain)
    maskmean[t] = N.mean(tmp_brain)
    maskmean_wo_scrubbing[t]=N.mean(tmp_wo_scrubbing[maskvox])
    maskmean_orig_input[t]=N.mean(tmp_orig_data[maskvox])
    
    #print maskmean[t]
    #maskcv[t] = maskmad[t] / maskmedian[t]
    #imgsnr[t] = maskmean[t] / N.std(tmp_nonbrain) #classical definition of standard deviatio
#    

#print "mean of maskmean: %d" %(N.mean(maskmean))
#print "std of maskmean: %d" %(N.std(maskmean))
#scaledmean = (maskmean - N.mean(maskmean)) / N.std(maskmean)
plt.figure()
plt.subplot(311)
plt.plot(imgdata_orig_input[55,65,23,:], 'g')
plt.plot(imgdata_orig_input[40,80,50,:], 'g')
plt.subplot(312)
plt.plot(imgdata_wo_scrubbing[55,65,23,:], 'r')
plt.plot(imgdata[55,65,23,:],'b')
plt.subplot(313)
plt.plot(imgdata_wo_scrubbing[40,80,50,:], 'r')
plt.plot(imgdata[40,80,50,:], 'b')
plt.show()

plt.figure()
plt.subplot(211)
plt.plot(maskmean_orig_input, 'g')
plt.subplot(212)
plt.plot(maskmean_wo_scrubbing, 'r')
plt.plot(maskmean,'b')
plt.show()
#plt.show()
mean_running_diff = N.zeros(maskmad.shape)
mean_running_diff = (maskmean[1:] - maskmean[:-1]) / ((maskmean[1:] + maskmean[:-1]) / 2.0)
plt.plot(mean_running_diff, 'r')
DVARS = N.zeros(imgdata.shape[3])
DVARS[1:] = N.sqrt(mean_running_diff ** 2) * 100.0
#N.savetxt(os.path.join(qadir, 'dvars.txt'), DVARS)
plt.figure()
plt.plot(DVARS, 'b')
plt.show()