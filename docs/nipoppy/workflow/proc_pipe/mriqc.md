## MRIQC image processing pipeline

---

MRIQC processes the participants and produces image quality metrics from T1w, T2w and BOLD data.

---


### [MRIQC](https://mriqc.readthedocs.io/en/latest/)
- Use [nipoppy/workflow/proc_pipe/mriqc/run_mriqc.py](https://github.com/neurodatascience/nipoppy/blob/main/nipoppy/workflow/proc_pipe/mriqc/run_mriqc.py) to run MRIQC pipeline directly or wrap the script in an SGE/Slurm script to run on cluster

```bash
python nipoppy/workflow/proc_pipe/mriqc/run_mriqc.py --global_config CONFIG.JSON --subject_id 001 --output_dir OUTPUT_DIR_PATH
```

- Mandatory: Pass in the absolute path to the configuration containing the MRIQC container and data directory to `global_config`
- Mandatory: Pass in the subject id to `participant_id`
- Mandatory: Pass in the subject id to `session_id`
- Mandatory: Pass in the absolute path to the output directory to `output_dir`

!!! note
	An example config is located [here](https://github.com/neurodatascience/nipoppy/blob/main/nipoppy/sample_global_configs.json)

> Sample cmd:
```bash
python nipoppy/workflow/proc_pipe/mriqc/run_mriqc.py \
 	--global_config GLOBAL_CONFIG \
 	--participant_id SUBJECT_ID \
 	--output_dir OUTPUT_DIR \
 	--session_id SESSION_ID
```

!!! note
	A run for a participant is considered successful when the participant's log file reads `Participant level finished successfully`

