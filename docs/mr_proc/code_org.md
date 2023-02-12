## Code organization

---

mr_proc codebase consists of three modules: 

---

1. scritps: 
    i. Intialize a mr_proc dataset
    ii. Run a mr_proc workflow (i.e. batch call to workflow scipts) 
2. workflow:
    - MRI data
        - Custom script to organize raw dicoms (i.e. scanner output) into a flat participant-level directory. 
        - Convert dicoms into BIDS using [Heudiconv](https://heudiconv.readthedocs.io/en/latest/)
        - Runs a set of containerized MRI image processing pipelines 
    - Tabular data
        - Custom scripts to organize raw tabular data (e.g. clinial assessments)
        - Custom scripts to normalize and standardize data and metadata for downstream harmonization (see [NeuroBagel](../index.md))
3. trackers:
    - Tracks available raw, standardized, and processed data
    - Generates `bagels` for NeuorBagel graph and dashboard. 

--- 

#### legend
- Red: dataset specific code and config
- Yellow: NeuroBagel interface


![code_org](../imgs/code_org.jpg)