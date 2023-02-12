## TODO

---

### TODO

---


### 4. Organize (and rename) DICOMs 
   - Scanner DICOM files are named and stored in various formats and locations. In this step we extract, copy, and rename DICOMs in a single directory for all participants with available imaging data. 
       - Copy / download all "raw dicoms" in the `<DATASET_ROOT>/scratch/raw_dicoms` directory.
       - Write a script to extract, copy, and rename these raw DICOMs into `<dataset>/dicom`. Ensure `participant_id` naming matches with `participants.csv` in `<DATASET_ROOT>/tabular/demographics` 
   - Copy a single participant (i.e. dicom dir) into `<DATASET_ROOT>/test_data/dicom`. This participant will serve as a test case for various pipelines. 
   
### 5. Run DICOM --> BIDS conversion using [Heudiconv](https://heudiconv.readthedocs.io/en/latest/) ([tutorial](https://neuroimaging-core-docs.readthedocs.io/en/latest/pages/heudiconv.html))
   - Make sure you have the appropriate HeuDiConv container in your [global configs](./workflow/global_configs.json)
   - Use [run_bids_conv.py](workflow/bids_conv/run_bids_conv.py) to run HeuDiConv `stage_1` and `stage_2`.  
      - Run `stage_1` to generate a list of available protocols from the DICOM header. These protocols are listed in `<DATASET_ROOT>/bids/.heudiconv/<participant_id>/info/dicominfo_ses-<session_id>.tsv`
      - Example command:
         - python run_bids_conv.py --global_config ../global_configs.json --participant_id MNI01 --session_id 01 --stage 1

      - Copy+Rename [sample heuristic file](workflow/bids_conv/sample_heuristic.py) --> `./heuristic.py` to create a name-mapping (i.e. dictionary) for bids organization based on the list of available protocols. **Note that this file automatically gets copied into `$DATASET_ROOT/proc/heuristic.py` to be seen by the Singularity container.**
      - Run `stage_2` to convert the dicoms into BIDS format based on the mapping from `heuristic.py`. 
      - Example command:
         - python run_bids_conv.py --global_config ../global_configs.json --participant_id MNI01 --session_id 01 --stage 2

       - The above scripts are written to work on a single participant. The entire dataset can be BIDSified using a "for loop" or if you have access to a cluster you can run it parallel using queue submission [scripts](workflow/bids_conv/scripts/hpc/)
       - If you are doing this for the first time, you should first try [run_bids_conv.py](workflow/bids_conv/run_bids_conv.py) in a `test mode` by following these steps:
            - Copy a single participant directory from `<DATASET_ROOT>/dicom` to `<DATASET_ROOT>/test_data/dicom` 
            - Run `stage_1` and `stage_2` with [run_bids_conv.py](workflow/bids_conv/run_bids_conv.py) with additional `--test_run` flag. 

### 6. Run BIDS validator
   - Make sure you have the appropriate HeuDiConv container in your `<DATASET_ROOT>/proc/global_configs.json`
   - Use [run_bids_val.sh](workflow/bids_conv/scripts/run_bids_val.sh) to check for errors and warnings
        - Sample command: `run_bids_val.sh <bids_dir> <log_dir>` 
        - Alternatively if your machine has a browser you can also use an online [validator](https://bids-standard.github.io/bids-validator/)
   - Note that Heudiconv is not perfect! Common issues:
       - Make sure you match the version of Heudiconv and BIDS validator standard. 
       - Heuristic file will also need to be updated if your dataset has different protocols for different participants. 
       - You should also open an issue on this repo with the problems and solutions you encounter during processing. 

### 7. Fix HeuDiConv errors
   - If you see errors from BIDS validator, it is possible that HeuDiConv may not be supporting your MRI sequence. In that case add a function to [fix_heudiconv_issues.py](workflow/bids_conv/fix_heudiconv_issues.py) to manually rename files, and run the script posthoc. 
   - Make sure to open an issue on [HeuDiConv Github](https://github.com/nipy/heudiconv/issues) for fix in future release. 
