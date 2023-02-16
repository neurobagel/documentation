### MRIQC image processing pipeline

---

MRIQC processes the participants and produces image quality metrics from T1w, T2w and BOLD data.

---


### [MRIQC](https://mriqc.readthedocs.io/en/latest/)
- Ensure you are running the appropriate MRIQC image, as provided [here](https://github.com/neurodatascience/mr_proc/blob/main/workflow/proc_pipe/mriqc/Dockerfile)
- Use [run_mriqc.py](https://github.com/neurodatascience/mr_proc/blob/main/workflow/proc_pipe/mriqc/run_mriqc.py) to run MRIQC pipeline directly or wrap the script in an SGE/Slurm script to run on cluster
	- Mandatory: Pass in the absolute path to the data directory to `global_config`
	- Mandatory: Pass in the absolute path to the results directory to `result_dir`
	- Mandatory: Pass in the absolute path to the participants list to `participant_list`
	- Mandatory: Pass in the absolute path to where the MRIQC container is located to `container`
	- Mandatory: Pass in the index of which subject to run from the participants list to `index`
> Sample cmd:
```bash
python run_mriqc.py \
 	--global_config DATA_DIR \
 	--result_dir RESULTS_DIR \
 	--participant_list PARTICIPANT_LIST \
 	--container CONTAINER_DIR \
 	--index INDEX
```

- The script generates the output and the job log in the listed `result_dir`
!!! note
	A run for a participant is considered successful when the participant's log file reads `Participant level finished successfully`

