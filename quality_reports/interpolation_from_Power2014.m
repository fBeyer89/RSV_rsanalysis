
%% apply interpolation from Power 2014
% uses standard SPM functions to handle niftis
%
% 21.3.17, michael.gaebler@gmail.com
% 22.3.17, janis reinelt clean up

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%     DIRECTORIES
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

data_dir = fullfile('/data/pt_nro132/nil2/MRI/');  % folder containing subject directories

subjs = dir(fullfile(data_dir,'NECOS*'));

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%     set parameters
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
numvols = 336; % number of volumes
TR = 1.4; % TR in s
ofac = 8; % "Ofac = oversampling frequency (generally>=4)"
hifac = 1; % "hifac = highest frequency allowed"
voxbinsize=2000; % set to a lower number in a smaller computer


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%     LOOPING OVER SUBJECTS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

for isub = 1:length(subjs)
    
    func_dir = fullfile(data_dir,subjs(isub).name,'preprocessed/functional');
    
    
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %     LOOPING OVER SCAN SESSIONS
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    for irest = 1:6
        
        scr_aroma_nifti_gz = fullfile(func_dir, ['rest', num2str(irest), '.feat/ICA_AROMA_scrubbed/scrubbed_denoised_func_data_nonaggr.nii.gz']);
        
        gunzip(scr_aroma_nifti_gz)
        
        scr_aroma_nifti = fullfile(func_dir, ['rest', num2str(irest), '.feat/ICA_AROMA_scrubbed/scrubbed_denoised_func_data_nonaggr.nii']);
        
        repaired_aroma_file =  fullfile(func_dir, ['rest', num2str(irest), '.feat/ICA_AROMA_scrubbed/scrubbed_repaired_denoised_func.nii']);
        
        hdr_file= '/nobackup/nil1/reinelt/sandkasten/scrubbing_matlab/Interpolation/scrubbed_nifti_interpolated.nii'
        
        power_dir = fullfile(func_dir, ['rest', num2str(irest), '_QA/report_Power'])
        
        uhr = fix(clock);
        disp(strcat({'Startzeit '},num2str(uhr(4)),':',num2str(uhr(5)),':',num2str(uhr(6))))
        disp(strcat({'SUBJECT '}, subjs(isub).name))
        disp(strcat({'scan session '},num2str(irest)))
        
        nifti = spm_vol(scr_aroma_nifti); % read nifti header
        niftivols = spm_read_vols(nifti); % load nifti data
        
        movefile(scr_aroma_nifti, repaired_aroma_file)
        
        sizenv = size(niftivols); % size [88 88 64 XXX]
        
        
        % from getTransform(): "Input h is a matrix with observations in columns and the number of rows equals the number the time points.
        % For our purposes number of voxels = number of columns."
        
        % figure; imagesc(niftivols(:,:,10)); % display the axial slice where z=10
        
        % create vector of volumes/time points for which observations are present (getTransform() input t)
        
        scrubvols = textread(fullfile(power_dir, 'scrubvols.txt')); % text file with numbers of scrubbed volumes
        allvols = 1:numvols; % all volumes
        TRtimes = ([1:numvols]'*TR); % TR times of all volumes
        
        nonscrubvols = setdiff(allvols, scrubvols)'; % column vector with numbers of remaining volumes
        % from getTransform(): "Input t is a column vector listing the time points for which observations are present"
        
        
        % %% Karsten's addition for one voxel (6.3.17)
        %
        % selectedvoxel = detrend(squeeze(niftivols(18,33,23,:))); % random voxel at coordinates 18 33 23
        %
        % selectedvoxel_scrubbed = selectedvoxel;
        % selectedvoxel_scrubbed(scrubvols) = [];
        %
        % selectedvoxel_int = getTransform(TRtimes(nonscrubvols),selectedvoxel_scrubbed,TRtimes,TR,ofac,hifac);
        %
        % selectedvoxel_repaired = selectedvoxel;
        % selectedvoxel_repaired(scrubvols) = selectedvoxel_int(scrubvols);
        %
        % figure
        % plot(selectedvoxel)
        % hold on
        % plot(selectedvoxel_repaired,'r');
        
        transformniftivols = reshape(niftivols, sizenv(1)*sizenv(2)*sizenv(3), sizenv(4)); % reshape to get 1-dimensional voxel vector
        transformniftivols = detrend(transformniftivols);
        temprun = transformniftivols';
        %temprun(scrubvols,:)=[];
        tempanish=zeros(numvols,size(transformniftivols,1));
        
        
        % adopted from FCPROCESS.m
        
        % running getTransform
        voxbin=1:voxbinsize:size(transformniftivols,1);
        voxbin=[voxbin size(transformniftivols,1)];
        for v=1:numel(voxbin)-1
            tic
            fprintf(1,'Running %d of %d\r',v,numel(voxbin)-1);
            tempanish(:,voxbin(v):voxbin(v+1))=getTransform(TRtimes(nonscrubvols),temprun(:,voxbin(v):voxbin(v+1)),TRtimes,TR,ofac,hifac);
            toc
        end
        fprintf(1,'\n');
        
        % save modified matrix X in the file 'data.nii' (will be overwritten)
        tempanisht = single(tempanish');
        tempanishint = reshape(tempanisht, [sizenv(1), sizenv(2), sizenv(3), numvols]);
        
        niftivols_streched = niftivols;
        
        three_d_zero_vol = zeros(size(squeeze(niftivols(:,:,:,1))));
        for i=1:size(scrubvols)
            %disp(scrubvols(i))
            niftivols_streched = cat(4, niftivols_streched(:,:,:, 1:scrubvols(i)-1), three_d_zero_vol, niftivols_streched(:,:,:, scrubvols(i):size(niftivols_streched,4)));
            %test = cat(4, niftivols_repaired(:,:,:, 1:scrubvols(i)-1), three_d_zero_vol, niftivols_repaired(:,:,:, scrubvols(i):size(niftivols_repaired,4)));
            disp(size(niftivols_streched))
        end
        
        niftivols_streched(:,:,:,scrubvols) = tempanishint(:,:,:,scrubvols);
        niftivols_repaired = niftivols_streched ;
        %niftivols_repaired(:,:,:,scrubvols) = tempanishint(:,:,:,scrubvols);
        %niftivols_repaired(scrubvols) = tempanishint(scrubvols);
        % nifti2 = spm_vol('repaired_nifti.nii'); % read nifti header
        
        
        
        header = spm_vol(hdr_file); % read nifti header
        % save as nifti
        for ii=1:numvols
            header(ii).fname = repaired_aroma_file;
            spm_write_vol(header(ii),niftivols_repaired(:,:,:,ii));
        end
        
        
        for i=1:numvols %size(niftivols,4)
            P=spm_vol(['/nobackup/nil1/reinelt/sandkasten/scrubbing_matlab/Interpolation/repaired_nifti.nii,' mat2str(i)]);
            P=spm_write_vol(P,niftivols_repaired(:,:,:,i));
        end
        
        for i=1:numvols %size(niftivols,4)
            P=spm_vol(['/nobackup/nil1/reinelt/sandkasten/scrubbing_matlab/Interpolation/tempanishint.nii,' mat2str(i)]);
            P=spm_write_vol(P,tempanishint(:,:,:,i));
        end
        
        
        %         for i=1:numvols %size(niftivols,4)
        %           P=spm_vol(['scrubbed_repaired_denoised_func.nii,' mat2str(i)]);
        %           disp(P)
        %           P=spm_write_vol(P,niftivols_repaired(:,:,:,i));
        %         end
        
        
        
        %for i=1:size(niftivols,4)
        %  P=spm_vol(['repaired_nifti.nii,' mat2str(i)]);
        %  P=spm_write_vol(P,tempanishint(:,:,:,i));
        %end
        
        % copyfile(fullfile(sourcedir,'unscrubbed_nifti.nii'), fullfile(destdir,'repaired_nifti.nii'))
        
        %     figure
        % plot(selectedvoxel)
        % hold on
        % plot(selectedvoxel_repaired,'g');
        % plot(selectedvoxel_scrubbed,'r');
        
        % plot(selectedvoxel_int,'r');
        
    end
    
end