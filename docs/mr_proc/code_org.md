## Code organization

---

The `mr_proc` codebase is divided into data processing `workflows` and data availability `trackers`.

---

**`workflow`**

- MRI data
    - Custom script to organize raw DICOMs (i.e. scanner output) into a flat participant-level directory. 
    - Convert DICOMs into BIDS using [Heudiconv](https://heudiconv.readthedocs.io/en/latest/)
    - Runs a set of containerized MRI image processing pipelines 
- Tabular data
    - Custom scripts to organize raw tabular data (e.g. clinial assessments)
    - Custom scripts to normalize and standardize data and metadata for downstream harmonization (see [NeuroBagel](../index.md))

**`trackers`**

- Track available raw, standardized, and processed data
- Generate `bagels` for Neurobagel graph and dashboard. 

--- 

*Legend*
- Red: dataset-specific code and configuration files
- Yellow: Neurobagel interface

![code_org](../imgs/code_org.png)
