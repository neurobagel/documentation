## DICOM organization

---

This is a dataset specific process and needs to be customized based on local scanner DICOM dumps and file naming. This organization should produce, for a given session, participant specific dicom dirs. Each of these participant-dir contains a flat list of dicoms for the participant for all available imaging modalities and scan protocols.

---

### Template procedure

- Copy / download all "raw dicoms" in the `<DATASET_ROOT>/scratch/raw_dicoms` directory.
- Modify [run_dicom_org.py](https://github.com/neurodatascience/mr_proc/blob/main/workflow/dicom_org/run_dicom_org.py) to:
    -  Validate: Excludeds certain individual dicom files that are invalid or contain scanner-derived data not compatible with BIDS conversion.
    -  Symlink (*): Creates symlinks from `raw_dicoms/` to the `<DATASET_ROOT>/dicom`, where all participant specific dicoms are in a flat list. 

> Sample cmd:
```python
python run_dicom_org.py <global_config_file>
```


!!! note

    It is recommended to rename the symlinked participant-level directories if the original participant_id contains any non-alphanumeric chacaters (e.g. "-" or "_"). 