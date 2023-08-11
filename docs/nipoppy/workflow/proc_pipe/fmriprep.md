### Objective

---

Run [fMRIPrep](https://fmriprep.org/en/stable/) pipeline on BIDS formatted dataset. Note that a standard fMRIPrep run also include FreeSurfer processing.
   
---

### Key directories and files

- `<DATASET_ROOT>/bids`
- `<DATASET_ROOT>/derivatives/fmriprep/`
- `<DATASET_ROOT>/derivatives/freesurfer/`
- `bids_filter.json`

### Procedure

- Ensure you have the appropriate fMRIPrep container listed in your `global_configs.json` 
- Use [run_fmriprep.py](https://github.com/neurodatascience/nipoppy/blob/main/workflow/proc_pipe/fmriprep/run_fmriprep.py) script to run fmriprep pipeline. 
- You can run "anatomical only" workflow by adding `--anat_only` flag
- (Optional) Copy+Rename [sample_bids_filter.json](https://github.com/neurodatascience/nipoppy/blob/main/workflow/proc_pipe/fmriprep/sample_bids_filter.json) to `bids_filter.json` in the code repo itself. Then edit `bids_filter.json` to filter certain modalities / acquisitions. This is common when you have multiple T1w acquisitions (e.g. Neuromelanin, SPIR etc.) for a given modality. 

!!! note

    When `--use_bids_filter` flag is set, this `bids_filter.json` is automatically copied into `<DATASET_ROOT>/bids/bids_filter.json` to be seen by the Singularity container.


- For FreeSurfer tasks, you need to have a [license.txt](https://surfer.nmr.mgh.harvard.edu/fswiki/License) file inside `<DATASET_ROOT>/derivatives/freesurfer/`
- fMRIPrep manages brain-template spaces using [TemplateFlow](https://fmriprep.org/en/stable/spaces.html). These templates can be shared across studies and datasets. Use `global_configs.json` to specify path to `TEMPLATEFLOW_DIR` where these templates can reside. 
   
   
!!! note

    For machines with Internet connections, all required templates are automatically downloaded duing the fMRIPrep run.
    
> Sample cmd:
```bash
python run_fmriprep.py \
   --global_config <global_config_file> \
   --participant_id MNI01 \
   --session_id 01 \
   --use_bids_filter 
```

!!! note

    Unlike DICOM and BIDS run scripts, `run_fmriprep.py` can only process 1 participant at a time due to heavy compute requirements of fMRIPrep. For parallel processing on a cluster, sample HPC job scripts (slurm and sge) are provided in [hpc](https://github.com/neurodatascience/nipoppy/tree/main/workflow/proc_pipe/fmriprep/scripts) subdir. 


!!! note

    You can change default run parameters in the [run_fmriprep.sh](https://github.com/neurodatascience/mr_proc/blob/main/workflow/proc_pipe/fmriprep/scripts/run_fmriprep.sh) by looking at the [documentation](https://fmriprep.org/en/stable/usage.html)

!!! note

    Clean-up working dir (`fmriprep_wf`): fMRIPrep run generates huge number of intermediate files. You should remove those after successful run to free-up space.


### fMRIPrep tasks
   - Main MR processing tasks run by fmriprep (see [fMRIPrep](https://fmriprep.org/en/stable/) for details):
      - Preprocessing
         - Bias correction / Intensity normalization (N4)
         - Brain extraction (ANTs)
         - Spatial normalization to standard space(s)
      - Anatomical
         - Tissue segmentation (FAST)
         - FreeSurfer recon-all
      - Functional
         - BOLD reference image estimation
         - Head-motion estimation
         - Slice time correction
         - Susceptibility Distortion Correction (SDC)
         - Pre-processed BOLD in native space
         - EPI to T1w registration
         - Resampling BOLD runs onto standard spaces
         - EPI sampled to FreeSurfer surfaces
         - Confounds estimation
         - ICA-AROMA (not run by default)
      - Qualtiy Control
         - [Visual reports](https://fmriprep.org/en/stable/outputs.html#visual-reports)