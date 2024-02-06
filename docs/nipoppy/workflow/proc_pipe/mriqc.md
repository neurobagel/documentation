## MRIQC image processing pipeline

---

MRIQC processes the participants and produces image quality metrics from T1w, T2w and BOLD data.

---


### [MRIQC](https://mriqc.readthedocs.io/en/latest/)
- Use [nipoppy/workflow/proc_pipe/mriqc/run_mriqc.py](https://github.com/neurodatascience/nipoppy/blob/main/nipoppy/workflow/proc_pipe/mriqc/run_mriqc.py) to run MRIQC pipeline directly or wrap the script in an SGE/Slurm script to run on cluster

```bash
python nipoppy/workflow/proc_pipe/mriqc/run_mriqc.py \
	--global_config <global_config_file> \
	--participant_id <participant_id> \
	--session_id <session_id> \
	--modalities <modalities> \
```

The required arguments are:
- `--global_config`: path to the configuration containing the MRIQC container and data directory
- `--participant_id`: participant/subject ID
- `--session_id`: session ID
- `--modality`: modality/modalities to check (valid values: `T1w`, `T2w`, `bold`, `dwi`)
