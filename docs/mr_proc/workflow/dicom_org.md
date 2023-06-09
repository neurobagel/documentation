## Objective

---

This is a dataset specific process and needs to be customized based on local scanner DICOM dumps and file naming. This organization should produce, for a given session, participant specific dicom dirs. Each of these participant-dir contains a flat list of dicoms for the participant for all available imaging modalities and scan protocols.

---
### Key directories and files

- `<DATASET_ROOT>/downloads`
- `<DATASET_ROOT>/scratch/raw_dicoms`
- `<DATASET_ROOT>/dicom`
- `<DATASET_ROOT>/tabular/demographics/mr_proc_manifest.csv`

### Procedure

- Download DICOM dumps (e.g. ZIPs / tarballs) in the `<DATASET_ROOT>/downloads` directory. It is recommended that different visits (i.e. sessions) are downloaded in separate sub-directories and named as listed in the `global_config.json`.
- Extract (and rename* if needed) all participants into `<DATASET_ROOT>/scratch/raw_dicoms` separately for each visit (i.e. session). 
  

!!! note

    **IMPORTANT**: the participant-level directory names should match participant_ids in the mr_proc_manifest.csv. It is recommended to use participant_id naming format to exclude any non-alphanumeric chacaters (e.g. "-" or "_"). If your participant_id does contain these characters, it is still recommended to remove them from the participant-level DICOM directory names (e.g., QPN_001 --> QPN001).  

!!! note

    It is **okay** for the participant directory to have messy internal subdir tree with DICOMs from multiple modalities. (See [data org schematic](data_org.md) for details). The run script will search and validate all available DICOM files automatically. 


- Run [run_dicom_org.py](https://github.com/neurodatascience/mr_proc/blob/main/workflow/dicom_org/run_dicom_org.py) to:
    - Search: Find all the DICOMs inside the participant directory. 
    - Validate: Excludes certain individual dicom files that are invalid or contain scanner-derived data not compatible with BIDS conversion.
    -  Copy or Symlink (**Recommended**): Creates symlinks from `raw_dicoms/` to the `<DATASET_ROOT>/dicom`, where all participant specific dicoms are in a flat list.

> Sample cmd:
```bash
python run_dicom_org.py \
    --global_config <global_config_file> \
    --session_id <session_id> \
    --use_symlinks 
```