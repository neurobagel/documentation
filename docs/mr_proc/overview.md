## What is mr_proc? 
*Process long and prosper*

---

mr_proc is a workflow manager for:

1. MRI and tabular data curation
2. Standarized processing 
3. Raw + processed data tracking

---

mr_proc workflow comprises three modules:

1. `Code`: mr_proc [repo](code_org.md)
2. `Data`: A [dataset](data_org.md) organized in a specific directory structure
3. `Containers`: Singularity containers encapsulating your processing pipelines



## Objectives
1. Standadized data i.e. convert DICOMs into BIDS
2. Run commonly used image processing pipelines e.g. FreeSurfer, fMRIPrep
3. Organize processed MR data inside `derivatives` directory
4. Organize demographic and clinical assessment data inside `tabular` directory
5. Provide metadata to `NeuroBagel` to allow dashboarding and querying participants across multiple studies
    

![mr_proc_org](../imgs/mr_proc_org.jpg)

