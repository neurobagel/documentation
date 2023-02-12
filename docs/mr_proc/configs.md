## Global files

---

mr_proc consists of two global files for specifying local paths and recruitment manifest 

---

### Global configs: `global_configs.json`
   - This is a dataset specific file and needs to be modified based on local configs and paths
   - Copy, rename, and populate [sample_global_configs.json](https://github.com/neurodatascience/mr_proc/blob/main/sample_global_configs.json) 
   - Althogh not mandatory, the preferred location would be: `<DATASET_ROOT>/proc/global_configs.json`
   - This file contains:
      - Path to mr_proc_dataset
      - List of pipelines + versions
      - Path to local `container_store` comprising containers used by several workflow scripts


### Subject manifest: `mr_proc_manifest.csv`
   - This list serves as a **ground-truth** for subject availability
   - Update the `mr_proc_manifest.csv` in `<DATASET_ROOT>/tabular/demographics` comprising at least `participant_id`,`session`, `age`,`sex`,`group` (typically a diagnosis) columns.  
   - New participant details should be appended upon recruitment
   - `participant_id` in this list are used to link MRI and tabular data 
   - Participants with multiple sessions should be added as separate rows
   - BIDS_ID for each participant is created automatically which attaches `sub-` prefix and removes any non-alphanumeric chacaters (e.g. "-" or "_") from the original `participant_id` string. 
              
