## Global files

### 1. Create subject manifest
   - Update the `mr_proc_manifest.csv` in `<DATASET_ROOT>/tabular/demographics` comprising at least `participant_id`,`age`,`sex`,`group` (typically a diagnosis) columns.  
       - This list serves as a ground truth for subject availability and participant IDs are used to create BIDS ids downstream.
              
### 2. Populate global configs
   - Copy, rename, and populate [sample_global_configs.json](/sample_global_configs.json) 
   - Althogh not mandatory, the preferred location would be: `<DATASET_ROOT>/proc/global_configs.json`
   - This file contains paths to dataset, pipeline versions, and containers used by several workflow scripts.
   - This is a dataset specific file and needs to be modified based on local configs and paths.