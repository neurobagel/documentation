## What is mr_proc? 
*Process long and prosper*

---

mr_proc is a workflow manager for:

1. MRI and tabular data curation
2. Standardized processing 
3. Raw + processed data tracking

---

## Modules

1. `Code`: mr_proc [repo](code_org.md)
2. `Data`: A [dataset](data_org.md) organized in a specific directory structure
3. `Containers`: Singularity containers encapsulating your processing pipelines


## Objectives
1. Standardized data i.e. convert DICOMs into BIDS
2. Run commonly used image processing pipelines e.g. FreeSurfer, fMRIPrep
3. Organize processed MR data inside `derivatives` directory
4. Organize demographic and clinical assessment data inside `tabular` directory
5. Run tracker scripts to populate `bagel.csv` with tabular and processing pipeline metadata
6. Provide metadata to `NeuroBagel` to allow dashboarding and querying participants across multiple studies
    

## Organization
Organization of `Code`, `Data`, and `Container` modules

![mr_proc_org](../imgs/mr_proc_org.jpg)


## Steps
The mr_proc workflow steps and linked identifiers (i.e. participant_id, dicom_id, bids_id) are show below:

![mr_proc_steps](../imgs/steps.jpg)
