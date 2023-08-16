### MRIQC image processing pipeline

---

MRIQC processes the participants and produces image quality metrics from T1w, T2w and BOLD data.

---


### [MRIQC](https://mriqc.readthedocs.io/en/latest/)
- Ensure you are running the appropriate MRIQC image, as provided [here](https://github.com/neurodatascience/nipoppy/blob/main/workflow/proc_pipe/mriqc/Dockerfile)
- Use [run_mriqc.py](https://github.com/neurodatascience/nipoppy/tree/main/workflow/proc_pipe/mriqc) to run MRIQC pipeline directly or wrap the script in an SGE/Slurm script to run on cluster

python run_mriqc.py --global_config CONFIG.JSON --subject_id 001 --output_dir OUTPUT_DIR_PATH
	- Mandatory: Pass in the absolute path to the configuration containing the MRIQC container and data directory to `global_config`
	- Mandatory: Pass in the subject id to `participant_id`
	- Mandatory: Pass in the subject id to `session_id`
	- Mandatory: Pass in the absolute path to the output directory to `output_dir`
	
!!! note
	An example config is located [here](https://github.com/neurodatascience/nipoppy/blob/main/sample_global_configs.json)

> Sample cmd:
```bash
python run_mriqc.py \
 	--global_config GLOBAL_CONFIG \
 	--participant_id SUBJECT_ID \
 	--output_dir OUTPUT_DIR \
 	--session_id SESSION_ID
```

!!! note
	A run for a participant is considered successful when the participant's log file reads `Participant level finished successfully`

### Evaluate MRIQC Results
- Use [mriqc_tracker.py](https://github.com/neurodatascience/nipoppy/blob/main/trackers/mriqc_tracker.py) to determine how many subjects successfully passed through the MRIQC pipeline
	- Mandatory: Pass in the subject directory as an argument
- After a successful run of the script, a dictionary called tracker_configs is returned contained whether the subject passed through the pipeline successfully

!!! note
	Multiple sessions can be evaluated, but each session will require a new job running this script

> Sample cmd:
```pycon
>>> results = {"pipeline_complete': mriqc_tracker.eval_mriqc(subject_dir, session_id)}
>>> results
 SUCCESS
>>> results = {"MRIQC_BOLD': mriqc_tracker.check_bold(subject_dir, session_id)}
>>> results
 FAIL
```
