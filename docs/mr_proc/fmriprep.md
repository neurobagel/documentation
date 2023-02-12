### 8. Run MR image processing pipelines
Curating dataset into BIDS format simplifies running several commonly used pipelines. Each pipeline follows similar steps:
   - Specify pipeline container (i.e. Singularity image / recipe) 
   - Run single participant test. This uses sample participant from /test_data/bids as input and generates output in the /test_data/<pipeline> dir. 
   - Run entire dataset (provided single participant test is successful)

#### 8.1 [fMRIPrep](https://fmriprep.org/en/stable/) (including FreeSurfer) 
   - Use [run_fmriprep](workflow/proc_pipe/fmriprep/run_fmriprep.py) script to run fmriprep pipeline. 
      - Mandatory: For FreeSurfer tasks, **you need to have a [license.txt](https://surfer.nmr.mgh.harvard.edu/fswiki/License) file inside `<DATASET_ROOT>/derivatives/fmriprep`**
      - Mandatory: fMRIPrep manages brain-template spaces using [TemplateFlow](https://fmriprep.org/en/stable/spaces.html). These templates can be shared across studies and datasets. Use [global configs](./workflow/global_configs.json) to specify path to `TEMPLATEFLOW_DIR` where these templates can reside. For machines with Internet connections, all required templates are automatically downloaded duing the fMRIPrep run. 
      - You can run "anatomical only" workflow by adding `--anat_only` flag
      - Optional: To ignore certain modalities / acquisitions you can create a `bids_filter.json` file. This is common when you have multiple T1w acquisitions (e.g. Neuromelanin, SPIR etc.) in the BIDS directory. See [sample_bids_filter.json](workflow/proc_pipe/fmriprep/sample_bids_filter.json) for an example. **Note that you can create a custom `bids_filter.json` by Copy+Renaming [sample_bids_filter.json](workflow/proc_pipe/fmriprep/sample_bids_filter.json). When `--use_bids_filter` flag is set, this `bids_filter.json` automatically gets copied into `<DATASET_ROOT>/bids/bids_filter.json` to be seen by the Singularity container.** 
      - Similar to HeuDiConv, you can do a test run by adding `--test_run` flag. (Requires a BIDS participant directory inside `<DATASET_ROOT>/test_data/bids`)
   - Example command:
      - python run_fmriprep.py --global_config ../../global_configs.json --participant_id MNI01 --session_id 01 --use_bids_filter
      - You can change default run parameters in the [run_fmriprep.sh](workflow/proc_pipe/fmriprep/scripts/run_fmriprep.sh) by looking at the [documentation](https://fmriprep.org/en/stable/usage.html)

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

   - Validate output 
      - You can check successful completion of the fmriprep run by confirming certain output files. The following two scripts will check `freesurfer` and `fmriprep` specific expeteced files independently.
         - [fsvalidator](workflow/proc_pipe/fmriprep/fs_validator.py)
         - [FS validator](workflow/proc_pipe/fmriprep/fmriprep_validator.py)
      - You should also do a Visual QC using reports provided by fmriprep. 
         - Look at the subject specific [html reports](https://fmriprep.org/en/stable/outputs.html#visual-reports)
         - SDC correction [note](https://neurostars.org/t/weird-results-of-performing-susceptibility-distortion-correction-on-the-epi/20352/2): "It is expected that the frontal lobe shrank after SDC correction. Indeed P>A acquisition has a tendency to “inflate” this area, so SDC correction shrank it to its original shape. More importantly, the functional image after SDC should get closer to anatomical outline" 

   - CLEANUP of working dir
      - fmriprep run generates huge number of intermediate files. You should remove those after successful run to free-up space. 
         - e.g. fmriprep_wf/
