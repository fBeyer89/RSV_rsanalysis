
%% apply interpolation from Power 2014
% uses standard SPM functions to handle niftis
%
% 21.3.17, michael.gaebler@gmail.com
% 22.3.17, janis reinelt clean up

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%     DIRECTORIES
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

data_dir = fullfile('/data/pt_nro148/3T/restingstate_and_freesurfer/wd/');  % folder containing subject directories
subjects_file='/data/pt_nro148/3T/restingstate_and_freesurfer/Lists/29_with_scrubbed_vols_FU_withoutRSV001_2.txt'
fileID = fopen(subjects_file);
SubjectsIDs=textscan(fileID,'%s');
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%     set parameters
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
numvols = 545; % number of volumes
TR = 1.4; % TR in s
ofac = 8; % "Ofac = oversampling frequency (generally>=4)"
hifac = 1; % "hifac = highest frequency allowed"
voxbinsize=2000; % set to a lower number in a smaller computer


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%     LOOPING OVER SUBJECTS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

for isub =1:length(SubjectsIDs{:})
    
    SubjectsIDs{:}{isub}
    %func_dir = fullfile(data_dir,subjs(isub));
    
    mkdir(sprintf('/data/pt_nro148/3T/restingstate_and_freesurfer/preprocessing/preprocessed/%s/scrubbed_interpolated/', SubjectsIDs{1}{isub}));
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %     LOOPING OVER SCAN SESSIONS
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    scr_nifti_gz = sprintf('/data/pt_nro148/3T/restingstate_and_freesurfer/wd/%s/lemon_resting/denoise/fix_tr/rest2anat_denoised.nii.gz', SubjectsIDs{1}{isub});
    gunzip(scr_nifti_gz) %(was done already)
    scr_nifti = sprintf('/data/pt_nro148/3T/restingstate_and_freesurfer/wd/%s/lemon_resting/denoise/fix_tr/rest2anat_denoised.nii', SubjectsIDs{1}{isub});
    
    repaired_file =  sprintf('/data/pt_nro148/3T/restingstate_and_freesurfer/preprocessing/preprocessed/%s/scrubbed_interpolated/rest2anat_denoised_scrubbed_intep.nii', SubjectsIDs{1}{isub});
    %movefile(scr_nifti, repaired_file)   
    power_dir = '/data/pt_nro148/3T/restingstate_and_freesurfer/quality_reports/poldrack_reports/'
    

    nifti = spm_vol(scr_nifti); % read nifti header
    mask=spm_vol(sprintf('/data/pt_nro148/3T/restingstate_and_freesurfer/wd/%s/lemon_resting/denoise/resample_brain/T1_brain_mask_lowres.nii.gz', SubjectsIDs{1}{isub}));
    niftivols = spm_read_vols(nifti); % load nifti data
    mask=spm_read_vols(mask);
    size(mask)
    %mask image with brain mask
    mask_repmat=repmat(mask,[1,1,1,numvols]);
    
    
    nifti_masked=niftivols(boolean(mask_repmat));
    transformniftivols=reshape(nifti_masked, [sum(mask(:)),numvols]);
    sizenv = size(niftivols) % size [88 88 64 XXX]
    fprintf('finished loading data')
    
    % from getTransform(): "Input h is a matrix with observations in columns and the number of rows equals the number the time points.
    % For our purposes number of voxels = number of columns."
    
    % figure; imagesc(niftivols(:,:,10)); % display the axial slice where z=10
    
    % create vector of volumes/time points for which observations are present (getTransform() input t)
    
    scrubvols = textread(fullfile(power_dir,SubjectsIDs{1}{isub}, 'scrubvols.txt')); % text file with numbers of scrubbed volumes
    allvols = 1:numvols; % all volumes
    TRtimes = ([1:numvols]'*TR); % TR times of all volumes
    
    nonscrubvols = setdiff(allvols, scrubvols)'; % column vector with numbers of remaining volumes
    % from getTransform(): "Input t is a column vector listing the time points for which observations are present"
    %transformniftivols = reshape(niftivols, sizenv(1)*sizenv(2)*sizenv(3),
    %sizenv(4)); % reshape to get 1-dimensional voxel vector,%not needed as already done before%not needed as already done before
    
    transformniftivols = detrend(transformniftivols);
    temprun = transformniftivols';
    tempanish=zeros(numvols,size(transformniftivols,1));
    
    
    % adopted from FCPROCESS.m
    
    % running getTransform
    voxbin=1:voxbinsize:size(transformniftivols,1);
    voxbin=[voxbin size(transformniftivols,1)];
    size(temprun)
    for v=1:numel(voxbin)-1
        tic
        fprintf(1,'Running %d of %d\r',v,numel(voxbin)-1);
        %from original power-script:
        %tempanish(:,voxbin(v):voxbin(v+1))=getTransform(TRtimes(~~QC(i).runtmask{j}),temprun(~~QC(i).runtmask{j},voxbin(v):voxbin(v+1)),TRtimes,QC(i).TR,ofac,hifac);
        %original as I got from Janis:
        %tempanish(:,voxbin(v):voxbin(v+1))=getTransform(TRtimes(nonscrubvols),temprun(:,voxbin(v):voxbin(v+1)),TRtimes,TR,ofac,hifac);
        tempanish(:,voxbin(v):voxbin(v+1))=getTransform(TRtimes(nonscrubvols),temprun(nonscrubvols,voxbin(v):voxbin(v+1)),TRtimes,TR,ofac,hifac);
        %getTransform (input: scrubbed timeseries (=whole timeseries masked with scrubvols), output: timeseries with
        %full number of volumes interpolated)
        toc
    end
    fprintf(1,'\n');
    
    %size(tempanish)
    % save modified matrix X in the file 'data.nii' (will be overwritten)
    tempanisht = single(tempanish');
    %tempanishint = reshape(tempanisht, [sizenv(1), sizenv(2), sizenv(3), numvols]);
%     
     niftivols_repaired = niftivols;
     niftivols_repl=niftivols; %replace volumes with output of getTransform
     niftivols_repl(boolean(mask_repmat))=tempanisht;
     niftivols_repaired(:,:,:,scrubvols)= niftivols_repl(:,:,:,scrubvols) ;%repaired volumes: only scrubvols are replaced
       
    header = spm_vol(scr_nifti); % read nifti header
    % save as nifti
    for ii=1:numvols
        header(ii).fname = repaired_file;
        spm_write_vol(header(ii),niftivols_repaired(:,:,:,ii));
    end
    
    %check results:
    ts_unscrubbed=niftivols(56,66,24,:);
    ts_scrubbed_and_replaced=niftivols_repaired(56,66,24,:);
    figure
    plot(squeeze(ts_unscrubbed),'b')
    hold on
    plot(squeeze(ts_scrubbed_and_replaced),'r')
    savefig(sprintf('/data/pt_nro148/3T/restingstate_and_freesurfer/preprocessing/preprocessed/%s/scrubbed_interpolated/compare_ts.fig', SubjectsIDs{1}{isub}));
    clear figure
    gzip(scr_nifti)
end



