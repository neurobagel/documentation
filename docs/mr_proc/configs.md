## Global files

---

mr_proc consists of two global files for specifying local data and container paths and recruitment manifest 

---

### Global configs: `global_configs.json`
   - This is a dataset specific file and needs to be modified based on local configs and paths
   - This file is used as an input to all workflow `run scripts` to read, process and track available data
   - Copy, rename, and populate [sample_global_configs.json](https://github.com/neurodatascience/mr_proc/blob/main/sample_global_configs.json) 
   - This file contains:
      - Path to mr_proc_dataset
      - List of pipelines + versions
      - Path to local `container_store` comprising containers used by several workflow scripts

!!! Suggestion

    Although not mandatory, for consistency the preferred location would be: `<DATASET_ROOT>/proc/global_configs.json`.


#### Sample `global_configs.json`
```json
{
    "DATASET_NAME": "MyDataset",
    "DATASET_ROOT": "/path/to/MyDataset",
    "CONTAINER_STORE": "/path/to/container_store",
    "SINGULARITY_PATH": "singularity",
    "TEMPLATEFLOW_DIR": "/path/to/templateflow",

    "BIDS": {
        "heudiconv": {
            "VERSION": "0.11.6",    
            "CONTAINER": "heudiconv_{}.sif",
            "URL": ""
        },
        "validator":{
            "CONTAINER": "bids_validator.sif",
            "URL": ""

        }
    },

    "PROC_PIPELINES": {
        "mriqc": {
            "VERSION": "",
            "CONTAINER": "mriqc_{}.sif",
            "URL": ""
        },
        "fmriprep": {
            "VERSION": "20.2.7",
            "CONTAINER": "fmriprep_{}.sif",
            "URL": ""
        },
        "freesurfer": {
            "VERSION": "6.0.1",
            "CONTAINER": "fmriprep_{}.sif",
            "URL": ""
        }
    }
}
```

### Participant manifest: `mr_proc_manifest.csv`
   - This list serves as the **ground-truth** for subject and visit (i.e. session) availability
   - Create the `mr_proc_manifest.csv` in `<DATASET_ROOT>/tabular/` comprising following columns
      - `participant_id`: ID assigned during recruitment (at times used interchangably with subject_id)
      - `participant_dicom_dir`: participant-level dicom directory name on the disk
      - `visit`: label to denote participant visit for data acquisition (e.g. "baseline", "m12", "m24" or "V01", "V02" etc.)
      - `session`: alternative naming for visit - typically used for imaging data to comply with [BIDS standard](https://bids-specification.readthedocs.io/en/stable/02-common-principles.html)
      - `datatype`: a list of acquired imaging datatype as defined by [BIDS standard](https://bids-specification.readthedocs.io/en/stable/02-common-principles.html)
      - `bids_id`: this is created automatically which attaches `sub-` prefix and removes any non-alphanumeric chacaters (e.g. "-" or "_") from the original `participant_id` string. `participant_id` and `bids_id` in `mr_proc_manifest.csv` are used to link tabular and MRI data
   - New participant are appended upon recruitment as new rows
   - Participants with multiple visits (i.e. sessions) should be added as separate rows


#### Sample `mr_proc_manifest.csv`

| participant_id | participant_dicom_dir | visit | session | datatype                     | bids_id |
|----------------|-----------------------|-------|---------|------------------------------|---------|
| 001            | MyStudy_001_2021      | V01   | ses-01  | ["anat","dwi","fmap","func"] | sub-001 |
| 001            | MyStudy_001_2022      | V02   | ses-02  | ["anat"]                     | sub-001 |
| 002            | MyStudy_002_2021      | V01   | ses-01  | ["anat","dwi"]               | sub-002 |
| 002            | MyStudy_002_2024      | V03   | ses-03  | ["anat","dwi"]               | sub-002 |