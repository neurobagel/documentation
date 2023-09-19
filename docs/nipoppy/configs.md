## Global files

---

Nipoppy requires two global files for specifying local data/container paths and recruitment manifest.

---

### Global configs: `global_configs.json`
   - This is a dataset-specific file and needs to be modified based on local configs and paths
   - This file is used as an input to all workflow runscripts to read, process and track available data
   - Copy, rename, and populate [sample_global_configs.json](https://github.com/neurodatascience/nipoppy/blob/main/nipoppy/sample_global_configs.json) 
   - This file contains:
      - Name of the Nipoppy dataset (`DATASET_NAME`, e.g., `PPMI`)
      - Path to the Nipoppy dataset (`DATASET_ROOT`)
      - Path to a local `CONTAINER_STORE` comprising containers used by several workflow scripts
      - Path to a Singularity executable (`SINGULARITY_PATH`)
      - Path to a TemplateFlow directory, if using fMRIPrep (`TEMPLATEFLOW_DIR`)
      - List of session IDs (`SESSION`, for MRI data) and visit IDs (`VISITS`, for tabular data)
      - Containers + versions for BIDS conversion: HeuDiConv, BIDS validator (`BIDS`)
      - List of processing pipelines + versions (`PROC_PIPELINES`)
      - Information about tabular data (`TABULAR`)
        - Version and path to the data dictionary (`data_dictionary`)

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

    "SESSIONS": ["1","5","7","9","11"],

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

### Participant manifest: `manifest.csv`
   - This list serves as the **ground truth** for subject and visit (i.e. session) availability
   - Create the `manifest.csv` in `<DATASET_ROOT>/tabular/` comprising following columns
      - `participant_id`: ID assigned during recruitment (at times used interchangeably with `subject_id`)
      - `visit`: label to denote participant visit for data acquisition (e.g. `"baseline"`, `"m12"`, `"m24"` or `"V01"`, `"V02"` etc.)
      - `session`: alternative naming for visit - typically used for imaging data to comply with [BIDS standard](https://bids-specification.readthedocs.io/en/stable/02-common-principles.html)
      - `datatype`: a list of acquired imaging datatype as defined by [BIDS standard](https://bids-specification.readthedocs.io/en/stable/02-common-principles.html)
      - `bids_id`: this is the `participant_id` after removing any non-alphanumeric character (e.g. "-" or "_") and attaching the `sub-` prefix. `participant_id` and `bids_id` in the manifest are used to link tabular and MRI data
   - New participant are appended upon recruitment as new rows
   - Participants with multiple visits (i.e. sessions) should be added as separate rows

#### Sample `manifest.csv`

| participant_id | visit | session | datatype                     | bids_id |
|----------------|-------|---------|------------------------------|---------|
| 001            | V01   | ses-01  | ["anat","dwi","fmap","func"] | sub-001 |
| 001            | V02   | ses-02  | ["anat"]                     | sub-001 |
| 002            | V01   | ses-01  | ["anat","dwi"]               | sub-002 |
| 002            | V03   | ses-03  | ["anat","dwi"]               | sub-002 |
