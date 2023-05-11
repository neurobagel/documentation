### MRIQC image processing pipeline

---

MRIQC processes the participants and produces image quality metrics from T1w, T2w and BOLD data.

---


### [MRIQC](https://mriqc.readthedocs.io/en/latest/)
- Ensure you are running the appropriate MRIQC image, as provided [here](https://github.com/neurodatascience/mr_proc/blob/main/workflow/proc_pipe/mriqc/Dockerfile)
- Use [run_mriqc.py](https://github.com/neurodatascience/mr_proc/tree/main/workflow/proc_pipe/mriqc) to run MRIQC pipeline directly or wrap the script in an SGE/Slurm script to run on cluster

python run_mriqc.py --global_config CONFIG.JSON --subject_id 001 --output_dir OUTPUT_DIR_PATH
	- Mandatory: Pass in the absolute path to the configuration containing the MRIQC container and data directory to `global_config`
	- Mandatory: Pass in the subject id to `subject_id`
	- Mandatory: Pass in the absolute path to the output directory to `output_dir`
	
!!! note
	An example config is located [here](https://github.com/neurodatascience/mr_proc/blob/main/sample_global_configs.json)

> Sample cmd:
```bash
python run_mriqc.py \
 	--global_config GLOBAL_CONFIG \
 	--subject_id SUBJECT_ID \
 	--output_dir OUTPUT_DIR
```

!!! note
	A run for a participant is considered successful when the participant's log file reads `Participant level finished successfully`

### Evaluate MRIQC Results
- Use [mriqc_tracker.py](https://github.com/neurodatascience/mr_proc/blob/main/trackers/mriqc_tracker.py) to determine how many subjects successfully passed through the MRIQC pipeline
	- Mandatory: Pass in the subject directory as an argument
- After a successful run of the script, a dictionary called tracker_configs is returned contained whether the subject passed through the pipeline successfully

!!! note
	Multiple sessions can be evaluated, but each session will require a new job running this script

> Sample cmd:
```bash
 from mriqc_tracker import tracker_configs 
 
 results = {}
 for name, func in tracer_configs.items():
 	if type(func) == dict:
 		results[name] = {"MRIQC_BOLD': func['MRIQC_BOLD'](subject_dir)}
 	else: results[name] = func(subject_dir)
```
