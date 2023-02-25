## Objective

---

Convert DICOMs to BIDS using [Heudiconv](https://heudiconv.readthedocs.io/en/latest/) ([tutorial](https://neuroimaging-core-docs.readthedocs.io/en/latest/pages/heudiconv.html)). 

---

   
### Key directories and files

- `<DATASET_ROOT>/dicom`
- `<DATASET_ROOT>/bids`
- `heuristic.py`

### Procedure

- Ensure you have the appropriate HeuDiConv container listed in your `global_configs.json`
- Use [run_bids_conv.py](https://github.com/neurodatascience/mr_proc/blob/main/workflow/bids_conv/run_bids_conv.py) to run HeuDiConv `stage_1` and `stage_2`.  
   - Run `stage_1` to generate a list of available protocols from the DICOM header. These protocols are listed in `<DATASET_ROOT>/bids/.heudiconv/<participant_id>/info/dicominfo_ses-<session_id>.tsv`
   
> Sample cmd:
```bash
python run_bids_conv.py \
   --global_config <global_config_file> \
   --session_id <session_id> \
   --stage 1
```
      
!!! note

    If participants have multiple sessions (or visits), these need to be converted separately and combined post-hoc to avoid Heudiconv errors. 

- Copy+Rename [sample_heuristic.py](https://github.com/neurodatascience/mr_proc/blob/main/workflow/bids_conv/sample_heuristic.py) to `heuristic.py` in the code repo itself. Then edit `./heuristic.py` to create a name-mapping (i.e. dictionary) for BIDS organization based on the list of available protocols. 

!!! note

    This file automatically gets copied into `<DATASET_ROOT>/proc/heuristic.py` to be seen by the Singularity container.


- Run `stage_2` to convert the dicoms into BIDS format based on the mapping from `heuristic.py`. 

> Sample cmd:
```python
python run_bids_conv.py \
   --global_config <global_config_file> \
   --session_id <session_id> \
   --stage 2
```


### BIDS validator
- Make sure you have the appropriate bids_validator container in your `<DATASET_ROOT>/proc/global_configs.json`
- Use [run_bids_val.sh](https://github.com/neurodatascience/mr_proc/blob/main/workflow/bids_conv/scripts/run_bids_val.sh) to check for errors and warnings
      - Sample command: `run_bids_val.sh <bids_dir> <log_dir>` 
      - Alternatively if your machine has a browser you can also use an online [validator](https://bids-standard.github.io/bids-validator/)


!!! note

    Make sure you match the version of Heudiconv and BIDS validator standard

!!! note

    Heuristic file needs to be updated if your dataset has different protocols for different participants

### Fix HeuDiConv errors
- If you see errors from BIDS validator, it is possible that HeuDiConv may not be supporting your MRI sequence. In that case add a function to [fix_heudiconv_issues.py](https://github.com/neurodatascience/mr_proc/blob/main/workflow/bids_conv/fix_heudiconv_issues.py) to manually rename files, and run the script posthoc. 
- Make sure to open an issue on [HeuDiConv Github](https://github.com/nipy/heudiconv/issues) for fix in future release. 
